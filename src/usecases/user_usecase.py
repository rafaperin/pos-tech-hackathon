import uuid
from typing import Optional

from src.config.errors import ResourceNotFound
from src.config.security import verify_password, get_password_hash

from src.entities.schemas.user_dto import CreateUserDTO, ChangeUserDTO, AuthenticateUserDTO
from src.entities.models.user_entity import User
from src.interfaces.gateways.user_gateway_interface import IUserGateway
from src.interfaces.use_cases.user_usecase_interface import UserUseCaseInterface


class UserUseCase(UserUseCaseInterface):
    def __init__(self, user_repo: IUserGateway) -> None:
        self._user_repo = user_repo

    def get_by_id(self, user_id: uuid.UUID):
        result = self._user_repo.get_by_id(user_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._user_repo.get_all()

    def create(self, input_dto: CreateUserDTO) -> User:
        user = User.create(
            input_dto.username,
            get_password_hash(input_dto.password)
        )

        new_user = self._user_repo.create(user)
        return new_user

    def update(self, user_id: uuid.UUID, input_dto: ChangeUserDTO) -> User:
        user = self._user_repo.get_by_id(user_id)

        if input_dto.username:
            user.change_username(input_dto.username)
        if input_dto.password:
            user.change_password(input_dto.password)

        updated_user = self._user_repo.update(user_id, user)
        return updated_user

    def remove(self, user_id: uuid.UUID) -> None:
        self._user_repo.remove(user_id)

    def authenticate(self, user_in: AuthenticateUserDTO) -> Optional[User]:
        user = self._user_repo.authenticate_user(user_in)
        if not user:
            return None
        if not verify_password(user_in.password, user.password):
            return None
        return user
