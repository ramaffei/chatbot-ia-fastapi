from fastapi_exceptionshandler import APIError, ErrorCodeBase
from starlette import status


class RAGException(APIError):
    class ErrorCode(ErrorCodeBase):
        Documents_Not_Found = "Documents not found", status.HTTP_404_NOT_FOUND
        RAG_Internal_Error = (
            "RAG internal error",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
