from datetime import datetime
import uuid

from sqlmodel import Field, SQLModel

from mtmai.mtlibs import mtutils


class SiteHostBase(SQLModel):
    domain: str = Field(min_length=3, max_length=255)
    is_default: bool = Field(default=False)
    is_https: bool = Field(default=False)
    site_id: uuid.UUID = Field(foreign_key="site.id", nullable=False, ondelete="CASCADE")

class SiteHost(SiteHostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)



class SiteBase(SQLModel):
    """
    站点基础配置
        1: 站点标题
        2: 站点域名
        3: 站点描述: 决定了 agent 如何自动采集文章和生成文章
        4: 站点关键词: 决定了 agent 如何自动采集文章和生成文章
        5: 站点作者
        6: 站点版权
        7: 站点创建时间
        8: 站点更新时间
    """

    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    keywords: str | None = Field(default=None, max_length=255)
    author: str | None = Field(default=None, max_length=255)
    copyright: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default=datetime.now())
    owner_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")



# Database model, database table inferred from class name
class Site(SiteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    updated_at: datetime = Field(default=datetime.now())


class SiteCreateRequest(SiteBase):
    owner_id: str|None=None



class SiteUpdateRequest(SiteBase):
    owner_id: str|None=None



class SiteItemPublic(SiteBase):
    id: uuid.UUID
    owner_id: str|None=None


class ListSiteResponse(SQLModel):
    data: list[SiteItemPublic]
    count: int



class ListSiteHostRequest(SQLModel):
    siteId: uuid.UUID
    q: str|None=Field(default=None,max_length=255)

class SiteHostItemPublic(SiteHostBase):
    id: uuid.UUID

class ListSiteHostsResponse(SQLModel):
    data: list[SiteHostItemPublic]
    count: int

class SiteHostCreateRequest(SiteHostBase):
    site_id: uuid.UUID

class SiteHostCreateResponse(SQLModel):
    id: uuid.UUID

class SiteHostUpdateRequest(SiteHostBase):
    id: uuid.UUID
    host: str = Field(min_length=3, max_length=255)

class SiteHostUpdateResponse(SQLModel):
    id: uuid.UUID

class SiteHostDeleteRequest (SQLModel):
    id: uuid.UUID

class SiteHostDeleteResponse(SQLModel):
    id: uuid.UUID