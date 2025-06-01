import logging
from typing import Any, Dict, List

from exceptions.chat import ChatException
from langchain_core.messages import BaseMessage, SystemMessage
from models.chat_model import Chat, MessageRole
from providers.llm_provider import LLMProvider
from repositories.chat_repository import ChatRepository
from services.document_service import DocumentService
from services.message_transformer import MessageTransformer
from sqlalchemy.orm import Session

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
            relevant_context = await self.document_service.query_documents(
                conversation_id=self._chat_id, query=user_message
            )

            # 3. Construir historial para LLM
            history = self._build_history()

            # 4. Agregar contexto de documentos si existe
            if relevant_context:
                context_text = self._format_context(relevant_context)
                history.insert(
                    0,
                    SystemMessage(
                        content=f"Context from relevant documents:\n{context_text}\n\nPlease use this context to inform your response when relevant."
                    ),
                )

            # 5. Obtener respuesta del LLM
            ai_response = self.llm_service.get_message_response(history=history)

            # 6. Guardar respuesta de la IA
            self.repository.create_message(
                chat_id=self._chat_id,
                role=MessageRole.AIMessage,
                content=ai_response.content,
            )

            return ai_response

        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            raise ChatException(ChatException.ErrorCode.Chat_Internal_Error)

    def _build_history(self) -> list[BaseMessage]:
        db_messages = self.repository.get_chat_messages_by_id(self._chat_id)
        history = [self.transformer.get_system_message()]
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
