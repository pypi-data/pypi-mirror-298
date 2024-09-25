from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import tools_condition

from mtmai.agents.states.state import MainState
from mtmai.core.logging import get_logger

logger = get_logger()


def edge_human_input(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "chat_tools_node"
    next_to = state.get("next")
    if next_to:
        return next_to
    return "__end__"


class HumanInputNode:
    def __init__(
        self,
    ):
        pass

    def node_name(self):
        return "human_input_node"

    async def __call__(self, state: MainState, config: RunnableConfig):
        last_message = state.get("messages")[-1]
        logger.info(f"进入 human node: {last_message}")
        return {
            "messages": [last_message],
        }
