import logging

from exceptions.llm_factory import LLMException
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from settings.llm_settings import llm_settings

logger = logging.getLogger(__name__)


def get_llm() -> BaseChatModel:
    try:
        llm = init_chat_model(
            model=llm_settings.modelName,
            model_provider="google_genai",
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
