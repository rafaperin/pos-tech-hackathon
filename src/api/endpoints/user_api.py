import uuid
from typing import Any

from fastapi import APIRouter, status, Depends

from src.api.errors.api_errors import APIErrorMessage
from src.config import security
from src.config.errors import RepositoryError, ResourceNotFound
from src.controllers.user_controller import UserController
from src.entities.schemas.user_dto import UserDTOResponse, CreateUserDTO, \
    ChangeUserDTO, UserDTOListResponse
from src.utils import utils

router = APIRouter(tags=["Users"])


@router.get(
    "/users",
    response_model=UserDTOListResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_users() -> dict:
    try:
        result = await UserController.get_all_users()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/users/id/{user_id}",
    response_model=UserDTOResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_user_by_id(
    user_id: uuid.UUID
) -> dict:
    try:
        result = await UserController.get_user_by_id(user_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No user with id: {user_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.post(
    "/users",
    response_model=UserDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_user(
    request: CreateUserDTO
) -> dict:
    try:
        result = await UserController.create_user(request)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/users/{user_id}",
    response_model=UserDTOResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def change_user_data(
    user_id: uuid.UUID,
    request: ChangeUserDTO
) -> dict:
    try:
        result = await UserController.change_user_data(user_id, request)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security.validate_token)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_user(
    user_id: uuid.UUID
) -> dict:
    try:
        await UserController.remove_user(user_id)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return {"result": "User removed successfully"}
