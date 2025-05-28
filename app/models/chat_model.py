import enum
import uuid

from db.base_class import Base
from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chat(Base):
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    username: Mapped[str] = mapped_column(String(50), nullable=True)

    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan", uselist=True
    )


class MessageRole(enum.StrEnum):
    HumanMessage = "user"
    AIMessage = "assistant"


class Message(Base):
    updated_at = None

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    chat_id: Mapped[str] = mapped_column(
        String(36), ForeignKey(Chat.id, ondelete="CASCADE"), nullable=False
    )
    role: Mapped[MessageRole] = mapped_column(
        Enum(
            MessageRole,
            native_enum=False,
            length=50,
            values_callable=lambda obj: [e.value for e in obj],
        )
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
