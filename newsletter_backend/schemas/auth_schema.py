from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserTokens(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_token: str
    session_expiry: datetime
    refresh_token: str
    refresh_expiry: datetime


class UserRefresh(BaseModel):
    refresh_token: str
