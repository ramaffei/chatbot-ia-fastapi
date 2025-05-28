import logging
from typing import Optional

from exceptions.llm import LLMException
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.llm_supported_models import SUPPORTED_MODELS

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

    @model_validator(mode="after")
    def set_provider(self):
        if not self.modelProvider:
            if self.modelName in SUPPORTED_MODELS:
                self.modelProvider = SUPPORTED_MODELS[self.modelName]
            else:
                logger.error(
                    f"Model '{self.modelName}' not supported. Add it to SUPPORTED_MODELS."
                )
                raise LLMException(LLMException.ErrorCode.Model_Not_Found)
        return self


llm_settings = LLMSettings()
