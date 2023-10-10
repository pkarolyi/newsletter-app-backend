from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete

from .models import User
from .database import getSession

app = FastAPI()


@app.get("/")
async def root(db: Annotated[Session, Depends(getSession)]):
    users = db.scalars(select(User)).all()
    return {"users": users}
