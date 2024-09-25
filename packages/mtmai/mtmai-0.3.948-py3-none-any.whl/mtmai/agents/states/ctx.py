from typing import Type

import httpx
import orjson
from json_repair import repair_json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from lazify import LazyProxy
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from mtmai.agents.graphs.graph_utils import get_graph_config
from mtmai.agents.retrivers.mtmdoc import MtmDocStore
from mtmai.core.config import settings
from mtmai.core.db import getdb
from mtmai.core.logging import get_logger
from mtmai.llm.embedding import get_default_embeddings
from mtmai.mtlibs.kv.mtmkv import MtmKvStore

logger = get_logger()


class AgentContext:
    def __init__(self, db_engine: Engine):
        self.httpx_session: httpx.Client = None
        self.db: Engine = db_engine
        self.session: Session = Session(db_engine)
        embedding = get_default_embeddings()

        self.vectorstore = MtmDocStore(session=Session(db_engine), embedding=embedding)
        self.kvstore = MtmKvStore(db_engine)

        self.graph_config = get_graph_config()

    def retrive_graph_config(self):
        return self.graph_config

    def load_doc(self):
        return self.vectorstore

    async def call_model_chat(
        self, tpl: PromptTemplate, inputs: dict, structured_output: BaseModel = None
    ):
        llm_chat = self.graph_config.llms.get("chat")
        llm_inst = ChatOpenAI(
            base_url=llm_chat.base_url,
            api_key=llm_chat.api_key,
            model=llm_chat.model,
            temperature=llm_chat.temperature,
            max_tokens=llm_chat.max_tokens,
        )

        messages = await tpl.ainvoke(inputs)
        llm_chain = llm_inst
        # if structured_output:
        #     llm_chain = llm_chain.with_structured_output(
        #         structured_output, include_raw=True
        #     )
        llm_chain = llm_chain.with_retry(stop_after_attempt=5)
        llm_chain = llm_chain.bind(response_format={"type": "json_object"})
        result = await llm_chain.ainvoke(messages)
        return result

    async def astream(
        self, tpl: PromptTemplate, inputs: dict, structured_output: BaseModel = None
    ):
        llm_chat = self.graph_config.llms.get("chat")
        llm_inst = ChatOpenAI(
            base_url=llm_chat.base_url,
            api_key=llm_chat.api_key,
            model=llm_chat.model,
            temperature=llm_chat.temperature,
            max_tokens=llm_chat.max_tokens,
        )

        llm_chain = llm_inst
        # if structured_output:
        #     llm_chain = llm_chain.with_structured_output(
        #         structured_output, include_raw=True
        #     )
        llm_chain = llm_chain.with_retry(stop_after_attempt=5)
        llm_chain = llm_chain.bind(response_format={"type": "json_object"})
        # result = await llm_chain.ainvoke(messages)
        stream = await tpl.astream(inputs)
        async for chunk in stream:
            print(chunk)
        return ""

    def repair_json(self, json_like_input: str):
        """修复 ai 以非标准的json回复 的 json 字符串"""
        good_json_string = repair_json(json_like_input, skip_json_loads=True)
        return good_json_string

    def load_json_response(
        self, ai_json_resonse_text: str, model_class: Type[BaseModel]
    ) -> Type[BaseModel]:
        repaired_json = self.repair_json(ai_json_resonse_text)
        try:
            loaded_data = orjson.loads(repaired_json)
            return model_class(**loaded_data)
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            raise ValueError(
                f"Failed to parse JSON and create {model_class.__name__} instance"
            ) from e

    async def get_db_pool(self):
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
        return pool

    async def get_graph_by_name(self, name: str):
        if name == "storm":
            from mtmai.agents.graphs.storm import StormGraph

            return StormGraph()
        if name == "joke_graph":
            from mtmai.agents.graphs.joke_graph import JokeGraph

            return JokeGraph()
        return None

    async def get_compiled_graph(self, name: str):
        checkpointer2 = AsyncPostgresSaver(await self.get_db_pool())
        graph2 = await self.get_graph_by_name(name)
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


def get_mtmai_ctx():
    db = getdb()
    agent_ctx = AgentContext(
        db_engine=db,
    )
    return agent_ctx


context: AgentContext = LazyProxy(get_mtmai_ctx, enable_cache=False)

# @contextmanager
# def make_agent_context(config: RunnableConfig):
#     session = httpx.Client()
#     db = getdb()
#     embedding = get_default_embeddings()
#     gconfig = get_graph_config()
#     try:
#         vectorstore = MtmDocStore(session=Session(db), embedding=embedding)
#         yield AgentContext(
#             httpx_session=session,
#             db=db,
#             session=Session(db),
#             vectorstore=vectorstore,
#             graph_config=gconfig,
#         )
#     finally:
#         session.close()


# context = Annotated[AgentContext, Context(get_mtmai_ctx)]


# class LcHelper:
#     def __init__(self, state, config: RunnableConfig = None) -> AgentContext:
#         self.state = state
#         self.config = config


# def get_ctx(state, config: RunnableConfig = None) -> AgentContext:
#     ctx = state.get("context")
#     return ctx


# def get_lc_helper(state, config: RunnableConfig = None) -> LcHelper:
#     return LcHelper(self.state, self.config)
