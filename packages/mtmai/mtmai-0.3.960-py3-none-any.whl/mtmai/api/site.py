from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, func, select

from mtmai.deps import AsyncSessionDep, CurrentUser, SessionDep
from mtmai.models.models import (
    Item,
)
from mtmai.models.site import Site, SiteBase

router = APIRouter()


class SiteItemPublic(SiteBase):
    id: str
    owner_id: str


class ListSiteResponse(SQLModel):
    data: list[SiteItemPublic]
    count: int


@router.get("/", response_model=ListSiteResponse)
def list_sites(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve site items.
    """

    count_statement = (
        select(func.count()).select_from(Site).where(Item.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Site).where(Site.owner_id == current_user.id).offset(skip).limit(limit)
    )
    items = session.exec(statement).all()

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


class SiteCreate(SiteBase):
    pass


@router.post("/", response_model=SiteItemPublic)
def create_Site(
    *, session: SessionDep, current_user: CurrentUser, item_in: SiteCreate
) -> Any:
    """
    Create new site.
    """
    item = Site.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


class SiteUpdate(SiteBase):
    pass


@router.put("/{id}", response_model=SiteItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: str,
    item_in: SiteUpdate,
) -> Any:
    """
    Update an item.
    """
    item = session.get(Site, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
