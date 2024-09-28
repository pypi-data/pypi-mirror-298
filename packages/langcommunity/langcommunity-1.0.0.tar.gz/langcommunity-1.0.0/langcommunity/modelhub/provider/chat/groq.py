from typing import Type

from langchain_core.language_models.chat_models import BaseChatModel
from langfoundation.modelhub.chat.base import BaseChatModelProvider


try:
    from langchain_groq import ChatGroq  # type: ignore[unused-ignore] # noqa: F401
except ImportError:
    raise ImportError("langchain_groq library is not installed. Please install `poetry update --with groq`.")


class GroqModelProvider(BaseChatModelProvider):
    """
    Provider for the Groq Chat models.
    """

    LLAMA3_8b = "llama3-8b-8192"
    M_8X7B_INSTRUCT_V0_1 = "mixtral-8x7b-32768"

    @property
    def provider(self) -> Type[BaseChatModel]:
        return ChatGroq

    @property
    def has_structured_output(self) -> bool:
        return True

    @property
    def has_json_mode(self) -> bool:
        return True
