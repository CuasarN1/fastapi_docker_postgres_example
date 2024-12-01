from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, PendingRollbackError, InterfaceError

from project.schemas.user import UserSchema, UserCreateUpdateSchema
from project.infrastructure.postgres.models import User

from project.core.exceptions import UserNotFound, UserAlreadyExists


class UserRepository:
    _collection: Type[User] = User

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.email == email)
        )

        user = await session.scalar(query)

        if not user:
            raise UserNotFound(_id=email)

        return UserSchema.model_validate(obj=user)

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = select(self._collection)

        users = await session.scalars(query)

        return [UserSchema.model_validate(obj=user) for user in users.all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == user_id)
        )

        user = await session.scalar(query)

        if not user:
            raise UserNotFound(_id=user_id)

        return UserSchema.model_validate(obj=user)

    async def create_user(
        self,
        session: AsyncSession,
        user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            insert(self._collection)
            .values(user.model_dump())
            .returning(self._collection)
        )

        try:
            created_user = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise UserAlreadyExists(email=user.email)

        return UserSchema.model_validate(obj=created_user)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == user_id)
            .values(user.model_dump())
            .returning(self._collection)
        )

        updated_user = await session.scalar(query)

        if not updated_user:
            raise UserNotFound(_id=user_id)

        return UserSchema.model_validate(obj=updated_user)

    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == user_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise UserNotFound(_id=user_id)
