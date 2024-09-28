from typing import Type

from langchain_core.language_models.chat_models import BaseChatModel
from langfoundation.modelhub.chat.base import BaseChatModelProvider


try:
    from langchain_mistralai.chat_models import ChatMistralAI  # type: ignore[unused-ignore] # noqa: F401
except ImportError:
    raise ImportError("langchain_mistralai library is not installed. Please install `poetry add langchain-mistralai`.")


class MistralModelProvider(BaseChatModelProvider):
    """
    Provider for the Mistral Chat models.
    """

    M_NEMO = "open-mistral-nemo"
    M_SMALL = "mistral-small-latest"
    M_LARGE = "mistral-large-latest"

    @property
    def provider(self) -> Type[BaseChatModel]:
        return ChatMistralAI

    @property
    def has_structured_output(self) -> bool:
        return True

    @property
    def has_json_mode(self) -> bool:
        return True
