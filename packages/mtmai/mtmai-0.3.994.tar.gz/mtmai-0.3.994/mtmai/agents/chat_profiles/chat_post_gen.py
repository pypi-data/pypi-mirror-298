"""
GraphIterator Module
"""

import mtmai.chainlit as cl
from mtmai.chainlit.chat_settings import ThreadForm
from mtmai.chainlit.thread_uistate import ThreadUIState
from mtmai.core.logging import get_logger
from mtmai.mtlibs.inputs.input_widget import TextInput

from ..nodes.base_node import BaseNode

logger = get_logger()


class ChatPostGenNode(BaseNode):
    """ """

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        # TODO: langgraph 调用入口

        return {}

    async def chat_start(self):
        await cl.Message(content="post gen 博客文章生成开始").send()
        await ThreadUIState(
            title="博客文章生成器",
            description="博客文章生成器",
            threadForm=ThreadForm(
                open=True,
                inputs=[
                    TextInput(
                        name="test1"
                        # id="Model",
                        # label="OpenAI - Model",
                        # values=[
                        #     "gpt-3.5-turbo",
                        #     "gpt-3.5-turbo-16k",
                        #     "gpt-4",
                        #     "gpt-4-32k",
                        # ],
                        # initial_index=0,
                    ),
                ],
            ),
        ).send()

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
