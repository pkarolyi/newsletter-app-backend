from sqlalchemy import select
from sqlalchemy.orm import Session

from newsletter_backend.models import ModelUser
from newsletter_backend.schemas.user_schema import UserCreate
from newsletter_backend.utils.security import hash_password


def create_user(db: Session, user_data: UserCreate):
    db_user = ModelUser(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, id: int):
    db_user = db.get(ModelUser, id)
    return db_user


def get_user_by_email(db: Session, email: str):
    db_user = db.scalar(select(ModelUser).where(ModelUser.email == email))
    return db_user
