import logging

from psycopg_pool import AsyncConnectionPool
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import settings
from mtmai.core.db import get_async_session
from mtmai.crud.crud import create_user, get_user_by_email
from mtmai.models.models import UserCreate

logger = logging.getLogger()


async def _seed_users(db: AsyncSession):
    # count = db.exec(select(func.count()).select_from(Agent)).one()
    # if count > 0:
    #     return

    super_user = await get_user_by_email(
        session=db, email=settings.FIRST_SUPERUSER_EMAIL
    )
    if not super_user:
        create_user(
            session=db,
            user_create=UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            ),
        )


async def seed_db(session: AsyncSession):
    await _seed_users(session)


async def setup_checkpointer():
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    logger.info("database connecting ...")
    await pool.open()
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()
    await pool.close()


async def init_database():
    """初始化数据库
    确保在空数据库的情况下能启动系统
    """
    logger.warning("⚠️ ⚠️ ⚠️ SEDDING DB  ⚠️ ⚠️⚠️")

    # engine = getdb()

    # try:
    #     with engine.connect() as connection:
    #         connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    #         # connection.execute(text("CREATE EXTENSION IF NOT EXISTS pgmq;"))
    #         connection.commit()
    # except Exception:
    #     logger.exception("error create postgresql extensions ")

    # SQLModel.metadata.create_all(engine)
    # async with AsyncSession(engine) as session:
    async with get_async_session() as session:
        await seed_db(session)

    await setup_checkpointer()
    logger.info("🟢 Seeding database finished")
