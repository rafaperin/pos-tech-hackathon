import uuid
from abc import ABC, abstractmethod
from typing import List

from src.entities.models.user_entity import User
from src.entities.schemas.user_dto import AuthenticateUserDTO


class IUserGateway(ABC):
    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def create(self, user_in: User) -> User:
        pass

    @abstractmethod
    def update(self, user_id: uuid.UUID, user_in: User) -> User:
        pass

    @abstractmethod
    def remove(self, user_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    def authenticate_user(self, user_in: AuthenticateUserDTO) -> User:
        pass
