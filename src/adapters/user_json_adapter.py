from typing import List

from src.entities.models.user_entity import User
from src.utils.utils import camelize_dict


def user_to_json(user: User):
    return camelize_dict(user.__dict__)


def user_list_to_json(user_list: List[User]):
    return [camelize_dict(user.__dict__) for user in user_list]


def access_token_to_json(user: User, token: str):
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user.user_id),
            "userName": user.username,
            "registrationNumber": user.registration_number
        }
    }
