from models.chat_model import MessageRole
from pydantic import ConfigDict, Field
from schemas.base import CamelModel


class MessageBase(CamelModel):
    content: str = Field(
        ...,
        description="Content of the message",
        examples=["Hello, how can I help you?"],
    )


class MessageCreate(MessageBase):
    role: MessageRole = Field(
        ...,
        description="Role of the message sender",
        examples=[MessageRole.HumanMessage, MessageRole.AIMessage],
    )
    chat_id: str = Field(
        ...,
        description="ID of the chat this message belongs to",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )


class MessageRead(MessageBase):
    id: str = Field(
        ...,
        description="Unique identifier for the message",
        examples=["123e4567-e89b-12d3-a456-426614174001"],
    )

    model_config = ConfigDict(use_enum_values=True)


class ChatBase(CamelModel):
    username: str | None = Field(
        default=None,
        description="Username of the chat participant",
        examples=["john_doe"],
    )


class ChatRead(ChatBase):
    id: str = Field(
        description="Unique identifier for the chat",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    messages: list[MessageRead] = Field(
        default_factory=list,
        description="List of messages in the chat",
        examples=[
            {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "content": "Hello, how can I help you?",
                "role": "user",
                "chat_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
