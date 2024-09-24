import logging
import pprint
from typing import Literal

from langchain_core.tools import tool
from langgraph.graph import MessagesState

from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger()


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    if city == "sf":
        return "It's always sunny in sf"
    raise AssertionError("Unknown city")  # noqa: EM101, TRY003


async def weather_node(state: MessagesState):
    tools = [get_weather]
    llm = get_llm_chatbot_default()
    llm_with_tools = llm.bind_tools(tools)
    messages = state["messages"]
    logger.info("开始 weather_node")
    response = await llm_with_tools.ainvoke(messages)
    logger.info(
        "weather_node response: %s",
        # pprint.pformat(response),
        pprint.pformat(response, depth=1),
    )
    return {"messages": [response]}
