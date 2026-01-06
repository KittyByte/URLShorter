from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseOrm



class ShortURLModel(BaseOrm):
    __tablename__ = "short_url"

    original_url: Mapped[str]
    short_code: Mapped[str] = mapped_column(String(10), unique=True)
    owner_id: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Table: ShortURL(id={self.id!r}, original_url={self.original_url!r}, "
            f"short_code={self.short_code!r}, owner_id={self.owner_id!r})>"
        )
