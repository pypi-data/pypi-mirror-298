"""
GraphIterator Module
"""

import mtmai.chainlit as cl
from mtmai.chainlit.chat_settings import ThreadForm
from mtmai.chainlit.context import context
from mtmai.core.logging import get_logger
from mtmai.mtlibs.inputs.input_widget import TextInput

from ..nodes.base_node import BaseNode

logger = get_logger()


class ChatPostGenNode(BaseNode):
    """ """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        # TODO: langgraph 调用入口

        return {}

    async def chat_start(self):
        await cl.Message(content="post gen 博客文章生成开始").send()

        demo_fn_call_result = await context.emitter.send_call_fn(
            "demo_fn", {"aaa": "bbb"}
        )
        logger.info("函数调用结果 %s", demo_fn_call_result)

        # 表单演示：
        demo_fn_call_result = await context.emitter.send_form(
            ThreadForm(
                open=True,
                inputs=[
                    TextInput(
                        name="test1",
                        label="prompt",
                        placeholder="请输入prompt",
                        description="附加的提示语",
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

        # await context.emitter.emit ThreadUIState(
        #     title="博客文章生成器",
        #     description="博客文章生成器",
        #     threadForm=ThreadForm(
        #         open=True,
        #         inputs=[
        #             TextInput(
        #                 name="test1",
        #                 label="prompt",
        #                 placeholder="请输入prompt",
        #                 description="附加的提示语",
        #             ),
        #         ],
        #     ),
        # ).send()

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
