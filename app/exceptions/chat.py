from fastapi_exceptionshandler import APIError, ErrorCodeBase
from starlette import status


class ChatException(APIError):
    class ErrorCode(ErrorCodeBase):
        Chat_Not_Found = "Chat not found", status.HTTP_404_NOT_FOUND
        Already_Exist = (
            "Chat already exists",
            status.HTTP_409_CONFLICT,
        )
        Message_Not_Found = "Message not found", status.HTTP_404_NOT_FOUND
