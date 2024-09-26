import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel


class TaggedItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id")
    item_id: uuid.UUID
    item_type: str

class Tag(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    # posts: list["Post"] = Relationship(back_populates="tags", link_model="PostTagLink")
    # posts: list["Post"] = Relationship(back_populates="tags", link_model=TaggedItem)
    # videos: list["Video"] = Relationship(back_populates="tags", link_model=TaggedItem)




# class PostTagLink(SQLModel, table=True):
#     post_id: uuid.UUID = Field(foreign_key="post.id", primary_key=True)
#     tag_id: uuid.UUID = Field(foreign_key="tag.id", primary_key=True)


class PostTabBase(SQLModel):
    name: str | None = Field(default=None)


class PostTab(PostTabBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PostBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    author: str | None = Field(default=None)
    # content: str | None = Field(default=None)


class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # tags: list[Tag] = Relationship(back_populates="posts", link_model=TaggedItem)
    # tags: list[Tag] = Relationship(
    #     back_populates="posts",
    #     link_model=TaggedItem,
    #     sa_relationship_kwargs={
    #         'primaryjoin': 'and_(TaggedItem.item_id == Post.id, TaggedItem.item_type == "post")',
    #         'secondaryjoin': 'Tag.id == TaggedItem.tag_id'
    #     }
    # )

    # doc_id: uuid.UUID | None = Field(default=None)
    # tags: list[Tag] = Relationship(back_populates="posts", link_model=PostTagLink)


class BlogPostItem(PostBase):
    id: uuid.UUID


class BlogPostListResponse(SQLModel):
    data: list[BlogPostItem]
    count: int


class BlogPostCreateReq(SQLModel):
    title: str
    content: str
    tags: list[str] = []


class BlogPostCreateRes(SQLModel):
    id: uuid.UUID


class BlogPostUpdateReq(SQLModel):
    title: str
    content: str


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
    # tags: list[Tag] = Relationship(back_populates="videos", link_model=TaggedItem)
    # tags: list[Tag] = Relationship(
    #     back_populates="videos",
    #     link_model=TaggedItem,
    #     sa_relationship_kwargs={
    #         'primaryjoin': 'and_(TaggedItem.item_id == Video.id, TaggedItem.item_type == "video")',
    #         'secondaryjoin': 'Tag.id == TaggedItem.tag_id'
    #     }
    # )

