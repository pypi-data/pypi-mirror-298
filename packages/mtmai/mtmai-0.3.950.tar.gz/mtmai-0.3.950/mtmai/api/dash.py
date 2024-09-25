import logging

from fastapi import APIRouter

from mtmai.models.dash import CmdkItem, DashConfig
from mtmai.models.models import DocCollsPublic

router = APIRouter()

logger = logging.getLogger()


@router.get("/config", response_model=DashConfig)
async def config(
    # db: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    """获取后台配置"""
    dashConfig = DashConfig(
        navMenus=[
            {
                "title": "chat",
                "icon": "MessageSquare",
                "variant": "ghost",
                "url": "/chat",
            },
            {
                "title": "thread",
                "icon": "thread",
                "variant": "ghost",
                "url": "/thread",
            },
            {
                "title": "站点",
                "icon": "site",
                "variant": "ghost",
                "url": "/site",
            },
            {
                "title": "settings",
                "icon": "settings",
                "variant": "ghost",
                "url": "/settings",
            },
        ]
    )
    return dashConfig


@router.get("/user_menus", response_model=DocCollsPublic)
async def user_menus(
    # db: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    """获取用户菜单"""
    user_cmdks = [
        CmdkItem(label="数据管理", icon="", url=""),
        CmdkItem(label="settings", icon="settings", url=""),
        CmdkItem(label="退出", icon="logout", url=""),
    ]
    return user_cmdks
