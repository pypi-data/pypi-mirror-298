"""博客系统的 curd 操作"""

import random
import string

from pydantic import BaseModel
from slugify import slugify
from sqlmodel import Session, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.llm.embedding import embedding_hf
from mtmai.models.blog import BlogPostCreateReq, Post, PostContent, Tag, TaggedItem
from mtmai.models.models import Document, DocumentIndex
from mtmai.models.search_index import SearchIndex
from mtmai.mtlibs.html.htmlUtils import extract_title_from_html


async def create_blog_post(
    *, session: AsyncSession, blog_post_create: BlogPostCreateReq
) -> Post:
    """
    改进1：
        embedding 应该用独立的方式进行，因为调用 embedding_hf 可能失败

    """
    input_data = BlogPostCreateReq.model_validate(blog_post_create)

    if not input_data.title:
        input_data.title = extract_title_from_html(input_data.content)
    if not input_data.title:
        input_data.title = "untitled"
    # 处理 slug
    base_slug = slugify(input_data.title)
    slug = base_slug
    while True:
        existing_post = await session.exec(select(Post).where(Post.slug == slug))
        if existing_post.first() is None:
            break
        # 如果 slug 已存在，添加随机字符串
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        slug = f"{base_slug}-{random_string}"
    # Create Post
    new_blog_post = Post(
        title=input_data.title,
        slug=slug,
    )

    session.add(new_blog_post)

    # 处理 tags
    if input_data.tags:
        for tag_name in input_data.tags:
            # Check if the tag already exists
            result = await session.exec(select(Tag).where(Tag.name == tag_name))
            existing_tag = result.first()
            if not existing_tag:
                # If the tag doesn't exist, create a new one
                existing_tag = Tag(name=tag_name)
                session.add(existing_tag)

            # Create a TaggedItem to link the post and the tag
            tagged_item = TaggedItem(
                tag_id=existing_tag.id, item_id=new_blog_post.id, item_type="post"
            )
            session.add(tagged_item)

    post_content = PostContent(post_id=new_blog_post.id, content=input_data.content)
    session.add(post_content)

    search_index = SearchIndex(
        content_type="post",
        content_id=new_blog_post.id,
        title=new_blog_post.title,
        meta={
            # "author_id": str(new_blog_post.author_id),
            # "tags": [tag.name for tag in new_blog_post.tags],
        },
        # search_vector=generate_search_vector(post.title, post.content),
        # embedding=generate_embedding(post.title, post.content)
    )
    session.add(search_index)

    await session.commit()
    await session.refresh(new_blog_post)
    return new_blog_post


class DocumentQueryReq(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0


async def document_query(session: Session, req: DocumentQueryReq) -> list[Document]:
    embedding_result = await embedding_hf(inputs=[req.query])
    query = (
        select(Document)
        .join(DocumentIndex, Document.id == DocumentIndex.document_id)
        .order_by(DocumentIndex.embedding.l2_distance(embedding_result[0]))
        .offset(req.offset)
        .limit(req.limit)
    )
    result = session.exec(query).all()
    return result


# async def get_post_detail(*, session: AsyncSession,post_id:str):
#     blog_post = await session.exec(select(Post).where(Post.id == post_id)).one_or_none()
#     if not blog_post:
#         raise HTTPException(status_code=404, detail="Post not found")

#     blog_post_content = await .exec(
#         select(Document).where(Document.id == blog_post.doc_id)
#     ).one_or_none()
#     # if not blog_post_content:
#     #     raise HTTPException(status_code=404, detail="Post content not found")

#     return BlogPostDetailResponse(
#         id=blog_post.id,
#         title=blog_post.title,
#         content=blog_post_content.content,
#         tags=[],  # Assuming tags are not implemented yet
#         author_id=None,  # Assuming author details are not implemented yet
#         author_avatar=None,
#     )


async def get_related_posts(db: AsyncSession, current_post: Post, limit: int = 5):
    """
    获取相关文章(未完成)
    """
    # 获取当前文章的标签
    current_tags = [tag.id for tag in current_post.tags]

    related_posts = (
        await db.query(Post)
        .join(TaggedItem)
        .filter(Post.id != current_post.id)  # 排除当前文章
        .filter(TaggedItem.tag_id.in_(current_tags))  # 匹配标签
        .group_by(Post.id)
        .order_by(func.count(TaggedItem.tag_id).desc())  # 按共享标签数量排序
        .limit(limit)
        .all()
    )
    return related_posts
