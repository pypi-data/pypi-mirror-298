import uuid

from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlmodel import Column, Field, SQLModel


class SearchIndexBase(SQLModel):
    type: str = Field(index=True)
    data_type: str = Field(index=True)
    title: str
    content: str


class SearchIndex(SearchIndexBase, table=True):
    __tablename__ = "search_index"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID | None = Field(default=None, index=True)
    is_public: bool = Field(default=True, index=True)
    search_vector: str = Field(sa_column=Column(TSVECTOR))


class SearchIndexPublic(SearchIndexBase):
    pass


class SearchIndexResponse(SQLModel):
    data: list[SearchIndexPublic]
    count: int


class SearchRequest(SQLModel):
    dataType: str | None = None
    q: str | None = None  # 搜索关键词
    limit: int = 100
    skip: int = 0
