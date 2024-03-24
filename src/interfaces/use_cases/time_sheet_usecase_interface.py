import datetime
import uuid
from abc import ABC
from typing import List

from src.entities.models.time_sheet_entity import TimeSheet
from src.entities.schemas.time_sheet_dto import CreateTimeSheetDTO, ChangeTimeSheetDTO
from src.interfaces.gateways.time_sheet_gateway_interface import ITimeSheetGateway


class TimeSheetUseCaseInterface(ABC):
    def __init__(self, time_sheet_repo: ITimeSheetGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, record_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def get_user_records_by_date(self, registration_number: int, date: datetime.datetime):
        pass

    def get_user_records_by_month(self, registration_number: int, date: datetime.datetime):
        pass

    def get_user_worked_hours_by_date(self, records: List[TimeSheet], registration_number: int, date: datetime.datetime):
        pass

    def get_user_worked_hours_by_month(self, records: List[TimeSheet], registration_number: int, date: datetime.datetime):
        pass

    def create(self, input_dto: CreateTimeSheetDTO) -> TimeSheet:
        pass

    def update(self, record_id: uuid.UUID, input_dto: ChangeTimeSheetDTO) -> TimeSheet:
        pass

    def remove(self, record_id: uuid.UUID) -> None:
        pass
