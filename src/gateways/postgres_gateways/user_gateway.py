import uuid
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from src.entities.models.user_entity import User, user_factory
from src.external.postgresql_database import SessionLocal
from src.gateways.orm.user_orm import Users
from src.interfaces.gateways.user_gateway_interface import IUserGateway


class PostgresDBUserRepository(IUserGateway):
    @staticmethod
    def to_entity(user: Users) -> User:
        user = user_factory(
            user_id=user.user_id,
            username=user.username,
            registration_number=user.registration_number,
            password=user.password,
            created_at=user.created_at,
            modified_at=user.modified_at,
        )
        return user

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        with SessionLocal() as db:
            result = db.query(Users).filter(Users.user_id == user_id).first()
        if result:
            return self.to_entity(result)
        else:
            return None

    def get_all(self) -> List[User]:
        users = []

        with SessionLocal() as db:
            result = db.query(Users).all()

        for user in result:
            users.append(self.to_entity(user))

        return users

    def create(self, obj_in: User) -> User:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = Users(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        new_user = self.to_entity(db_obj)  # type: ignore
        return new_user

    def update(self, user_id: uuid.UUID, obj_in: User) -> User:
        user_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(Users).filter(Users.user_id == user_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in user_in:
                    setattr(db_obj, field, user_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        updated_user = self.to_entity(db_obj)
        return updated_user

    def remove(self, user_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            db_obj = db.query(Users).filter(Users.user_id == user_id).first()
            db.delete(db_obj)
            db.commit()

    def authenticate_user(self, user_in: User) -> Optional[User]:
        with SessionLocal() as db:
            result = db.query(Users).filter(Users.username == user_in.username).first()
        if result:
            return self.to_entity(result)
        else:
            return None
