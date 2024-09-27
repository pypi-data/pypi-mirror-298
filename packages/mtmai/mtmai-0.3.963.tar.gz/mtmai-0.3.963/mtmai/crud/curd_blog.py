"""博客系统的 curd 操作"""

from pydantic import BaseModel
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.llm.embedding import embedding_hf
from mtmai.models.blog import Post, PostBase, PostContent, TaggedItem
from mtmai.models.models import Document, DocumentIndex
from mtmai.models.search_index import SearchIndex
from sqlmodel import func, select



class PostCreate(PostBase):
    content: str


async def create_blog_post(
    *, session: AsyncSession, blog_post_create: PostCreate
) -> Post:
    """
    改进1：
        embedding 应该用独立的方式进行，因为调用 embedding_hf 可能失败

    """

    input_data = PostCreate.model_validate(blog_post_create)

    # Create Post
    new_blog_post = Post(title=input_data.title)
    session.add(new_blog_post)

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