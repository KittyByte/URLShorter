from fastapi import APIRouter
from fastapi.responses import RedirectResponse, FileResponse
from fastapi import status
from fastapi import Request
from app.url_short.schemas import ShortenURLRequest, ShortenURLResponse
from app.url_short.service import create_short_url, get_url_data_by_code



router = APIRouter(tags=['URL Shortener'])



@router.get('/', name='main_page')
async def main_page():
    return FileResponse('app/static/main.html')


@router.get('/404', name='not_found')
async def not_found():
    return FileResponse('app/static/404.html', status.HTTP_404_NOT_FOUND)


@router.post('/shorten')
async def shorten_url(original_url: ShortenURLRequest) -> ShortenURLResponse:
    short_code = await create_short_url(str(original_url.original_url))
    return {"short_code": short_code}


@router.get('/{short_code}', response_class=RedirectResponse)
async def redirect_url(request: Request, short_code: str):
    url_data = await get_url_data_by_code(short_code)

    if url_data:
        if url_data.owner_id:
            # TODO вызов нотификации о переходе по короткой ссылке и разные другие действия
            ...
        return RedirectResponse(url_data.original_url, status.HTTP_302_FOUND)
    return RedirectResponse(request.url_for('not_found'), status.HTTP_302_FOUND)

