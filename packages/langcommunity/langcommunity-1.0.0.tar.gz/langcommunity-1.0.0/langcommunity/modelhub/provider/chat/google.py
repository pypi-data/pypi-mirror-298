from typing import Any, Dict, Optional, Type

from langchain_core.language_models.chat_models import BaseChatModel
from langfoundation.modelhub.chat.base import BaseChatModelProvider


try:
    from langchain_google_vertexai import (  # type: ignore[unused-ignore] # noqa: F401
        ChatVertexAI,  # type: ignore[unused-ignore] # noqa: F401
        HarmBlockThreshold,
        HarmCategory,
    )
except ImportError:
    raise ImportError("langchain_google_vertexai library is not installed. Please install `poetry update --with google`.")


class GoogleChatModelProvider(BaseChatModelProvider):
    """
    Provider for the Google Chat models.
    """

    GEMINI_1_5 = "gemini-1.5-pro-preview-0409"

    @property
    def provider(self) -> Type[BaseChatModel]:
        """The type of the chat model provider."""
        return ChatVertexAI

    @property
    def has_structured_output(self) -> bool:
        return True

    @property
    def has_json_mode(self) -> bool:
        return False

    def _config(
        self,
        temperature: float = 0.7,
        top_p: float = 1,
        max_tokens: Optional[int] = None,
        streaming: bool = True,
        extra_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        config: Dict[str, Any] = {}
        match self.value:
            case self.GEMINI_1_5:
                return {
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_output_tokens": max_tokens,  # "4096",
                    "model_name": "gemini-1.5-pro-preview-0409",
                    "streaming": streaming,
                    # Note: can be pass as extra config in ChatModelConfig (too see)
                    "project": "pred-techeval-sb-01-0ce36d94",
                    # Note: can be pass as max_tokens config in ChatModelConfig (too see)
                    "safety_config": {
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    },
                }
            case _:
                raise NotImplementedError

        config.update(extra_config or {})
        return config
