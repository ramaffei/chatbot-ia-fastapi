from enum import Enum

from fastapi_exceptionshandler import APIError
from starlette import status


class TokenException(APIError):
    class ErrorCode(Enum):
        No_Credentials = "Unauthenticated Error"
        Invalid_Token = "Invalid Token"

    class StatusCode(Enum):
        No_Credentials = status.HTTP_401_UNAUTHORIZED
        Invalid_Token = status.HTTP_403_FORBIDDEN

    def __init__(
        self, error_code: ErrorCode, exception: Exception | None = None
    ) -> None:
        super().__init__(error_code, exception)
        if hasattr(self.StatusCode, error_code.name):
            self.status_code = getattr(self.StatusCode, error_code.name).value
