from langchain_core import messages
from langchain_core.messages import BaseMessage, SystemMessage
from models.chat_model import Message


class MessageTransformer:
    def to_langchain_messages(self, db_messages: list[Message]) -> list[BaseMessage]:
        return [self._build_message(msg.content, msg.role.name) for msg in db_messages]

    def get_system_message(self, prompt: str | None = None) -> SystemMessage:
        default_prompt = (
            "Por favor, responde a las preguntas de manera clara y concisa."
        )
        return SystemMessage(prompt or default_prompt)

    def _build_message(self, content: str, role: str) -> BaseMessage:
        try:
            cls = getattr(messages, role)
            return cls(content)
        except AttributeError:
            raise ValueError(f"No se encontró la clase '{role}' en langchain_core")
