from langchain_core.language_models.chat_models import BaseChatModel
from providers.llm_factory import get_llm


class ChatService:
    def __init__(self) -> None:
        self.llm: BaseChatModel = get_llm()

    def chat(self, messages: list[str]) -> str:
        response = self.llm.invoke(messages)
        return response.content
