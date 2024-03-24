from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.config.errors import RepositoryError
from src.controllers.user_controller import UserController
from src.entities.schemas.user_dto import AuthenticateUserDTO

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user_in = AuthenticateUserDTO(
        username=form_data.username,
        password=form_data.password
    )

    try:
        result = await UserController.authenticate_user(user_in)
    except Exception as e:
        print(e)
        raise RepositoryError.get_operation_failed()

    return result
