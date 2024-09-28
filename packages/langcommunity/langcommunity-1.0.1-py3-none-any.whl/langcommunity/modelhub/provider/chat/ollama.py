from typing import Type

from langchain_core.language_models.chat_models import BaseChatModel
from langfoundation.modelhub.chat.base import BaseChatModelProvider


try:
    from langchain_community.chat_models import ChatOllama  # type: ignore[unused-ignore] # noqa: F401
except ImportError:
    raise ImportError("ChatOllama library is not installed. Please install `poetry add langchain-ollama`.")


class OllamaModelProvider(BaseChatModelProvider):
    """
    Provider for the Ollama Chat models.
    """

    M_NEMO = "mistral-nemo"

    @property
    def provider(self) -> Type[BaseChatModel]:
        return ChatOllama

    @property
    def has_structured_output(self) -> bool:
        return True

    @property
    def has_json_mode(self) -> bool:
        return True
