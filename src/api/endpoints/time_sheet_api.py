import datetime
import uuid

from fastapi import APIRouter, status, Depends

from src.api.errors.api_errors import APIErrorMessage
from src.config import security
from src.config.errors import RepositoryError, ResourceNotFound
from src.controllers.time_sheet_controller import TimeSheetController
from src.entities.schemas.time_sheet_dto import TimeSheetDTOResponse, CreateTimeSheetDTO, \
    ChangeTimeSheetDTO, TimeSheetDTOListResponse

router = APIRouter(tags=["Time Sheets"])


@router.get(
    "/time-sheets",
    response_model=TimeSheetDTOListResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_time_sheet_records() -> dict:
    try:
        result = await TimeSheetController.get_all_time_sheet_records()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/time-sheets/user/{registration_number}/date",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_user_worked_hours_by_date(
    registration_number: int, day: int, month: int, year: int
) -> dict:
    date = datetime.datetime(year, month, day)
    try:
        result = await TimeSheetController.get_user_records_by_date(registration_number, date)
    except Exception as e:
        print(e)
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/time-sheets/user/{registration_number}/month",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_user_worked_hours_by_month(
    registration_number: int, month: int, year: int
) -> dict:
    date = datetime.datetime(year, month, 1)
    try:
        result = await TimeSheetController.get_user_records_by_month(registration_number, date)
    except Exception as e:
        print(e)
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/time-sheets/record-id/{record_id}",
    response_model=TimeSheetDTOResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_time_sheet_record_by_id(
    record_id: uuid.UUID
) -> dict:
    try:
        result = await TimeSheetController.get_time_sheet_record_by_id(record_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No time sheet with id: {record_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.post(
    "/time-sheets",
    response_model=TimeSheetDTOResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_time_sheet_record(
    request: CreateTimeSheetDTO
) -> dict:
    try:
        result = await TimeSheetController.create_time_sheet_record(request)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/time-sheets/{record_id}",
    response_model=TimeSheetDTOResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def change_time_sheet_record(
    record_id: uuid.UUID,
    request: ChangeTimeSheetDTO
) -> dict:
    try:
        result = await TimeSheetController.change_time_sheet_record(record_id, request)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.delete(
    "/time-sheets/record-id/{time_sheet_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_time_sheet_record(
    record_id: uuid.UUID
) -> dict:
    try:
        await TimeSheetController.remove_time_sheet_record(record_id)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return {"result": "Time sheet record removed successfully"}
