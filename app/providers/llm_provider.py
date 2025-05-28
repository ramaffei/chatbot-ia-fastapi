import logging

from exceptions.llm import LLMException
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from settings.llm_settings import llm_settings

logger = logging.getLogger(__name__)


class LLMProvider:
    def __init__(self) -> None:
        self.llm: BaseChatModel = self.get_llm()

    def get_message_response(self, history: list[BaseMessage]) -> BaseMessage:
        try:
            response: BaseMessage = self.llm.invoke(history)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise LLMException(LLMException.ErrorCode.LLM_Internal_Error)

    def get_llm(self) -> BaseChatModel:
        try:
            llm = init_chat_model(
                model=llm_settings.modelName,
                model_provider=llm_settings.modelProvider,
                temperature=llm_settings.temperature,
                max_tokens=llm_settings.maxTokens,
                api_key=llm_settings.apiKey,
            )
            return llm
        except ImportError as e:
            logger.error(
                f"Error importing model provider {llm_settings.modelProvider}: {e}"
            )
            raise LLMException(LLMException.ErrorCode.Import_Error)
        except ValueError as e:
            logger.error(f"Error initializing model {llm_settings.modelName}: {e}")
            raise LLMException(LLMException.ErrorCode.Model_Initialization_Error)
