from sre_parse import State
from mtmai.agents.nodes.utils import get_vector_store
from mtmai.agents.states.research_state import InterviewState, Outline, ResearchState, WikiSection
from langchain_core.runnables import Runnable
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import VectorStore


section_writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert Wikipedia writer. Complete your assigned WikiSection from the following outline:\n\n"
            "{outline}\n\nCite your sources, using the following references:\n\n<Documents>\n{docs}\n<Documents>",
        ),
        ("user", "Write the full WikiSection for the {section} section."),
    ]
)

def format_conversation(interview_state):
    messages = interview_state["messages"]
    convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
    return f'Conversation with {interview_state["editor"].name}\n\n' + convo

class WriteSectionsNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable


    def node_name(self):
        return "gen_question"

    async def __call__(self, state: InterviewState, config: RunnableConfig,):
        """Write the individual sections of the article"""
        outline = state["outline"]


        refined_outline = await self.get_refine_outline(State)

        sections = await self.get_section_writer(state).abatch(
            [
                {
                    "outline": refined_outline.as_str,
                    "section": section.section_title,
                    "topic": state["topic"],
                }
                for section in outline.sections
            ]
        )
        return {
            **state,
            "sections": sections,
        }

    async def get_section_writer(self, state: ResearchState):
        vs = get_vector_store(state)
        retriever = vs.as_retriever(k=10)
        async def retrieve(inputs: dict):
            docs = await retriever.ainvoke(inputs["topic"] + ": " + inputs["section"])
            formatted = "\n".join(
                [
                    f'<Document href="{doc.metadata["source"]}"/>\n{doc.page_content}\n</Document>'
                    for doc in docs
                ]
            )
            return {"docs": formatted, **inputs}
        section_writer = (
            retrieve
            | section_writer_prompt
            | self.runnable.with_structured_output(WikiSection).with_retry(stop_after_attempt=3)
        )
        return section_writer


    async def get_refine_outline(self, state: ResearchState):
        refine_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a Wikipedia writer. You have gathered information from experts and search engines. Now, you are refining the outline of the Wikipedia page. \
        You need to make sure that the outline is comprehensive and specific. \
        Topic you are writing about: {topic}

        Old outline:

        {old_outline}""",
                ),
                (
                    "user",
                    "Refine the outline based on your conversations with subject-matter experts:\n\nConversations:\n\n{conversations}\n\nWrite the refined Wikipedia outline:",
                ),
            ]
        )

        # Using turbo preview since the context can get quite long
        refine_outline_chain = refine_outline_prompt | self.runnable.with_structured_output(
            Outline
        )

        convos = "\n\n".join(
            [
                format_conversation(interview_state)
                for interview_state in state.get("interview_results", [])
            ]
        )

        updated_outline = await refine_outline_chain.ainvoke(
            {
                "topic": state["topic"],
                "old_outline": state["outline"].as_str,
                "conversations": convos,
            }
        )
        return {**state, "outline": updated_outline}

