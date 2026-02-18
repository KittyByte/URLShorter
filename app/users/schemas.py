from pydantic import BaseModel, Field
from datetime import datetime
from app.common.shemas import SuccessResponse


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str
    exp: datetime


class User(BaseModel):
    username: str
    fullname: str | None = None
    email: str | None = None
    disabled: bool


class UserInDB(User):
    id: int
    hashed_password: str = Field(validation_alias='password')


class InputRegisterUserData(BaseModel):
    username: str
    password: str


class RegisterResponse(SuccessResponse):
    token: Token | None = None

