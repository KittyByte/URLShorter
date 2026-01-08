from app.orm.dao import BaseDAO
from app.url_short.models import ShortURLModel


class ShortURLDAO(BaseDAO):
    model = ShortURLModel

