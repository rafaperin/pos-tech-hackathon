import datetime
import uuid
from dataclasses import dataclass


@dataclass
class User:
    user_id: uuid.UUID
    username: str
    registration_number: int
    password: str
    created_at: datetime.datetime
    modified_at: datetime.datetime

    @classmethod
    def create(cls, username: str, registration_number: int, password: str) -> "User":
        user_id = uuid.uuid4()
        return cls(
            user_id=user_id,
            username=username,
            registration_number=registration_number,
            password=password,
            created_at=datetime.datetime.utcnow(),
            modified_at=datetime.datetime.utcnow()
        )

    def change_username(self, new_username) -> None:
        self.username = new_username

    def change_password(self, new_password) -> None:
        self.password = new_password


def user_factory(
    user_id: uuid.UUID,
    username: str,
    registration_number: int,
    password: str,
    created_at: datetime.datetime,
    modified_at: datetime.datetime
) -> User:
    return User(
        user_id=user_id,
        username=username,
        registration_number=registration_number,
        password=password,
        created_at=created_at,
        modified_at=modified_at
    )
