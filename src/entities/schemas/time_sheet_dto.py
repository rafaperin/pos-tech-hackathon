import datetime
import uuid
from typing import List

from src.utils.utils import CamelModel


class TimeSheetDTO(CamelModel):
    record_id: uuid.UUID
    registration_number: int
    record_time: datetime.time
    record_type: str
    record_date: datetime.date


class CreateTimeSheetDTO(CamelModel):
    registration_number: int


class ChangeTimeSheetDTO(CamelModel):
    registration_number: int


class TimeSheetDTOResponse(CamelModel):
    result: TimeSheetDTO


class TimeSheetDTOListResponse(CamelModel):
    result: List[TimeSheetDTO]
