import datetime
import random
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List

from src.entities.errors.time_sheet_error import TimeSheetError


class RecordType(Enum):
    IN: str = "in"
    OUT: str = "out"


@dataclass
class TimeSheet:
    record_id: uuid.UUID
    registration_number: int
    record_time: datetime.time
    record_type: str
    record_date: datetime.date

    @classmethod
    def create(cls, registration_number: int, record_type: str) -> "TimeSheet":
        record_id = uuid.uuid4()
        return cls(
            record_id=record_id,
            registration_number=registration_number,
            record_time=datetime.datetime.now().time(),
            record_type=record_type,
            record_date=datetime.datetime.now().date()
        )

    def check_if_in_time_or_out_time(self, records_amount: int):
        # Checks if the user has clocked in an even or odd amount of times
        if records_amount % 2 == 0:
            self.record_type = RecordType.IN.value
        else:
            self.record_type = RecordType.OUT.value


def time_sheet_factory(
    record_id: uuid.UUID,
    registration_number: int,
    record_time: datetime.time,
    record_type: str,
    record_date: datetime.date,
) -> TimeSheet:
    return TimeSheet(
        record_id=record_id,
        registration_number=registration_number,
        record_time=record_time,
        record_type=record_type,
        record_date=record_date
    )
