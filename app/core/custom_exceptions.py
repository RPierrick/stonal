from fastapi import status


class CustomException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class BadRequestError(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    err = "BadRequestError"


class IntegrityError(CustomException):
    status_code = status.HTTP_302_FOUND
    err = "DatabaseIntegrityError"


class NotFoundError(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    err = "NotFoundError"


class UnreachableDatabase(CustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    err = "Database not accessible"


class UniqueConstraintError(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    err = "Unique Key Constraint Violation"
