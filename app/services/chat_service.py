import logging
from typing import Any, Dict, List

from exceptions.chat import ChatException
from langchain_core.messages import BaseMessage
from models.chat_model import Chat, MessageRole
from providers.llm_provider import LLMProvider
from repositories.chat_repository import ChatRepository
from services.document_service import DocumentService
from services.message_transformer import MessageTransformer
from sqlalchemy.orm import Session

from services.rag_service import VectorStoreService

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(
        self,
        session: Session,
        chat_id: str | None = None,
        username: str | None = None,
    ):
        self.repository = ChatRepository(session)
        self.llm_service = LLMProvider()
        self.transformer = MessageTransformer()
        self.document_service = DocumentService()
        self.rag_service = VectorStoreService()
        self.username: str | None = username
        self._chat_id = self._ensure_chat_exists(chat_id, username)

    async def process_pdf(self, file_content: bytes) -> str:
        """Process and store a PDF file for the current conversation"""
        return await self.document_service.process_pdf(
            file_content=file_content, conversation_id=self._chat_id
        )

    async def process_user_message(self, user_message: str) -> BaseMessage:
        try:
            # 1. Guardar mensaje del usuario
            self.repository.create_message(
                chat_id=self._chat_id,
                role=MessageRole.HumanMessage,
                content=user_message,
            )

            # 2. Buscar contexto relevante en los documentos
            context_text = self.rag_service.similarity_search_by_query(
                query=user_message
            )

            # 3. Construir historial para LLM
            history = self._build_history(context=context_text)

            # 4. Obtener respuesta del LLM
            ai_response = self.llm_service.get_message_response(history=history)

            # 5. Guardar respuesta de la IA
            self.repository.create_message(
                chat_id=self._chat_id,
                role=MessageRole.AIMessage,
                content=ai_response.content,
            )

            return ai_response

        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            raise ChatException(ChatException.ErrorCode.Chat_Internal_Error)

    def _build_history(self, context: str | None) -> list[BaseMessage]:
        db_messages = self.repository.get_chat_messages_by_id(self._chat_id)
        history = [self.transformer.get_system_message(context=context)]
        history.extend(self.transformer.to_langchain_messages(db_messages))
        return history

    def _ensure_chat_exists(self, chat_id: str | None, username: str | None) -> str:
        if chat_id is None:
            chat: Chat = self.repository.create(username=username)
            return chat.id
        return chat_id

    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """Format the document context into a readable string"""
        formatted_chunks = []
        for item in context:
            relevance = round(item["relevance"] * 100)
            formatted_chunks.append(
                f"[Relevance: {relevance}%]\n{item['content'].strip()}\n"
            )
        return "\n---\n".join(formatted_chunks)

    @property
    def chat_id(self) -> str:
        return self._chat_id
