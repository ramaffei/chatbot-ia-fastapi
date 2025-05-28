from exceptions.chat import ChatException
from models.chat_model import Chat
from repositories.base import ModelRepository


class ChatRepository(ModelRepository):
    model: Chat = Chat
    field_not_found = ChatException(ChatException.ErrorCode.Chat_Not_Found)
    already_exists_error = ChatException(ChatException.ErrorCode.Already_Exist)
