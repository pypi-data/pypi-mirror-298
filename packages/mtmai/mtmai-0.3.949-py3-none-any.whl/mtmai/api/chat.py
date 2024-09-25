from typing import Annotated

import orjson
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

import mtmai.chainlit as cl
import mtmai.chainlit.data as cl_data
from mtmai.agents.hello_agent import step_joke_graph
from mtmai.agents.states.ctx import get_mtmai_ctx
from mtmai.agents.states.research_state import Outline
from mtmai.auth import authenticate_user
from mtmai.chainlit.context import init_http_context, init_ws_context
from mtmai.chainlit.element import Element
from mtmai.chainlit.input_widget import Select, Slider, Switch
from mtmai.chainlit.session import WebsocketSession
from mtmai.core.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.crud import crud
from mtmai.deps import SessionDep
from mtmai.models.chat import ChatProfile
from mtmai.models.models import User
from mtmai.mtlibs.chainlit.data_layer import SQLAlchemyDataLayer

# from mtmai.mtlibs.chainlit.data_layer import SQLAlchemyDataLayer

# 使用自定义的 sql 存储chainlit数据
cl_data._data_layer = SQLAlchemyDataLayer()

router = APIRouter()
logger = get_logger()


async def init_outline(topic: str):
    """初始化大纲"""
    ctx = get_mtmai_ctx()
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


@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    async with get_async_session() as session:
        user = await crud.authenticate(
            session=session, email=username, password=password
        )
    if user:
        return cl.User(
            id=user.id,
            identifier=user.username,
            metadata={"role": "admin", "provider": "credentials"},
        )
    else:
        return None


# @cl.header_auth_callback
# async def header_auth_callback(headers: Dict) -> Optional[cl.User]:
#     auth_header = headers.get("Authorization")
#     if auth_header and auth_header.startswith("Bearer "):
#         token = auth_header.split(" ")[1]
#         try:
#             token_data = verify_token(token)
#             # db = get_session_v2()
#             async with get_async_session() as session:
#                 user = await crud.get_user_by_username(
#                     session, username=token_data.username
#                 )
#                 if user:
#                     return cl.User(
#                         id=user.id,
#                         identifier=user.username,
#                         metadata={"role": "admin", "provider": "jwt"},
#                     )
#         except:
#             pass
#     return None


# @cl.header_auth_callback
# def header_auth_callback(headers: Dict) -> Optional[cl.User]:
#     # Verify the signature of a token in the header (ex: jwt token)
#     # or check that the value is matching a row from your database
#     if headers.get("test-header") == "test-value":
#         return cl.User(
#             identifier="admin", metadata={"role": "admin", "provider": "header"}
#         )
#     else:
#         return None


async def get_all_profiles():
    all_profiles = [
        ChatProfile(
            name="GPT-3.5",
            description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
        ),
        ChatProfile(
            name="GPT-3.6",
            default=True,
            description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
        ),
    ]
    return all_profiles


async def get_default_chat_profile():
    return next(
        (profile for profile in await get_all_profiles() if profile.default), None
    )


@cl.set_chat_profiles
async def chat_profile(current_user: User):
    logger.info("当前用户 %s", current_user)
    clChatProfiles = [
        cl.ChatProfile(
            name=profile.name,
            markdown_description=profile.description,
            icon=profile.icon,
            default=profile.default,
            starters=profile.starters,
        )
        for profile in await get_all_profiles()
    ]

    return clChatProfiles


@cl.on_chat_start
async def chat_start():
    user = cl.user_session.get("user")
    chat_profile = cl.user_session.get("chat_profile")
    if not chat_profile:
        chat_profile_obj = await get_default_chat_profile()
        if chat_profile_obj:
            chat_profile = chat_profile_obj.name
        else:
            logger.error("没有找到默认的聊天配置文件")
    logger.info("chat start with profile %s", chat_profile)

    await cl.Message(
        content=f"欢迎 {user.username} 使用 {chat_profile} , 开始吧"
    ).send()
    # await cl.Message(
    #     content="环境准备好了, 你可以开始提问了",
    # ).send()

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                initial_index=0,
            ),
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Slider(
                id="SAI_Steps",
                label="Stability AI - Steps",
                initial=30,
                min=10,
                max=150,
                step=1,
                description="Amount of inference steps performed on image generation.",
            ),
            Slider(
                id="SAI_Cfg_Scale",
                label="Stability AI - Cfg_Scale",
                initial=7,
                min=1,
                max=35,
                step=0.1,
                description="Influences how strongly your generation is guided to match your prompt.",
            ),
            Slider(
                id="SAI_Width",
                label="Stability AI - Image Width",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
            Slider(
                id="SAI_Height",
                label="Stability AI - Image Height",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
        ]
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    logger.info("on_settings_update", settings)


@cl.on_chat_end
def end():
    logger.info("goodbye %s", cl.user_session.get("id", ""))


@cl.on_message
async def on_message(message: cl.Message):
    app_user = cl.user_session.get("user")

    # global counter
    # counter += 1
    await step_joke_graph(topic=message.content)
    # logger.info(f"Received message {counter}")
    # await hello_step(topic=message.content)
    # await my_step1()
    # await my_step2()
    # topic = message.content
    # result = await init_outline(topic)
    # reply = result.model_dump_json()
    # await cl.Message(
    #     content=f"Received: {reply}",
    # ).send()


@router.get("/cl/1")
async def login_access_token(session: SessionDep):
    init_http_context()
    current_step = cl.context.current_step
    print("current_step = cl.context.current_step")
    await cl.Message(content="Hello, I am a chatbot!").send()
    return {"message": "Hello World from main app"}


@router.get("/hello/{session_id}")
async def hello(
    request: Request,
    session_id: str,
    current_user: Annotated[cl.User, Depends(authenticate_user)],
):
    ws_session = WebsocketSession.get_by_id(session_id=session_id)
    init_ws_context(ws_session)
    await cl.Message(content="Hello World").send()
    return "Data sent to the websocket client"


@router.get("/hello")
async def cl_hello(
    request: Request,
    current_user: Annotated[cl.User, Depends(authenticate_user)],
):
    print(current_user)
    init_http_context(user=current_user)
    await cl.Message(content="Hello World").send()
    return HTMLResponse("Hello World")


@router.get("/hello2", response_model=Element)
async def cl_hello2(
    request: Request,
    current_user: Annotated[cl.User, Depends(authenticate_user)],
):
    data = Element(
        type="image",
        name="Hello World",
        content="Hello World",
    )
    return data
