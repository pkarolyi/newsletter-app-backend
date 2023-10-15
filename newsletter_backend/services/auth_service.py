import hmac
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from newsletter_backend.models import ModelUser, ModelUserTokens
from newsletter_backend.utils.security import generate_tokens


def user_login(db: Session, user_id: int):
    db_tokens = generate_tokens(user_id)

    db.query(ModelUserTokens).filter(ModelUserTokens.user_id == user_id).delete()
    db.add(db_tokens)
    db.commit()
    db.refresh(db_tokens)

    return db_tokens


def check_refresh_token(db: Session, user_id: int, refresh_token: str):
    db_tokens = (
        db.query(ModelUserTokens).filter(ModelUserTokens.user_id == user_id).first()
    )

    if not db_tokens:
        return False

    if db_tokens.refresh_expiry.timestamp() < datetime.utcnow().timestamp():
        return False

    if not hmac.compare_digest(db_tokens.refresh_token, refresh_token):
        return False

    return True


def user_refresh_session(db: Session, user_id: int):
    db_tokens = generate_tokens(user_id)

    db.query(ModelUserTokens).filter(ModelUserTokens.user_id == user_id).delete()
    db.add(db_tokens)
    db.commit()
    db.refresh(db_tokens)

    return db_tokens


def get_user_by_token(db: Session, token: str):
    db_user = db.scalar(
        select(ModelUser)
        .join(ModelUserTokens, ModelUser.id == ModelUserTokens.user_id)
        .where(ModelUserTokens.session_token == token)
    )
    return db_user
