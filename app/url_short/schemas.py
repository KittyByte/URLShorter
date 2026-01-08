from pydantic import BaseModel, AnyUrl
from datetime import datetime


class ShortenURLRequest(BaseModel):
    original_url: AnyUrl


class ShortenURLResponse(BaseModel):
    short_code: str | None = None


class URLShortDB(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    original_url: AnyUrl
    short_code: str
    owner_id: int | None = None


class URLShortRedis(BaseModel):
    id: int
    original_url: AnyUrl
    short_code: str
    owner_id: int | None = None

    model_config = {'extra': 'ignore'}

