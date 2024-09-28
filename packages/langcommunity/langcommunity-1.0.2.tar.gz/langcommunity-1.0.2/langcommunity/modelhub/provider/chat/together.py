from typing import Type

from langchain_core.language_models.chat_models import BaseChatModel
from langfoundation.modelhub.chat.base import BaseChatModelProvider


try:
    from langchain_together import ChatTogether  # type: ignore[unused-ignore] # noqa: F401
except ImportError:
    raise ImportError("langchain_together library is not installed. Please install `poetry add langchain-together`.")


class TogetherModelProvider(BaseChatModelProvider):
    """
    Provider for the Together Chat models.
    """

    M_8X7B_INSTRUCT_V0_3 = "mistralai/Mistral-7B-Instruct-v0.3"

    @property
    def provider(self) -> Type[BaseChatModel]:
        return ChatTogether

    @property
    def has_structured_output(self) -> bool:
        # NOTE: MAYBE NOT ALL MODEL
        return True

    @property
    def has_json_mode(self) -> bool:
        return True
