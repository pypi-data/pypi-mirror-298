"""
为前端，以 openapi 的方式生成类型

"""

from pydantic import BaseModel

from mtmai.core.config import settings


class BotConfig(BaseModel):
    """mtmaibot 配置"""

    baseUrl: str | None = None
    apiPrefix: str | None = settings.API_V1_STR
    accessToken: str | None = None
    loginUrl: str = "/auth/login"
