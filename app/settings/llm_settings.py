import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.llm_supported_models import SUPPORTED_MODELS

from app.exceptions.llm_factory import LLMException

logger = logging.getLogger(__name__)


class LLMSettings(BaseSettings):
    """
    Settings for the LLM (Large Language Model) integration.
    This class holds configuration options for the LLM, such as the model name,
    temperature, and max tokens.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    modelName: Optional[str] = "gemini-2.0-flash"
    temperature: Optional[float] = 0.7
    maxTokens: Optional[int] = None
    apiKey: Optional[str] = None
    modelProvider: Optional[str] = None

    def get_provider(self) -> str:
        if self.modelProvider:
            return self.modelProvider
        if self.modelName in SUPPORTED_MODELS:
            return SUPPORTED_MODELS[self.modelName]
        logger.error(
            f"Model '{self.modelName}' not supported. Add it to SUPPORTED_MODELS."
        )
        raise LLMException(LLMException.ErrorCode.Model_Not_Found)


llm_settings = LLMSettings()
