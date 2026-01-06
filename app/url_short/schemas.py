from pydantic import BaseModel, AnyUrl



class ShortenURLRequest(BaseModel):
    original_url: AnyUrl


class ShortenURLResponse(BaseModel):
    short_code: str | None = None


class ShortenURL(BaseModel):
    original_url: AnyUrl
    short_code: str
    owner_id: int | None = None
