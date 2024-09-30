"""
GraphIterator Module
"""

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.chainlit.context import context
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile

logger = get_logger()


class PostGenAgent(ChatAgentBase):
    """
    前端站点的 “AI生成新文章”按钮，调用这个agent
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
    def get_chat_profile(self):
        return ChatProfile(
            name="postGen",
            # default=F,
            description="博客文章生成器",
        )

    async def chat_start(self):
        await cl.Message(content="post gen 博客文章生成开始").send()

        # 获取页面上下文参数

        fnCall_result = await context.emitter.send_call_fn("fn_get_site_id", {})
        # logger.info("函数调用结果 %s", fnCall_result)
        siteId = fnCall_result.get("siteId", "")
        await cl.Message(content=f"siteId: {siteId}").send()
        # 表单演示：
        # demo_fn_call_result = await context.emitter.send_form(
        #     ThreadForm(
        #         open=True,
        #         inputs=[
        #             TextInput(
        #                 name="test1",
        #                 label="prompt",
        #                 placeholder="请输入prompt",
        #                 description="附加的提示语",
        #             ),
        #         ],
        #     )
        # )
        # logger.info("表单调用结果 %s", demo_fn_call_result)
        # await context.emitter.emit("clear_ask_form", {})
        # res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
        # if res:
        #     await cl.Message(
        #         content="Continue!",
        #     ).send()

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
