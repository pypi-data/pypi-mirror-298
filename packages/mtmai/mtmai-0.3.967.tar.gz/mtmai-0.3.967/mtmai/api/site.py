from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from mtmai.deps import AsyncSessionDep, CurrentUser, OptionalUserDep
from mtmai.models.models import (
    Item,
)
from mtmai.models.site import (
    ListSiteHostsResponse,
    ListSiteResponse,
    Site,
    SiteCreateRequest,
    SiteHost,
    SiteItemPublic,
    SiteUpdateRequest,
)

router = APIRouter()


@router.get("/", response_model=ListSiteResponse)
async def list_sites(
    session: AsyncSessionDep, current_user: OptionalUserDep
) -> Any:
    """
    Retrieve site items.
    """

    count_statement = (
        select(func.count()).select_from(Site).where(Item.owner_id == current_user.id)
    )
    a = await session.exec(count_statement)
    count = a.one()
    statement = (
        select(Site).where(Site.owner_id == current_user.id)#.offset(skip).limit(limit)
    )
    r = await session.exec(statement)
    items = r.all()

    return ListSiteResponse(data=items, count=count)


@router.get("/{id}", response_model=SiteItemPublic)
async def get_site(session: AsyncSessionDep, current_user: CurrentUser, id: str) -> Any:
    """
    Get item by ID.
    """
    item = await session.get(Site, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/", response_model=SiteItemPublic)
async def create_Site(
    *, session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest
) -> Any:
    """
    Create new site.
    """
    item = Site.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{id}", response_model=SiteItemPublic)
async def update_item(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    id: str,
    item_in: SiteUpdateRequest,
) -> Any:
    """
    Update an item.
    """
    item = await session.get(Site, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.get("/hosts", response_model=ListSiteHostsResponse)
async def list_site_hosts(
    session: AsyncSessionDep, current_user: OptionalUserDep
) -> Any:
    """
    Retrieve site hosts.
    """
    count_statement = (
        select(func.count()).select_from(SiteHost).where(Item.owner_id == current_user.id)
    )
    a = await session.exec(count_statement)
    count = a.one()
    statement = (
        select(SiteHost).where(Site.owner_id == current_user.id)#.offset(skip).limit(limit)
    )
    r = await session.exec(statement)
    items = r.all()

    return ListSiteHostsResponse(data=items, count=count)
