from src.config.errors import DomainError, ResourceNotFound


class TimeSheetError(DomainError):
    @classmethod
    def invalid_time_sheet(cls) -> "TimeSheetError":
        return cls("User has not clocked in the correct amount of times")


class TimeSheetNotFound(ResourceNotFound):
    pass
