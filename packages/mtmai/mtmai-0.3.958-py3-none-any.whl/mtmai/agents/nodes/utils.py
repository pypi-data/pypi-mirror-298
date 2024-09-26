import json

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.runnables import chain as as_runnable
from langgraph.graph import END, START, StateGraph
from mtmai.core.logging import get_logger
from langchain_community.vectorstores import VectorStore


from mtmai.agents.states.research_state import InterviewState, ResearchState

logger = get_logger()

def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.dict(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}


def get_vector_store(state)->VectorStore:
    ctx = state.get("context")
    vs:VectorStore = ctx.vectorstore
    return vs