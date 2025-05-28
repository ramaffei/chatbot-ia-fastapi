from exceptions.chat import ChatException
from models.chat_model import Chat, Message
from repositories.base import ModelRepository


class ChatRepository(ModelRepository):
    model: Chat = Chat
    field_not_found = ChatException(ChatException.ErrorCode.Chat_Not_Found)
    already_exists_error = ChatException(ChatException.ErrorCode.Already_Exist)

    def get_messages_by_chat_id(self, chat_id: str) -> list[Message]:
        chat: Chat = self.get(chat_id)
        if not chat:
            raise self.field_not_found
        return chat.messages or []

    def create_message(self, chat_id: str, role: str, content: str) -> Message:
        chat: Chat = self.get(chat_id)
        if not chat:
            raise self.field_not_found

        message = Message(role=role, content=content, chat_id=chat.id)
        chat.messages.append(message)
        self.update_instance(chat)
        return message
