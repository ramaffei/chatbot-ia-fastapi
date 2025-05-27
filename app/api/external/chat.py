import logging
from app.services.chat_service import ChatService
from fastapi import APIRouter, Body
from fastapi_versioning import version

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/chat")
@version(1, 0)
def message_generate(
    message: str = Body(embed=True),
) -> str:
    """
    Generate a response to a chat message.

    Args:
        message (str): The input message to generate a response for.

    Returns:
        dict: A dictionary containing the generated response.
    """
    logger.info(f"Received message: {message}")

    response = ChatService().chat([message])
    logger.info(f"Generated response: {response}")
    return response
