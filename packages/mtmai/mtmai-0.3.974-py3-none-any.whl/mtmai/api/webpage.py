import logging

from fastapi import APIRouter, Query

from mtmai.deps import AsyncSessionDep, SiteDep
from mtmai.models.webpage import PageMetaAuthor, PageMetaResponse

router = APIRouter()

logger = logging.getLogger()


@router.get("/page_meta", response_model=PageMetaResponse)
async def page_meta(
    *,
    session: AsyncSessionDep,
    # siteId: uuid.UUID|None=None,
    query: str = Query(default=""),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    site: SiteDep,
):
    return PageMetaResponse(
        title="test_page_meta",
        description="test_page_meta",
        keywords=["test_page_meta"],
        authors=[PageMetaAuthor(name="test_page_meta", url="test_page_meta")],
        creator="test_page_meta",
        manifest="test_page_meta",
    )
