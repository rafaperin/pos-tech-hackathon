import uuid
from abc import ABC

from src.entities.models.user_entity import Customer
from src.entities.schemas.user_dto import CreateCustomerDTO, ChangeCustomerDTO
from src.interfaces.gateways.customer_gateway_interface import ICustomerGateway


class CustomerUseCaseInterface(ABC):
    def __init__(self, customer_repo: ICustomerGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, customer_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def create(self, input_dto: CreateCustomerDTO) -> Customer:
        pass

    def update(self, customer_id: uuid.UUID, input_dto: ChangeCustomerDTO) -> Customer:
        pass

    def remove(self, customer_id: uuid.UUID) -> None:
        pass

    def anonymize_data(self, customer_id: uuid.UUID) -> Customer:
        pass
