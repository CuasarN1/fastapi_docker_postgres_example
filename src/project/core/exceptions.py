from typing import Final

from fastapi import HTTPException, status


class UserNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "User с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class UserAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Пользователь с почтой '{email}' уже существует"

    def __init__(self, email: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(email=email)
        super().__init__(self.message)


class DatabaseError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Произошла ошибка в базе данных: {message}"

    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)


class CredentialsException(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
