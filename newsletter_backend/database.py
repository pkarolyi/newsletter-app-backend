from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from .config import app_config

db_engine = create_engine(app_config.database_url)


class ModelBase(DeclarativeBase):
    pass
