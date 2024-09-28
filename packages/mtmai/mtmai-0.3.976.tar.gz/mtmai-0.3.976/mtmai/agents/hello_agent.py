import orjson
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import mtmai.chainlit as cl
from mtmai.agents.graphs.chat_runner import agent_event_stream_v2
from mtmai.agents.states.ctx import get_mtmai_ctx
from mtmai.agents.states.research_state import Outline
from mtmai.core.logging import get_logger

logger = get_logger()


@cl.step
async def init_outline(topic: str):
    """初始化大纲"""
    ctx = get_mtmai_ctx()
    current_step = cl.context.current_step
    logger.info(f"current_step: {current_step}")

    parser = PydanticOutputParser(pydantic_object=Outline)
    direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific."
                "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
                "\n- Use double quotes for all strings"
                "\n- Ensure all keys and values are properly enclosed"
                "\n- Do not include any text outside of the JSON object"
                "\n- Strictly adhere to the following JSON schema:"
                "\n{format_instructions}"
                "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
            ),
            ("user", "topic is: {topic}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    ai_response = await ctx.call_model_chat(direct_gen_outline_prompt, {"topic": topic})

    loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
    outline: Outline = Outline.model_validate(loaded_data)
    return outline


@cl.step(name="大纲草稿", type="llm")
async def init_outline_v2(topic: str):
    """初始化大纲"""
    ctx = get_mtmai_ctx()
    current_step = cl.context.current_step
    logger.info(f"current_step: {current_step}")

    parser = PydanticOutputParser(pydantic_object=Outline)
    direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific."
                "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
                "\n- Use double quotes for all strings"
                "\n- Ensure all keys and values are properly enclosed"
                "\n- Do not include any text outside of the JSON object"
                "\n- Strictly adhere to the following JSON schema:"
                "\n{format_instructions}"
                "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
            ),
            ("user", "topic is: {topic}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    # ai_response = await ctx.astream(direct_gen_outline_prompt, {"topic": topic})
    messages = await direct_gen_outline_prompt.ainvoke({"topic": topic})
    llm_chat = ctx.graph_config.llms.get("chat")

    llm_inst = ChatOpenAI(
        base_url=llm_chat.base_url,
        api_key=llm_chat.api_key,
        model=llm_chat.model,
        temperature=llm_chat.temperature,
        max_tokens=llm_chat.max_tokens,
    )

    llm_chain = llm_inst.with_retry(stop_after_attempt=5)
    llm_chain = llm_chain.bind(response_format={"type": "json_object"})

    current_step = cl.context.current_step
    async for event in llm_chain.astream_events(messages, version="v2"):
        kind = event["event"]
        node_name = event["name"]
        # logger.info(f"kind: {kind}, node_name: {node_name}")
        data = event["data"]
        if kind == "on_chat_model_stream":
            content = data["chunk"].content
            if content:
                # yield aisdk.text(content)
                await current_step.stream_token(content)

        if kind == "on_chat_model_end":
            output = data.get("output")
            if output:
                chat_output = output.content
                current_step.output = "大语言模型输出：" + chat_output
        if kind == "on_llm_end":
            pass
        # if chunk.content:
        #     print(chunk.content)
        #     await current_step.stream_token(chunk.content)
    # loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
    # outline: Outline = Outline.model_validate(loaded_data)
    return ""


@cl.step(name="笑话生成器(练习和测试目的)", type="llm")
async def step_joke_graph(topic: str):
    """笑话生成器 (练习和测试目的)"""
    ctx = get_mtmai_ctx()
    current_step = cl.context.current_step
    # logger.info(f"current_step: {current_step}")
    await agent_event_stream_v2(model="joke_graph", prompt=topic)


@cl.step
async def hello_step(topic: str):
    async with cl.Step(name="Parent step") as parent_step:
        parent_step.input = "Parent step input"

        result = await init_outline_v2(topic)
        # reply = result.model_dump_json()
        async with cl.Step(name="Child step") as child_step:
            child_step.input = "Child step input"
            child_step.output = "Child step output"

        parent_step.output = "Parent step output"


@cl.step
async def graph_storm_step(topic: str):
    async with cl.Step(name="graph_storm_step") as parent_step:
        parent_step.input = topic

        result = await init_outline(topic)
        reply = result.model_dump_json()
        async with cl.Step(name="Child step") as child_step:
            child_step.input = "Child step input"
            child_step.output = "Child step output"


@cl.step
async def my_step1():
    current_step = cl.context.current_step

    # Override the input of the step
    current_step.input = "My custom input1"

    # Override the output of the step
    current_step.output = "My custom output1"


@cl.step
async def my_step2():
    current_step = cl.context.current_step

    # Override the input of the step
    current_step.input = "My custom input2"

    # Override the output of the step
    current_step.output = "My custom output2"
