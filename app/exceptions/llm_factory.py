from fastapi_exceptionshandler import APIError, ErrorCodeBase
from starlette import status


class LLMException(APIError):
    class ErrorCode(ErrorCodeBase):
        Model_Not_Found = "Model not found", status.HTTP_500_INTERNAL_SERVER_ERROR
        Model_Initialization_Error = (
            "Model initialization error",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        Import_Error = "Import error", status.HTTP_500_INTERNAL_SERVER_ERROR
