import bcrypt
import secrets
from datetime import datetime, timedelta

from newsletter_backend.config import app_config
from newsletter_backend.models import ModelUserTokens


def hash_password(plain_password: str):
    password = bytes(plain_password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt).decode("utf-8")


def check_password(plain_password: str, hashed_password: str):
    password = bytes(plain_password, "utf-8")
    h_password = bytes(hashed_password, "utf-8")
    return bcrypt.checkpw(password, h_password)


def generate_tokens(user_id: int):
    session_token = secrets.token_urlsafe(app_config.session_token_length)
    session_expiry = datetime.utcnow() + timedelta(minutes=app_config.session_exp_min)
    refresh_token = secrets.token_urlsafe(app_config.refresh_token_length)
    refresh_expiry = datetime.utcnow() + timedelta(days=app_config.refresh_exp_day)

    tokens = ModelUserTokens(
        user_id=user_id,
        session_token=session_token,
        session_expiry=session_expiry,
        refresh_token=refresh_token,
        refresh_expiry=refresh_expiry,
    )

    return tokens
