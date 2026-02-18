from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, FileResponse

from app.users.schemas import Token, User, InputRegisterUserData, RegisterResponse
from app.exceptions.user_exceptions import invalid_user_exception
from app.users.service import authenticate_user, create_access_token, create_user
from app.users.dependencies import GetCurrentActiveUserDep

router = APIRouter(
    prefix='/users', tags=['User']
)


@router.post("/token")
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise invalid_user_exception
    access_token = await create_access_token(sub = user.username)
    return Token(access_token=access_token)


@router.get("/me")
async def read_users_me(current_user: GetCurrentActiveUserDep) -> User:
    return current_user


@router.get("/pages/login", response_class=HTMLResponse, summary="Return user login page")
async def html_login_user():
    return FileResponse('app/static/login.html')


@router.get('/pages/register', response_class=HTMLResponse, summary="Return user registration page")
async def html_register_user():
    return FileResponse('app/static/register.html')


@router.post("/register", summary="Create user object")
async def register_user(input_user_data: InputRegisterUserData) -> RegisterResponse:
    if await create_user(input_user_data.username, input_user_data.password):
        access_token = await create_access_token(sub = input_user_data.username)
        return RegisterResponse(token=Token(access_token=access_token))
    return RegisterResponse(success=False, message='User with this username is already exists')
