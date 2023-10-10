from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .config import AppSettings

engine = create_engine(AppSettings().database_url)


def getSession():
    with Session(engine) as session:
        yield session
