from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import AppSettings

engine = create_engine(AppSettings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
