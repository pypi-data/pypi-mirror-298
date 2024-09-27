"""
博客系统api
"""

from typing import Union

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from mtmai.auth import get_current_user
from mtmai.chainlit.config import (
    config,
)
from mtmai.chainlit.data import get_data_layer
from mtmai.chainlit.markdown import get_markdown_str
from mtmai.chainlit.types import GetThreadsRequest
from mtmai.chainlit.user import PersistedUser, User
from mtmai.crud import curd_chat
from mtmai.deps import AsyncSessionDep, CurrentUser

router = APIRouter()
_language_pattern = (
    "^[a-zA-Z]{2,3}(-[a-zA-Z]{2,3})?(-[a-zA-Z]{2,8})?(-x-[a-zA-Z0-9]{1,8})?$"
)


@router.post("/threads")
async def get_user_threads(
    req: GetThreadsRequest,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """Get the threads page by page."""
    # payload.filter.userId = current_user.id

    user_threads = await curd_chat.get_user_threads(
        session,
        current_user.id,
        # thread_id=req.filter.therad_id,
        limit=limit,
        skip=skip,
    )
    return user_threads


@router.get("/settings")
async def project_settings(
    current_user: Annotated[Union[User, PersistedUser], Depends(get_current_user)],
    language: str = Query(
        default="en-US", description="Language code", pattern=_language_pattern
    ),
):
    """Return project settings. This is called by the UI before the establishing the websocket connection."""

    # Load the markdown file based on the provided language

    markdown = get_markdown_str(config.root, language)

    profiles = []
    if config.code.set_chat_profiles:
        chat_profiles = await config.code.set_chat_profiles(current_user)
        if chat_profiles:
            profiles = [p.to_dict() for p in chat_profiles]

    starters = []
    if config.code.set_starters:
        starters = await config.code.set_starters(current_user)
        if starters:
            starters = [s.to_dict() for s in starters]

    if config.code.on_audio_chunk:
        config.features.audio.enabled = True

    debug_url = None
    data_layer = get_data_layer()

    if data_layer and config.run.debug:
        debug_url = await data_layer.build_debug_url()

    data_resonse = {
        "ui": config.ui.to_dict(),
        "features": config.features.to_dict(),
        "userEnv": config.project.user_env,
        "dataPersistence": get_data_layer() is not None,
        "threadResumable": bool(config.code.on_chat_resume),
        "markdown": markdown,
        "chatProfiles": profiles,
        "starters": starters,
        "debugUrl": debug_url,
    }
    return JSONResponse(content=data_resonse)
