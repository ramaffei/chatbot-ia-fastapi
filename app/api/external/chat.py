import logging

from db.deps import get_session
from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi_versioning import version
from schemas.external.message_schema import MessageInput
from services.chat_service import ChatService
from services.rag_service import RAGService
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/chat")
@version(1, 0)
async def message_generate(
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

    chat_service = ChatService(
        session=session, username=user_message.username, chat_id=user_message.chat_id
    )
    response = await chat_service.process_user_message(
        user_message=user_message.message
    )

    logger.info(f"Generated response: {response}")
    return {"content": response.content, "chat_id": chat_service.chat_id}


@router.post("/chat/upload-pdf")
@version(1, 0)
async def upload_pdf(
    file: UploadFile = File(...),
) -> dict:
    """
    Upload a PDF file to be used as context in the chat.

    Args:
        file: The PDF file to upload

    Returns:
        dict: A dictionary containing the document ID
    """
    if not file.content_type == "application/pdf":
        raise ValueError("File must be a PDF")

    contents = await file.read()

    chat_service = RAGService()

    document_id = chat_service.add_pdf_to_vector_store(contents)

    return {"document_len": len(document_id)}
