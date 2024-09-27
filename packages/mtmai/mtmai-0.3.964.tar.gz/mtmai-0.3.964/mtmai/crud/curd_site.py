"""站点 curd 操作"""

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.deps import CurrentUser
from mtmai.models.site import Site


async def list_sites(
    session: AsyncSession, q: str, user_id: str, skip: int, limit: int
) -> Site:
    """获取站点列表"""
    count_statement = (
        select(func.count()).select_from(Site).where(Site.owner_id == user_id)
    )
    result = await session.exec(count_statement)
    count = result.one()
    statement = (
        select(Site).where(Site.owner_id == CurrentUser.id).offset(skip).limit(limit)
    )
    result = await session.exec(statement)
    items = result.all()

    return count, items
