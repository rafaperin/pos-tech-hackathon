import datetime
import uuid
from abc import ABC, abstractmethod
from typing import List

from src.entities.models.time_sheet_entity import TimeSheet


class ITimeSheetGateway(ABC):
    @abstractmethod
    def get_by_id(self, record_id: uuid.UUID) -> TimeSheet:
        pass

    @abstractmethod
    def get_all(self) -> List[TimeSheet]:
        pass

    @abstractmethod
    def get_all_records_by_date(self, registration_number: int, date: datetime.date) -> List[TimeSheet]:
        pass

    @abstractmethod
    def get_all_records_by_month(self, registration_number: int, date: datetime.date) -> List[TimeSheet]:
        pass

    @abstractmethod
    def create(self, time_sheet_in: TimeSheet) -> TimeSheet:
        pass

    @abstractmethod
    def update(self, record_id: uuid.UUID, time_sheet_in: TimeSheet) -> TimeSheet:
        pass

    @abstractmethod
    def remove(self, record_id: uuid.UUID) -> None:
        pass
