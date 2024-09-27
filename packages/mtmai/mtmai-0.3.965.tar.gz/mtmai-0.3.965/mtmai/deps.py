from collections.abc import Generator
from typing import Annotated, AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from pydantic import ValidationError
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core import security
from mtmai.core.config import settings
from mtmai.core.db import engine, get_async_engine, get_checkpointer
from mtmai.models.models import TokenPayload, User
from mtmai.mtlibs.mq.pq_queue import AsyncPGMQueue

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,  # 没有 token header 时不触发异常
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


async def get_asession() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(get_async_engine()) as session:
        yield session


async def get_mq():
    queue = await AsyncPGMQueue.create(settings.DATABASE_URL)
    yield queue


SessionDep = Annotated[Session, Depends(get_db)]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_asession)]


TokenDep = Annotated[str, Depends(reusable_oauth2)]
MqDep = Annotated[str, Depends(get_mq)]


def get_host_from_request(request: Request) -> str:
    host = request.headers.get("Host")
    return host


HostDep = Annotated[str, Depends(get_host_from_request)]


def get_current_user(session: SessionDep, token: TokenDep, request: Request) -> User:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_optional_current_user(
    session: SessionDep, token: TokenDep, request: Request
) -> User | None:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    if not token:
        return None
    try:
        return get_current_user(session, token, request)
    except HTTPException:
        return None


OptionalUserDep = Annotated[User | None, Depends(get_optional_current_user)]


CheckPointerDep = Annotated[AsyncPostgresSaver, Depends(get_checkpointer)]


# def get_crawl_worker(
#     mq: Annotated[AsyncPGMQueue, Depends(get_mq)], db: SessionDep
# ) -> CrawlWorker:
#     return CrawlWorker(mq=mq, db=db)


# CrawlWorkerDep = Annotated[CrawlWorker, Depends(get_crawl_worker)]
