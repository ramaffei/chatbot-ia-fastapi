from models.chat_model import MessageRole
from pydantic import ConfigDict, Field
from schemas.base import CamelModel


class MessageInput(CamelModel):
    message: str = Field(
        ...,
        description="The input message to generate a response for",
        examples=["Hello, how can I help you?"],
    )
    username: str | None = Field(
        default=None, description="Username of the chat participant"
    )
    chat_id: str | None = Field(
        default=None, description="ID of the chat this message belongs to"
    )


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
