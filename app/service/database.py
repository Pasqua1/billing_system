from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


from app.config import settings

DATABASE_URL = settings.DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(
    engine, class_ = AsyncSession,
    expire_on_commit = False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
