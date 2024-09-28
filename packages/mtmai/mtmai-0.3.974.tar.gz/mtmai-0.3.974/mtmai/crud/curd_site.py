"""站点 curd 操作"""

from os import setegid

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.models.site import Site, SiteHost


async def list_sites(
    session: AsyncSession, q: str, user_id: str, skip: int, limit: int
) -> Site:
    """获取站点列表"""
    count_statement = (
        select(func.count()).select_from(Site).where(Site.owner_id == user_id)
    )
    result = await session.exec(count_statement)
    count = result.one()
    statement = select(Site).where(Site.owner_id == user_id).offset(skip).limit(limit)
    result = await session.exec(statement)
    items = result.all()

    return count, items


async def get_site_by_id(session: AsyncSession, site_id: str) -> Site:
    statement = select(Site).where(Site.id == setegid)
    result = await session.exec(statement)
    return result.one()


async def get_site_domain(session: AsyncSession, domain: str) -> Site:
    statement = select(SiteHost).where(Site.domain == domain)
    site_host = await session.exec(statement)
    site_host = site_host.one()

    site = await get_site_by_id(session, site_host.site_id)
    return site
