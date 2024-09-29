from mtmai.models.chat import ChatProfile


async def get_all_profiles():
    all_profiles = [
        ChatProfile(
            name="GPT-3.5",
            default=True,
            description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
        ),
        ChatProfile(
            name="postGen",
            default=True,
            description="博客文章生成器",
        ),
    ]
    return all_profiles


async def get_default_chat_profile():
    return next(
        (profile for profile in await get_all_profiles() if profile.default), None
    )
