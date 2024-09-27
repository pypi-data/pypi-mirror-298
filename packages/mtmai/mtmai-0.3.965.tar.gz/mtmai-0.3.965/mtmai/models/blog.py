import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class TaggedItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id")
    item_id: uuid.UUID
    item_type: str


class Tag(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)


class PostTabBase(SQLModel):
    name: str | None = Field(default=None)


class PostTab(PostTabBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PostBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    slug: str = Field(index=True, unique=True)  # Add this line

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    author: str | None = Field(default=None)
    # content: str | None = Field(default=None)


class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class BlogPostItem(PostBase):
    id: uuid.UUID


class BlogPostListResponse(SQLModel):
    data: list[BlogPostItem]
    count: int


class BlogPostCreateReq(SQLModel):
    content: str
    title: str | None = None
    tags: list[str] = []
    slug: str | None = None


class BlogPostCreateRes(SQLModel):
    id: uuid.UUID


class BlogPostUpdateReq(SQLModel):
    title: str
    content: str
    slug: str  # Add this line


class BlogPostUpdateRes(SQLModel):
    id: str


class BlogPostDetailResponse(SQLModel):
    id: str
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    author: str | None


class PostContent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="post.id", unique=True, ondelete="CASCADE")
    content: str = Field(default=None)  # Full content


# 练习 tags 与 vedio 的关系
class VideoBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    url: str
    duration: int  # in seconds
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    author: str | None = Field(default=None)


class Video(VideoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
