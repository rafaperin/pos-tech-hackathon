import uuid

from src.adapters.user_json_adapter import user_list_to_json, user_to_json, access_token_to_json
from src.config.errors import ResourceNotFound, RepositoryError
from src.config.security import create_access_token
from src.entities.errors.user_error import UserError
from src.entities.schemas.user_dto import CreateUserDTO, ChangeUserDTO, AuthenticateUserDTO
from src.gateways.postgres_gateways.user_gateway import PostgresDBUserRepository
from src.usecases.user_usecase import UserUseCase


class UserController:
    @staticmethod
    async def authenticate_user(user_in: AuthenticateUserDTO) -> dict:
        user_gateway = PostgresDBUserRepository()

        try:
            user = UserUseCase(user_gateway).authenticate(user_in)
            if not user:
                raise UserError.invalid_user_or_password()
            token = create_access_token(
                sub=str(user.user_id), username=user.username, registration_number=user.registration_number
            )
            result = access_token_to_json(user, token)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return result

    @staticmethod
    async def get_all_users() -> dict:
        user_gateway = PostgresDBUserRepository()

        try:
            all_users = UserUseCase(user_gateway).get_all()
            if all_users:
                result = user_list_to_json(all_users)
            else:
                result = list()
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_user_by_id(
        user_id: uuid.UUID
    ) -> dict:
        user_gateway = PostgresDBUserRepository()

        try:
            user = UserUseCase(user_gateway).get_by_id(user_id)
            result = user_to_json(user)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No user with id: {user_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def create_user(
        request: CreateUserDTO
    ) -> dict:
        user_gateway = PostgresDBUserRepository()

        try:
            user = UserUseCase(user_gateway).create(request)
            result = user_to_json(user)
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_user_data(
        user_id: uuid.UUID,
        request: ChangeUserDTO
    ) -> dict:
        user_gateway = PostgresDBUserRepository()

        try:
            user = UserUseCase(user_gateway).update(user_id, request)
            result = user_to_json(user)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def remove_user(
        user_id: uuid.UUID
    ) -> dict:
        user_gateway = PostgresDBUserRepository()

        try:
            UserUseCase(user_gateway).remove(user_id)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "User removed successfully"}
