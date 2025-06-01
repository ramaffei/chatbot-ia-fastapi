import logging
from typing import Dict, Any

from db.deps import get_session
from fastapi import APIRouter, Body, Depends, UploadFile, File
from fastapi_versioning import version
from sqlalchemy.orm import Session

from services.chat_service import ChatService
from schemas.external.message_schema import MessageInput

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/chat")
@version(1, 0)
async def message_generate(
    session: Session = Depends(get_session),
    user_message: MessageInput = Body(...),
) -> Dict[str, Any]:
    """
    Generate a response to a chat message.

    Args:
        message (str): The input message to generate a response for.

    Returns:
        dict: A dictionary containing the generated response.
    """
    logger.info(f"Received message: {user_message}")

    chat_service = ChatService(
        session=session, username=user_message.username, chat_id=user_message.chat_id
    )
    response = await chat_service.process_user_message(
        user_message=user_message.message
    )

    logger.info(f"Generated response: {response}")
    return {"content": response.content}


@router.post("/chat/upload-pdf")
@version(1, 0)
async def upload_pdf(
    file: UploadFile = File(...),
    chat_id: str | None = None,
    username: str | None = None,
    session: Session = Depends(get_session),
) -> Dict[str, str]:
    """
    Upload a PDF file to be used as context in the chat.

    Args:
        file: The PDF file to upload
        chat_id: Optional chat ID to associate the document with
        username: Optional username for the chat

    Returns:
        dict: A dictionary containing the document ID
    """
    if not file.content_type == "application/pdf":
        raise ValueError("File must be a PDF")

    contents = await file.read()

    chat_service = ChatService(session=session, chat_id=chat_id, username=username)

    document_id = await chat_service.process_pdf(contents)

    return {"document_id": document_id}
