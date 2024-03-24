import datetime
import uuid

from src.adapters.time_sheet_json_adapter import time_sheet_list_to_json, time_sheet_to_json, user_records_to_json
from src.config.errors import ResourceNotFound, RepositoryError
from src.entities.schemas.time_sheet_dto import CreateTimeSheetDTO, ChangeTimeSheetDTO
from src.external.mailing_client import MailingClient
from src.gateways.postgres_gateways.time_sheet_gateway import PostgresDBTimeSheetRepository
from src.usecases.time_sheet_usecase import TimeSheetUseCase


class TimeSheetController:
    @staticmethod
    async def get_all_time_sheet_records() -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            all_time_sheets = TimeSheetUseCase(time_sheet_gateway).get_all()
            if all_time_sheets:
                result = time_sheet_list_to_json(all_time_sheets)
            else:
                result = list()
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_user_records_by_date(registration_number: int, date: datetime.datetime) -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            records = TimeSheetUseCase(time_sheet_gateway).get_user_records_by_date(registration_number, date)
            worked_hours = TimeSheetUseCase(time_sheet_gateway).get_user_worked_hours_by_date(
                records, registration_number, date
            )
            result = user_records_to_json(records, registration_number, worked_hours)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_user_records_by_month(registration_number: int, date: datetime.datetime) -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            records = TimeSheetUseCase(time_sheet_gateway).get_user_records_by_month(registration_number, date)
            worked_hours = TimeSheetUseCase(time_sheet_gateway).get_user_worked_hours_by_month(
                records, registration_number, date
            )
            result = user_records_to_json(records, registration_number, worked_hours)

            MailingClient.send(str(result))
        except Exception as e:
            print(e)
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_time_sheet_record_by_id(
        record_id: uuid.UUID
    ) -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            time_sheet = TimeSheetUseCase(time_sheet_gateway).get_by_id(record_id)
            result = time_sheet_to_json(time_sheet)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No time_sheet record with id: {record_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def create_time_sheet_record(
        request: CreateTimeSheetDTO
    ) -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            time_sheet = TimeSheetUseCase(time_sheet_gateway).create_time_sheet_record(request)
            result = time_sheet_to_json(time_sheet)
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_time_sheet_record_data(
        record_id: uuid.UUID,
        request: ChangeTimeSheetDTO
    ) -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            time_sheet = TimeSheetUseCase(time_sheet_gateway).update_time_sheet_record(record_id, request)
            result = time_sheet_to_json(time_sheet)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def remove_time_sheet_record(
        record_id: uuid.UUID
    ) -> dict:
        time_sheet_gateway = PostgresDBTimeSheetRepository()

        try:
            TimeSheetUseCase(time_sheet_gateway).remove_time_sheet_record(record_id)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Time sheet record removed successfully"}
