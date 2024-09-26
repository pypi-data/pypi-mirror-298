import logging
from functools import lru_cache

from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from sqlmodel import Session, select

from mtmai.core.config import settings
from mtmai.models.agent import AgentMeta, Chatbot, UiMessage
from mtmai.models.models import User
from mtmai.mtlibs import aisdk, mtutils

logger = logging.getLogger()


@lru_cache(maxsize=1000)
async def get_graph_by_name(name: str):
    if name == "storm":
        from mtmai.agents.graphs.storm import StormGraph

        return StormGraph()
    if name == "joke_graph":
        from mtmai.agents.graphs.joke_graph import JokeGraph

        return JokeGraph()
    return None


# def sync_get_graph(name: str):
#     return asyncio.run(async_get_graph(name))


# @lru_cache(maxsize=1000)
# def get_graph(name: str):
#     return sync_get_graph(name)


@lru_cache(maxsize=1000)
async def get_graph(name: str):
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    await pool.open()
    checkpointer2 = AsyncPostgresSaver(pool)
    graph2 = await get_graph_by_name(name)
    workflow = graph2.create_graph()
    interrupt_after = []
    human_node = workflow.nodes.get("human_node")
    if human_node:
        interrupt_after.append("human_node")
    graph = workflow.compile(
        checkpointer=checkpointer2,
        interrupt_after=interrupt_after,
        debug=True,
    )
    return graph


all_agents = [
    AgentMeta(
        id="mtmaibot",
        name="mtmaibot",
        label="AI聊天",
        base_url=settings.API_V1_STR + "/mtmaibot",
        description="基于 graph 的综合智能体(开发版)",
        # is_dev=True,
    ),
]


class ChatCompletinRequest(BaseModel):
    thread_id: str | None = None
    chat_id: str | None = None
    prompt: str
    option: str | None = None
    task: dict | None = None


async def agent_event_stream(
    *,
    model: str | None = None,
    session: Session,
    user: User,
    prompt: str,
    chat_id: str | None = None,
    thread_id: str | None = None,
):
    graph_name = model
    graph = await get_graph(graph_name)
    if not graph:
        raise Exception(status_code=503, detail=f"No atent model found: {model}")

    if not chat_id:
        # 如果没有提供 chat_id，创建新的 chat
        chatbot = Chatbot(
            name="New Chat",
            description="New Chat",
        )
        session.add(chatbot)
        session.commit()
        chat_id = chatbot.id
        # 通知前端创建了新的chat_id
        yield aisdk.data(
            {
                "chat_id": chatbot.id,
            }
        )
    else:
        # 确保提供的 chat_id 存在
        chatbot = session.exec(select(Chatbot).where(Chatbot.id == chat_id)).first()
        if not chatbot:
            # 如果提供的 chat_id 不存在，创建新的 chat
            chatbot = Chatbot(
                name="New Chat",
                description="New Chat",
            )
            session.add(chatbot)
            session.commit()
            chat_id = chatbot.id
            # 通知前端创建了新的chat_id
            yield aisdk.data(
                {
                    "chat_id": chatbot.id,
                }
            )

    new_message = UiMessage(
        component="UserMessage",
        content=prompt,
        props={"content": prompt},
        chatbot_id=chat_id,
        role="user",
    )
    session.add(new_message)
    session.commit()

    # 加载聊天消息历史
    # FIXME: 用户消息的加载有待优化
    chat_messages = session.exec(
        select(UiMessage)
        .where(UiMessage.chatbot_id == chat_id)
        .order_by(UiMessage.created_at)
    ).all()

    # 从数据库的聊天记录构造 langgraph 的聊天记录
    langgraph_messages = []
    for message in chat_messages:
        if message.content:
            langgraph_message = ChatMessage(
                role="user" if message.role == "user" else "assistant",
                content=message.content if message.role == "user" else message.response,
            )
            langgraph_messages.append(langgraph_message)

    if not thread_id:
        thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user.id,
            "chat_id": chat_id,
        }
    }

    inputs = {
        "user_id": user.id,
        "user_input": prompt,
        "messages": [*langgraph_messages],
    }
    state = await graph.aget_state(thread)

    if state.created_at is not None:
        # 是人机交互继续执行的情况
        await graph.aupdate_state(
            thread,
            inputs,
            as_node="human_node",
        )
        inputs = None

    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=thread,
    ):
        thread_id = thread.get("configurable").get("thread_id")
        user_id = user.id
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]
        if kind == "on_chat_model_stream":
            if event["metadata"].get("langgraph_node") == "human_node":
                content = data["chunk"].content
                if content:
                    yield aisdk.text(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        if kind == "on_chain_stream":
            if data and node_name == "entry_node":
                chunk_data = data.get("chunk", {})
                picked_data = {
                    key: chunk_data[key]
                    for key in ["ui_messages", "uistate"]
                    if key in chunk_data
                }

                if picked_data:
                    yield aisdk.data(picked_data)
        if kind == "on_chain_end":
            chunk_data = data.get("chunk", {})

            if node_name == "human_node":
                output = data.get("output")
                if output:
                    artifacts = data.get("output").get("artifacts")
                    if artifacts:
                        yield aisdk.data({"artifacts": artifacts})

                ui_messages = output.get("ui_messages", [])
                if len(ui_messages) > 0:
                    for uim in ui_messages:
                        db_ui_message2 = UiMessage(
                            # thread_id=thread_id,
                            chatbot_id=chat_id,
                            user_id=user_id,
                            component=uim.component,
                            content=uim.content,
                            props=uim.props,
                            artifacts=uim.artifacts,
                        )
                        session.add(db_ui_message2)
                        session.commit()

                    # 跳过前端已经乐观更新的组件
                    skip_components = ["UserMessage", "AiCompletion"]
                    filterd_components = [
                        x for x in ui_messages if x.component not in skip_components
                    ]
                    yield aisdk.data(
                        {
                            "ui_messages": filterd_components,
                        }
                    )
                if output.get("uistate"):
                    yield aisdk.data(
                        {
                            "uistate": output.get("uistate"),
                        }
                    )

            # if node_name == "entry_node":
            #     task_title = data.get("task_title", "no-title")
            #     item = AgentTask(thread_id=thread_id, user_id=user_id, title=task_title)
            #     session.add(item)
            #     session.commit()

            if node_name == "LangGraph":
                logger.info("中止节点")
                if (
                    data
                    and (output := data.get("output"))
                    and (final_messages := output.get("messages"))
                ):
                    for message in final_messages:
                        message.pretty_print()

        if kind == "on_tool_start":
            logger.info("(@stream)工具调用开始 %s", node_name)
        # if kind == "on_tool_end":
        #     output = data.get("output")
        #     if output and output.artifact:
        #         yield aisdk.data(output.artifact)

    yield aisdk.finish()
