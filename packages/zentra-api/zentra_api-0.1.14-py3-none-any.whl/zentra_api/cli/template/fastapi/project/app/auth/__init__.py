from typing import Annotated


from app.auth.response import CreateUserResponse, GetUserDetailsResponse
from app.auth.schema import CreateUser, GetUser, UserBase
from app.core.config import security
from app.core.dependencies import (
    DB_DEPEND,
    OAUTH2_DEPEND,
    OAUTH2_FORM_DEPEND,
)
from app.db_models import CONNECT
from app.db_models.user import DBUser, DBUserDetails

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from zentra_api.schema import Token
from zentra_api.responses import SuccessMsgResponse, exceptions, get_response_models


router = APIRouter(prefix="/auth", tags=["Authentication"])


def authenticate_user(db: Session, username: str, password: str) -> DBUser | bool:
    """Authenticates the user based on its password, assuming it exists and the password is valid. If not, returns `False`."""
    user: DBUser | None = CONNECT.user.get_by_username(db, username)

    if not user:
        return False

    if not security.verify_password(password, user.password):
        return False

    return user


async def get_current_user(token: OAUTH2_DEPEND, db: DB_DEPEND) -> GetUser:
    """Gets the current user based on the given token."""
    username = security.verify_access_token(token)

    user: DBUser = CONNECT.user.get_by_username(db, username)
    details: DBUserDetails = CONNECT.user_details.get(db, user.id)

    return GetUser(
        username=user.username,
        is_active=user.is_active,
        **details.__dict__,
    )


async def get_current_active_user(
    current_user: Annotated[GetUser, Depends(get_current_user)],
) -> GetUser:
    if not current_user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user.")

    return current_user


@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    responses=get_response_models([400, 401]),
    response_model=GetUserDetailsResponse,
)
async def get_user(current_user: Annotated[GetUser, Depends(get_current_active_user)]):
    return GetUserDetailsResponse(
        code=status.HTTP_200_OK,
        data=current_user.model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses=get_response_models(400),
    response_model=CreateUserResponse,
)
async def register_user(user: CreateUser, db: DB_DEPEND):
    exists = CONNECT.user.get_by_username(db, user.username)

    if exists:
        raise exceptions.USER_ALREADY_REGISTERED

    encrypted_user: CreateUser = security.encrypt(user, "password")
    created_user: DBUser = CONNECT.user.create(db, encrypted_user.model_dump())
    CONNECT.user_details.create(db, data={"user_id": created_user.id})
    user_data = UserBase(username=created_user.username)

    return CreateUserResponse(
        code=status.HTTP_201_CREATED,
        data=user_data,
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post(
    "/token",
    status_code=status.HTTP_202_ACCEPTED,
    responses=get_response_models(401),
    response_model=Token,
)
async def login_for_access_token(form_data: OAUTH2_FORM_DEPEND, db: DB_DEPEND):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise exceptions.INVALID_USER_DETAILS

    access_token = security.create_access_token({"sub": user.username})
    refresh_token = security.create_refresh_token({"sub": user.username})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/token/verify/{token}",
    status_code=status.HTTP_200_OK,
    responses=get_response_models(401),
    response_model=SuccessMsgResponse,
)
async def verify_user_token(token: OAUTH2_DEPEND):
    security.verify_access_token(token)
    return SuccessMsgResponse(
        code=status.HTTP_200_OK,
        message="Token is valid.",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post(
    "/token/refresh",
    status_code=status.HTTP_201_CREATED,
    responses=get_response_models(401),
    response_model=Token,
)
async def refresh_access_token(refresh_token: str):
    username = security.verify_refresh_token(refresh_token)

    if not username:
        raise exceptions.INVALID_REFRESH_TOKEN

    access_token = security.create_access_token({"sub": username})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


ACTIVE_USER_DEPEND = Annotated[GetUser, Depends(get_current_active_user)]
