from langchain_core.language_models.chat_models import BaseChatModel
from models.chat_model import Chat, Message, MessageRole
from providers.llm_factory import get_llm
from repositories.chat_repository import ChatRepository
from sqlalchemy.orm import Session
from langchain_core import messages
from langchain_core.messages import BaseMessage


class ChatService:
    def __init__(
        self, session: Session, chat_id: str | None = None, username: str | None = None
    ) -> None:
        self.llm: BaseChatModel = get_llm()
        self.chat_id: str | None = chat_id
        self.username: str | None = username
        self.repository = ChatRepository(session)

    def get_response_message(self, user_message: str) -> str:
        self.repository.create_message(
            chat_id=self.chat_id,
            role=MessageRole.HumanMessage,
            content=user_message,
        )
        messages_history = self._build_history()
        response = self.llm.invoke(messages_history)
        self.repository.create_message(
            chat_id=self.chat_id,
            role=MessageRole.AIMessage,
            content=response.content,
        )
        return response.content

    def _build_history(self) -> list[BaseMessage]:
        chat_messages: list[Message] = self.repository.get_messages_by_chat_id(
            self.chat_id
        )
        history = []
        history.append(self._get_system_message())
        for message in chat_messages:
            history.append(self._build_message(message.content, message.role.name))
        return history

    def _get_system_message(self) -> BaseMessage | None:
        return messages.SystemMessage(
            "Por favor, responde a las preguntas de manera clara y concisa."
        )

    def _build_message(self, content: str, role: str) -> BaseMessage:
        try:
            cls = getattr(messages, role)
            return cls(content)
        except AttributeError:
            raise ValueError(f"No se encontró la clase '{role}' en langchain_core")

    @property
    def chat_id(self) -> str | None:
        return self._chat_id

    @chat_id.setter
    def chat_id(self, chat_id: str | None) -> None:
        self._chat_id: str | None = chat_id
        if chat_id is None:
            chat: Chat = self.repository.create(username=self.username)
            self._chat_id = chat.id
