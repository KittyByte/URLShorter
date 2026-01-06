from fastapi import APIRouter
from fastapi.responses import RedirectResponse, ORJSONResponse
from app.url_short.schemas import ShortenURLRequest, ShortenURLResponse
from app.url_short.service import create_short_url, get_url_data_by_code



router = APIRouter(tags=['URL Shortener'])


@router.post('/shorten')
async def shorten_url(original_url: ShortenURLRequest) -> ShortenURLResponse:
    short_code = await create_short_url(str(original_url.original_url))
    return {"short_code": short_code}


@router.get('/{short_code}')
async def redirect_url(short_code: str):
    url_data = await get_url_data_by_code(short_code)

    if url_data:
        return RedirectResponse(url=url_data.original_url)
    return ORJSONResponse(status_code=404, content={"detail": "URL not found"})

