from fastapi import APIRouter, HTTPException, status

from newsletter_backend.dependencies import CurrentUserDepends, DbSessionDepends
from newsletter_backend.exceptions import HTTPError
from newsletter_backend.schemas.auth_schema import UserRefresh, UserTokens
from newsletter_backend.schemas.user_schema import UserCreate, User, UserLogin
from newsletter_backend.services.auth_service import (
    user_login,
    check_refresh_token,
    user_refresh_session,
)
from newsletter_backend.services.user_service import (
    create_user,
    get_user_by_email,
)
from newsletter_backend.utils.security import check_password


router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"model": HTTPError}},
)
def register(db: DbSessionDepends, user_in: UserCreate) -> User:
    db_user = get_user_by_email(db, user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_in.email} already exists.",
        )

    db_user = create_user(db, user_in)
    user = User.model_validate(db_user)
    return user


@router.post(
    "/login",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
    },
)
def login(db: DbSessionDepends, user_in: UserLogin) -> UserTokens:
    db_user = get_user_by_email(db, user_in.email)
    if not db_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if not check_password(user_in.password, db_user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db_tokens = user_login(db, db_user.id)
    tokens = UserTokens.model_validate(db_tokens)

    return tokens


@router.post(
    "/refresh_session",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": HTTPError},
    },
)
def refresh_session(
    db: DbSessionDepends, current_user: CurrentUserDepends, refresh_in: UserRefresh
) -> UserTokens:
    if not check_refresh_token(db, current_user.id, refresh_in.refresh_token):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Forbidden")

    db_tokens = user_refresh_session(db, current_user.id)
    tokens = UserTokens.model_validate(db_tokens)

    return tokens


@router.get(
    "/me",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
    },
)
def current_user(current_user: CurrentUserDepends) -> User:
    return current_user
