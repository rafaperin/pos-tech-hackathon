import datetime
import uuid

from sqlalchemy import String, DateTime, func, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.external.postgresql_database import Base


class TimeSheets(Base):
    __tablename__ = "time_sheets"
    record_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    registration_number: Mapped[int] = mapped_column(ForeignKey("users.registration_number"))
    record_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    record_type: Mapped[str] = mapped_column(String(64))
    record_date: Mapped[datetime.date] = mapped_column(Date())

    user: Mapped["Users"] = relationship(back_populates="time_sheets")

