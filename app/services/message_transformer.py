from langchain_core import messages
from langchain_core.messages import BaseMessage, SystemMessage
from models.chat_model import Message


class MessageTransformer:
    def to_langchain_messages(self, db_messages: list[Message]) -> list[BaseMessage]:
        return [self._build_message(msg.content, msg.role.name) for msg in db_messages]

    def get_system_message(
        self, prompt: str | None = None, context: str | None = None
    ) -> SystemMessage:
        default_prompt = (
            """ Por favor, responde a las preguntas de manera clara y concisa."""
            """ Si no tienes suficiente información, indica que no puedes responder."""
            """ Si la pregunta es ambigua, pide aclaraciones."""
            """ Si la pregunta es sobre un tema que no conoces, indica que no tienes información al respecto."""
            """ Si la pregunta es sobre un tema que no está relacionado con el contexto, indica que no puedes responder."""
            """ El contexto es el siguiente: """
            f" {context} "
            if context
            else ""
            """ Si no hay contexto, responde de manera general pero resumida."""
        )
        return SystemMessage(prompt or default_prompt)

    def _build_message(self, content: str, role: str) -> BaseMessage:
        try:
            cls = getattr(messages, role)
            return cls(content)
        except AttributeError:
            raise ValueError(f"No se encontró la clase '{role}' en langchain_core")
