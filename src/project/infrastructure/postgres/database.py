from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

from sqlalchemy import JSON, MetaData, String
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from project.core.config import settings
from project.core.exceptions import DatabaseError


class PostgresDatabase:
    def __init__(self) -> None:
        self._engine = create_async_engine(settings.postgres_url)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except (Exception, PendingRollbackError) as error:
                await session.rollback()
                raise DatabaseError(message=repr(error))


database = PostgresDatabase()
metadata = MetaData(schema=settings.POSTGRES_SCHEMA)


class Base(DeclarativeBase):
    metadata = metadata
    type_annotation_map = {str: String().with_variant(String(255), "postgresql"), Dict[str, Any]: JSON}
