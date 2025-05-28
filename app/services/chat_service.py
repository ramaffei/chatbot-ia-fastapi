import logging

from exceptions.chat import ChatException
from langchain_core.messages import BaseMessage
from models.chat_model import Chat, MessageRole
from providers.llm_provider import LLMProvider
from repositories.chat_repository import ChatRepository
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
        self.username: str | None = username
        self._chat_id = self._ensure_chat_exists(chat_id, username)

    def process_user_message(self, user_message: str) -> BaseMessage:
        try:
            # 1. Guardar mensaje del usuario
            self.repository.create_message(
                chat_id=self._chat_id,
                role=MessageRole.HumanMessage,
                content=user_message,
            )

            # 2. Construir historial para LLM
            history = self._build_history()

            # 3. Obtener respuesta del LLM
            ai_response = self.llm_service.get_message_response(history=history)

            # 4. Guardar respuesta de la IA
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

    @property
    def chat_id(self) -> str:
        return self._chat_id
