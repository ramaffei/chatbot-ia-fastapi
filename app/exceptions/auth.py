from fastapi.exception_handlers import REPORT_LEVEL, APIError, ErrorCodeBase
from starlette import status


class AuthException(APIError):
    # This status code may be overridden
    status_code = status.HTTP_400_BAD_REQUEST
    report_level = REPORT_LEVEL.IGNORE

    class ErrorCode(ErrorCodeBase):
        Not_Authorized = "Not authorized", status.HTTP_401_UNAUTHORIZED
