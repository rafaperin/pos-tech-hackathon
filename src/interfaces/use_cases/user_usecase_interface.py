import uuid
from abc import ABC

from src.entities.models.user_entity import User
from src.entities.schemas.user_dto import CreateUserDTO, ChangeUserDTO, AuthenticateUserDTO
from src.interfaces.gateways.user_gateway_interface import IUserGateway


class UserUseCaseInterface(ABC):
    def __init__(self, user_repo: IUserGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, user_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def create(self, input_dto: CreateUserDTO) -> User:
        pass

    def update(self, user_id: uuid.UUID, input_dto: ChangeUserDTO) -> User:
        pass

    def remove(self, user_id: uuid.UUID) -> None:
        pass

    def authenticate(self, user_in: AuthenticateUserDTO) -> User:
        pass
