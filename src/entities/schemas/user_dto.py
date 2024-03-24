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


class UserResponseDTO(CamelModel):
    user_id: uuid.UUID
    username: str
    registration_number: int
    created_at: datetime.datetime
    modified_at: datetime.datetime


class CreateUserDTO(CamelModel):
    username: Optional[str]
    password: Optional[str]


class AuthenticateUserDTO(CamelModel):
    username: Optional[str]
    password: Optional[str]


class ChangeUserDTO(CamelModel):
    username: Optional[str]
    password: Optional[str]


class UserDTOResponse(CamelModel):
    result: UserResponseDTO


class UserDTOListResponse(CamelModel):
    result: List[UserResponseDTO]

