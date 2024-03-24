import datetime
import uuid

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.external.postgresql_database import Base


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(60))
    registration_number: Mapped[int] = mapped_column()
    password: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    time_sheets: Mapped["TimeSheets"] = relationship(back_populates="user")
