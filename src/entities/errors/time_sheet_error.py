from src.config.errors import DomainError, ResourceNotFound


class TimeSheetError(DomainError):
    @classmethod
    def invalid_time_sheet(cls) -> "TimeSheetError":
        return cls("User has not clocked in the correct amount of times")

    @classmethod
    def insufficient_permissions(cls) -> "TimeSheetError":
        return cls("User doesn´t have permission to access this data")


class TimeSheetNotFound(ResourceNotFound):
    pass
