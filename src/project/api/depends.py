from typing import Annotated

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status

from project.schemas.auth import TokenData
from project.schemas.user import UserSchema
from project.core.config import settings
from project.core.exceptions import CredentialsException
from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.resource.auth import oauth2_scheme


user_repo = UserRepository()
database = PostgresDatabase()

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные для авторизации"


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

    async with database.session() as session:
        user = await user_repo.get_user_by_email(
            session=session,
            email=token_data.username,
        )

    if user is None:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

    return user


def check_for_admin_access(user: UserSchema) -> None:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только админ имеет права добавлять/изменять/удалять пользователей"
        )

