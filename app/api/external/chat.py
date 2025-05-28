import logging

from db.deps import get_session
from fastapi import APIRouter, Body, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from app.services.chat_service import ChatService
from schemas.external.message_schema import MessageInput

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/chat")
@version(1, 0)
def message_generate(
    session: Session = Depends(get_session),
    user_message: MessageInput = Body(...),
) -> dict:
    """
    Generate a response to a chat message.

    Args:
        message (str): The input message to generate a response for.

    Returns:
        dict: A dictionary containing the generated response.
    """
    logger.info(f"Received message: {user_message}")

    response = ChatService(
        session=session, username=user_message.username, chat_id=user_message.chat_id
    ).process_user_message(user_message=user_message.message)

    logger.info(f"Generated response: {response}")
    return response
