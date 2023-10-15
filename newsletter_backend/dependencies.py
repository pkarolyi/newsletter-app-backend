from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from newsletter_backend.database import db_engine
from newsletter_backend.schemas.user_schema import User
from newsletter_backend.services.auth_service import get_user_by_token


def getSession():
    with Session(db_engine) as session:
        yield session


DbSessionDepends = Annotated[Session, Depends(getSession)]


def get_bearer_session_token(authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        return None

    scheme, token = authorization.split(" ", 1)
    if scheme != "Bearer" or token is None:
        return None

    return token


def get_current_user(
    db: DbSessionDepends, token: Annotated[str, Depends(get_bearer_session_token)]
):
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db_user = get_user_by_token(db, token)
    if not db_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = User.model_validate(db_user)
    return user


CurrentUserDepends = Annotated[User, Depends(get_current_user)]
