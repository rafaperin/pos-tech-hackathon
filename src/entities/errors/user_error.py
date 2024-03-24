from src.config.errors import DomainError, ResourceNotFound


class UserError(DomainError):
    @classmethod
    def invalid_user_or_password(cls) -> "UserError":
        return cls("Provided user or password is not valid!")


class UserNotFound(ResourceNotFound):
    pass
