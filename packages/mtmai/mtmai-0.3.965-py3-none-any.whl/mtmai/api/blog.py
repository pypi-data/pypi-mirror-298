"""
博客系统api
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from mtmai.core.db import get_session
from mtmai.crud.curd_blog import create_blog_post
from mtmai.deps import AsyncSessionDep
from mtmai.models.blog import (
    BlogPostCreateReq,
    BlogPostCreateRes,
    BlogPostDetailResponse,
    BlogPostItem,
    BlogPostListResponse,
    BlogPostUpdateReq,
    BlogPostUpdateRes,
    Post,
    PostContent,
    Tag,
    TaggedItem,
)
from mtmai.models.models import Document

router = APIRouter()


@router.get("/posts", response_model=BlogPostListResponse)
async def post_list(
    *,
    db: Session = Depends(get_session),
    query: str = Query(default=""),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    if query:
        # 如果有查询字符串，执行向量搜索
        vector_search_query = (
            select(Document.id)
            .order_by(Document.embedding.l2_distance(query))
            .limit(limit * 2)
        )
        relevant_doc_ids = db.exec(vector_search_query).all()

        # 然后使用这些ID来获取完整的博客文章信息
        joined_query = (
            select(Document, Post)
            .join(Post, Document.id == Post.doc_id)
            .where(Document.id.in_(relevant_doc_ids))
            .offset(offset)
            .limit(limit)
        )
    else:
        # 如果没有查询字符串，返回最新的博客文章
        joined_query = (
            select(Post, PostContent)
            .join(PostContent, Post.id == PostContent.post_id)
            .order_by(Post.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

    results = db.exec(joined_query).all()

    posts = [
        BlogPostItem(
            id=post.id,
            title=post.title or "",
            content=doc.content or "",
            slug=post.slug,
        )
        for post, doc in results
    ]

    return BlogPostListResponse(data=posts, count=len(posts))


@router.post("/", response_model=BlogPostCreateRes)
async def post_create(
    *,
    db: AsyncSessionDep,
    req: BlogPostCreateReq,
):
    return await create_blog_post(session=db, blog_post_create=req)


@router.put("/{post_id}", response_model=BlogPostUpdateRes)
async def blog_post_update(
    *,
    post_id: str,
    db: Session = Depends(get_session),
    req: BlogPostUpdateReq,
):
    blog_post = db.exec(select(Post).where(Post.id == post_id)).one()
    if not blog_post:
        raise HTTPException(status_code=404)
    # Update slug if changed
    if req.slug != blog_post.slug:
        existing_post = await db.exec(select(Post).where(Post.slug == req.slug)).first()
        if existing_post:
            raise HTTPException(status_code=400, detail="Slug already exists")
        blog_post.slug = req.slug
    blog_post.title = req.title

    # 更新内容
    if blog_post.content_id:
        blog_post_content = db.exec(
            select(Document).where(Document.id == blog_post.content_id)
        ).one_or_none()
    else:
        blog_post_content = None

    if not blog_post_content:
        blog_post_content = Document(content=req.content)
        db.add(blog_post_content)
        db.commit()
        db.refresh(blog_post_content)
        blog_post.content_id = blog_post_content.id
    else:
        blog_post_content.content = req.content

    db.add(blog_post)
    db.add(blog_post_content)
    db.commit()
    return BlogPostUpdateRes(id=blog_post.id)


@router.get("/{slug}", response_model=BlogPostDetailResponse)
async def get_post_by_slug(
    *,
    slug: str,
    db: AsyncSessionDep,
):
    """获取 Post 详细完整信息"""
    # Change the function parameter to accept a slug instead of post_id
    # slug = slug.replace('-', ' ')  # Convert slug to title-like string

    # Query the post by slug (which is derived from the title)
    a = await db.exec(select(Post).where(Post.slug == slug))
    blog_post = a.one_or_none()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Query the post content
    a = await db.exec(
        select(PostContent).where(PostContent.post_id == blog_post.id)
    )
    blog_post_content = a.one_or_none()
    if not blog_post_content:
        raise HTTPException(status_code=404, detail="Post content not found")

    # Query tags for the post
    tags_query = (
        select(Tag)
        .join(TaggedItem)
        .where((TaggedItem.item_id == blog_post.id) & (TaggedItem.item_type == "post"))
    )
    tags = (await db.exec(tags_query)).all()

    return BlogPostDetailResponse(
        id=str(blog_post.id),
        title=blog_post.title,
        content=blog_post_content.content,
        tags=[tag.name for tag in tags],
        created_at=blog_post.created_at,
        updated_at=blog_post.updated_at,
        author=blog_post.author,
    )
