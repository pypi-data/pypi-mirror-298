"""
GraphIterator Module
"""

import mtmai.chainlit as cl

from .base_node import BaseNode

DEFAULT_BATCHSIZE = 16


class ChatPostGenNode(BaseNode):
    """ """

    def __init__(
        self,
        # input: str,
        # output: List[str],
        # node_config: Optional[dict] = None,
        # node_name: str = "GraphIterator",
    ):
        # super().__init__(codename, "node", input, output, 2, node_config)

        # self.verbose = (
        #     False if node_config is None else node_config.get("verbose", False)
        # )
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        await cl.Message(content="欢迎 post gen开始吧").send()

        return {}

    async def chat(self):
        await cl.Message(content="欢迎 post gen开始吧").send()
