from fastapi import APIRouter

import mtmai.chainlit as cl
import mtmai.chainlit.data as cl_data
from mtmai.agents.chat_profiles.chat_post_gen import PostGenAgent
from mtmai.agents.chat_profiles.profiles import (
    get_all_profiles,
    get_default_chat_profile,
)
from mtmai.core.logging import get_logger
from mtmai.models.models import User
from mtmai.mtlibs.chainlit.data_layer import SQLAlchemyDataLayer

# 使用自定义的 sql 存储chainlit数据
cl_data._data_layer = SQLAlchemyDataLayer()

router = APIRouter()
logger = get_logger()


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

    node = PostGenAgent()
    await node.chat_start()
    cl.user_session.set("chat_agent", node)


@cl.on_settings_update
async def setup_agent(settings):
    logger.info("on_settings_update", settings)


@cl.on_chat_end
def end():
    logger.info("goodbye %s", cl.user_session.get("id", ""))


@cl.on_message
async def on_message(message: cl.Message):
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
