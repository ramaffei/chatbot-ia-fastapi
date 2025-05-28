import logging
from app.services.chat_service import ChatService
from fastapi import APIRouter, Body, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session
from db.deps import get_session

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/chat")
@version(1, 0)
def message_generate(
    session: Session = Depends(get_session),
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

    response = ChatService(session).get_response_message([message])
    logger.info(f"Generated response: {response}")
    return response
