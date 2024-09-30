"""
GraphIterator Module
"""

import uuid

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.chainlit.chat_settings import ThreadForm
from mtmai.chainlit.context import context
from mtmai.core.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.crud.curd_site import get_site_by_id
from mtmai.models.chat import ChatProfile
from mtmai.mtlibs.inputs.input_widget import TextInput

logger = get_logger()


class SiteSettingsAgent(ChatAgentBase):
    """
    站点配置Agent
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        # TODO: langgraph 调用入口

        return {}

    @classmethod
    def name(cls):
        return "siteSettings"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="siteSettings",
            description="站点配置",
        )

    async def chat_start(self):
        fnCall_result = await context.emitter.send_call_fn("fn_get_site_id", {})
        # logger.info("函数调用结果 %s", fnCall_result)
        siteId = fnCall_result.get("siteId", "")
        async with get_async_session() as session:
            site = await get_site_by_id(session, uuid.UUID(siteId))
        demo_fn_call_result = await context.emitter.send_form(
            ThreadForm(
                open=True,
                inputs=[
                    TextInput(
                        name="title",
                        label="站点名称",
                        placeholder="请输入站点名称",
                        description="站点名称",
                        value=site.title,
                    ),
                    TextInput(
                        name="description",
                        label="站点描述",
                        placeholder="请输入站点描述",
                        description="站点描述",
                        value=site.description,
                    ),
                ],
            )
        )
        logger.info("表单调用结果 %s", demo_fn_call_result)
        await context.emitter.emit("clear_ask_form", {})
        res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
        if res:
            await cl.Message(
                content="Continue!",
            ).send()

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
