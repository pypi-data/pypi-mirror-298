from fastapi import APIRouter

import mtmai.chainlit as cl
import mtmai.chainlit.data as cl_data
from mtmai.agents.chat_profiles.chat_post_gen import ChatPostGenNode
from mtmai.agents.chat_profiles.profiles import (
    get_all_profiles,
    get_default_chat_profile,
)
from mtmai.core.logging import get_logger
from mtmai.models.models import User
from mtmai.mtlibs.chainlit.data_layer import SQLAlchemyDataLayer

# from mtmai.mtlibs.chainlit.data_layer import SQLAlchemyDataLayer

# 使用自定义的 sql 存储chainlit数据
cl_data._data_layer = SQLAlchemyDataLayer()

router = APIRouter()
logger = get_logger()


# async def init_outline(topic: str):
#     """初始化大纲"""
#     ctx = get_mtmai_ctx()
#     parser = PydanticOutputParser(pydantic_object=Outline)
#     direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific."
#                 "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
#                 "\n- Use double quotes for all strings"
#                 "\n- Ensure all keys and values are properly enclosed"
#                 "\n- Do not include any text outside of the JSON object"
#                 "\n- Strictly adhere to the following JSON schema:"
#                 "\n{format_instructions}"
#                 "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
#             ),
#             ("user", "topic is: {topic}"),
#         ]
#     ).partial(format_instructions=parser.get_format_instructions())
#     ai_response = await ctx.call_model_chat(direct_gen_outline_prompt, {"topic": topic})

#     loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
#     outline: Outline = Outline.model_validate(loaded_data)
#     return outline


# @cl.password_auth_callback
# async def auth_callback(username: str, password: str):
#     async with get_async_session() as session:
#         user = await crud.authenticate(
#             session=session, email=username, password=password
#         )
#     if user:
#         return cl.User(
#             id=user.id,
#             identifier=user.username,
#             metadata={"role": "admin", "provider": "credentials"},
#         )
#     else:
#         return None


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
    # user = cl.user_session.get("user")
    chat_profile = cl.user_session.get("chat_profile")
    if not chat_profile:
        chat_profile_obj = await get_default_chat_profile()
        if chat_profile_obj:
            chat_profile = chat_profile_obj.name
        else:
            logger.error("没有找到默认的聊天配置文件")
            await cl.Message(content="内部出错: 没有找到默认的聊天配置文件").send()
            return
    logger.info("chat start with profile %s", chat_profile)

    # await cl.Message(
    #     content=f"欢迎 {user.username} 使用 {chat_profile} , 开始吧"
    # ).send()

    node = ChatPostGenNode()
    await node.chat_start()
    cl.user_session.set("chat_agent", node)

    # settings = await cl.ChatSettings(
    #     [
    #         Select(
    #             id="Model",
    #             label="OpenAI - Model",
    #             values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
    #             initial_index=0,
    #         ),
    #         Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
    #         Slider(
    #             id="Temperature",
    #             label="OpenAI - Temperature",
    #             initial=1,
    #             min=0,
    #             max=2,
    #             step=0.1,
    #         ),
    #     ]
    # ).send()


@cl.on_settings_update
async def setup_agent(settings):
    logger.info("on_settings_update", settings)


@cl.on_chat_end
def end():
    logger.info("goodbye %s", cl.user_session.get("id", ""))


@cl.on_message
async def on_message(message: cl.Message):
    # app_user = cl.user_session.get("user")

    chat_agent = cl.user_session.get("chat_agent")
    if chat_agent:
        await chat_agent.on_message(message)
    else:
        logger.error("没有找到聊天代理")
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
