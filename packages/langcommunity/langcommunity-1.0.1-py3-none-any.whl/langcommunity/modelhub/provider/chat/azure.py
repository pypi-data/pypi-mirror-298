from typing import Any, Dict, Optional, Type

from langchain_core.language_models.chat_models import BaseChatModel
from langfoundation.modelhub.chat.base import BaseChatModelProvider


try:
    from langchain_openai import AzureChatOpenAI  # type: ignore[unused-ignore] # noqa: F401
except ImportError:
    raise ImportError("langchain_openai library is not installed. Please install `poetry add langchain-openai`.")


class AzureChatModelProvider(BaseChatModelProvider):
    """
    Provider for Azure Chat models.

    [Docs](https://python.langchain.com/docs/integrations/chat/azure_chat_openai/)
    TODO:::
                        "openai_api_key": os.environ["AZURE_OPENAI_API_KEY"],
                    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    """

    GPT4_32k = "GPT4_32k_2024-02-15-preview"

    @property
    def provider(self) -> Type[BaseChatModel]:
        return AzureChatOpenAI

    @property
    def has_structured_output(self) -> bool:
        return True

    @property
    def has_json_mode(self) -> bool:
        return True

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
            case self.GPT4_32k:
                config = {
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens,
                    "openai_api_version": "2024-02-15-preview",
                    "azure_deployment": "GPT4_32k2",
                    "streaming": streaming,
                }

        config.update(extra_config or {})
        return config
