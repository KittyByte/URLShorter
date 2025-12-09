from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, class_mapper, mapped_column, Mapped
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.settings import db_settings

engine = create_async_engine(url=db_settings.DATABASE_URL, hide_parameters=True, echo=True)
session_factory = async_sessionmaker(engine)


class BaseOrm(AsyncAttrs, DeclarativeBase):
    # https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#customizing-the-type-map
    type_annotation_map = {
        dict: JSONB
    }

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))  # func.now() он указывает время не по UTC0, а серверное
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))
    # updated_at - делать обновление лучше всего на уровне БД, в Пострес есть триггеры на автообновление записей

    def to_dict(self):
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}

