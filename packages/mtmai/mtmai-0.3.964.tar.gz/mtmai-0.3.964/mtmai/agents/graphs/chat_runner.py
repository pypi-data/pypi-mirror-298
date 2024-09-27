import logging

from langchain_core.runnables import RunnableConfig

import mtmai.chainlit as cl
from mtmai.agents.states.ctx import get_mtmai_ctx
from mtmai.mtlibs import mtutils

logger = logging.getLogger()


async def agent_event_stream_v2(
    *,
    model: str | None = None,
    prompt: str,
):
    current_step = cl.context.current_step
    ctx = get_mtmai_ctx()
    graph = await ctx.get_compiled_graph(model)

    thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
        }
    }
    inputs = {
        "prompt": prompt,
    }
    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=thread,
    ):
        thread_id = thread.get("configurable").get("thread_id")
        # user_id = user.id
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]
        if kind == "on_chat_model_stream":
            if event["metadata"].get("langgraph_node") == "human_node":
                content = data["chunk"].content
                if content:
                    await current_step.stream_token(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        if kind == "on_chat_model_end":
            output = data.get("output")
            if output:
                chat_output = output.content
                current_step.output = "节点输出：" + chat_output

        # if kind == "on_chain_stream":
        #     if data and node_name == "entry_node":
        #         chunk_data = data.get("chunk", {})
        #         picked_data = {
        #             key: chunk_data[key]
        #             for key in ["ui_messages", "uistate"]
        #             if key in chunk_data
        #         }

        #         if picked_data:
        #             yield aisdk.data(picked_data)
        # if kind == "on_chain_end":
        #     chunk_data = data.get("chunk", {})

        #     if node_name == "human_node":
        #         output = data.get("output")
        #         if output:
        #             artifacts = data.get("output").get("artifacts")
        #             if artifacts:
        #                 yield aisdk.data({"artifacts": artifacts})

        #     if node_name == "LangGraph":
        #         logger.info("中止节点")
        #         if (
        #             data
        #             and (output := data.get("output"))
        #             and (final_messages := output.get("messages"))
        #         ):
        #             for message in final_messages:
        #                 message.pretty_print()

        if kind == "on_tool_start":
            logger.info("(@stream)工具调用开始 %s", node_name)
