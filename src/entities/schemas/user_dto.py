import datetime
import uuid
from typing import Optional, List

from pydantic import EmailStr

from src.utils.utils import CamelModel


class UserDTO(CamelModel):
    user_id: uuid.UUID
    username: str
    registration_number: int
    password: str
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "user_id": "00000000-0000-0000-0000-000000000000",
                "cpf": "000.000.000-00",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@email.com",
                "phone": "(11) 99999-9999"
            }
        }


class CreateUserDTO(CamelModel):
    cpf: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "cpf": "000.000.000-00",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@email.com",
                "phone": "(11) 99999-9999"
            }
        }


class ChangeUserDTO(CamelModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@email.com",
                "phone": "(11) 99999-9999"
            }
        }


class UserDTOResponse(CamelModel):
    result: UserDTO


class UserDTOListResponse(CamelModel):
    result: List[UserDTO]

