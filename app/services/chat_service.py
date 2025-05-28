from langchain_core.language_models.chat_models import BaseChatModel
from models.chat_model import Chat
from providers.llm_factory import get_llm
from repositories.chat_repository import ChatRepository
from sqlalchemy.orm import Session


class ChatService:
    def __init__(
        self, session: Session, chat_id: str | None = None, username: str | None = None
    ) -> None:
        self.llm: BaseChatModel = get_llm()
        self.chat_id: str | None = chat_id
        self.username: str | None = username
        self.repository = ChatRepository(session)

    def get_response_message(self, messages: list[str]) -> str:
        response = self.llm.invoke(messages)
        return response.content

    def _build_history(self) -> None:
        return

    @property
    def chat_id(self) -> str | None:
        return self._chat_id

    @chat_id.setter
    def chat_id(self, chat_id: str | None) -> None:
        self._chat_id: str | None = chat_id
        if chat_id is None:
            chat: Chat = self.repository.create(username=self.username)
            self._chat_id = chat.id
