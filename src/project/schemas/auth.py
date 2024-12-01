from pydantic import BaseModel, Field


class AuthCredential(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = Field(default=None)
