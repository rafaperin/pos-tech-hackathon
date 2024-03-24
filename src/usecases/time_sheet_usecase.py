import datetime
import uuid
from typing import List

from src.config.errors import ResourceNotFound
from src.entities.errors.time_sheet_error import TimeSheetError

from src.entities.schemas.time_sheet_dto import CreateTimeSheetDTO, ChangeTimeSheetDTO
from src.entities.models.time_sheet_entity import TimeSheet, RecordType
from src.interfaces.gateways.time_sheet_gateway_interface import ITimeSheetGateway
from src.interfaces.use_cases.time_sheet_usecase_interface import TimeSheetUseCaseInterface


class TimeSheetUseCase(TimeSheetUseCaseInterface):
    def __init__(self, time_sheet_repo: ITimeSheetGateway) -> None:
        self._time_sheet_repo = time_sheet_repo

    def get_by_id(self, record_id: uuid.UUID):
        result = self._time_sheet_repo.get_by_id(record_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._time_sheet_repo.get_all()

    def get_user_records_by_date(self, registration_number: int, date: datetime.datetime):
        return self._time_sheet_repo.get_all_records_by_date(registration_number, date)

    def get_user_records_by_month(self, registration_number: int, date: datetime.datetime):
        return self._time_sheet_repo.get_all_records_by_month(registration_number, date)

    def get_user_worked_hours_by_date(
        self, records: List[TimeSheet], registration_number: int, date: datetime.datetime
    ):
        in_records, out_records = [], []

        for record in records:
            if record.record_type == RecordType.IN.value:
                in_records.append(record)
            else:
                out_records.append(record)

        if (len(in_records) + len(out_records)) % 2 != 0:
            raise TimeSheetError.invalid_time_sheet()

        worked_hours_sum = datetime.timedelta()
        for record in in_records:
            (h, m, s) = str(record.record_time).split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            worked_hours_sum += d

        break_hours_sum = datetime.timedelta()
        for record in out_records:
            (h, m, s) = str(record.record_time).split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            break_hours_sum += d

        return break_hours_sum - worked_hours_sum

    def get_user_worked_hours_by_month(
        self, records: List[TimeSheet], registration_number: int, date: datetime.datetime
    ):
        in_records, out_records = [], []

        for record in records:
            if record.record_type == RecordType.IN.value:
                in_records.append(record)
            else:
                out_records.append(record)

        if (len(in_records) + len(out_records)) % 2 != 0:
            raise TimeSheetError.invalid_time_sheet()

        worked_hours_sum = datetime.timedelta()
        for record in in_records:
            (h, m, s) = str(record.record_time).split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            worked_hours_sum += d

        break_hours_sum = datetime.timedelta()
        for record in out_records:
            (h, m, s) = str(record.record_time).split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            break_hours_sum += d

        return break_hours_sum - worked_hours_sum

    def create_time_sheet_record(self, input_dto: CreateTimeSheetDTO) -> TimeSheet:
        records = self._time_sheet_repo.get_all_records_by_date(
            input_dto.registration_number, date=datetime.date.today()
        )
        record_type = ""

        if len(records) % 2 == 0:
            record_type = RecordType.IN.value
        else:
            record_type = RecordType.OUT.value

        time_sheet = TimeSheet.create(
            input_dto.registration_number,
            record_type
        )

        new_time_sheet = self._time_sheet_repo.create(time_sheet)
        return new_time_sheet

    def update_time_sheet_record(self, record_id: uuid.UUID, input_dto: ChangeTimeSheetDTO) -> TimeSheet:
        time_sheet = self._time_sheet_repo.get_by_id(record_id)

        # if input_dto.timeSheetname:
        #     time_sheet.change_timeSheetname(input_dto.timeSheetname)
        # if input_dto.password:
        #     timeSheet.change_password(input_dto.password)

        updated_time_sheet = self._time_sheet_repo.update(record_id, time_sheet)
        return updated_time_sheet

    def remove_time_sheet_record(self, record_id: uuid.UUID) -> None:
        self._time_sheet_repo.remove(record_id)
