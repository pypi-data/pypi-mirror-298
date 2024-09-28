import logging
from typing import Any, List, Tuple, Type, Union

from langchain_community.cross_encoders.base import BaseCrossEncoder

from langfoundation.modelhub.rerank.base import BaseRerankModel, BaseRerankProvider


logger = logging.getLogger(__name__)


try:
    from cohere.client import Client as CohereClient  # type: ignore[unused-ignore] # noqa: F401
except ImportError:
    raise ImportError()


class RerankCohere(BaseRerankModel):
    """Interface for cross encoder models."""

    client: Union[
        Type[CohereClient],
        Type[Any],
    ]
    model_name: str

    def rerank(
        self,
        query: str,
        docs: List[str],
    ) -> List[Tuple[int, float]]:
        with self.client() as client:
            response = client.rerank(
                model=self.model_name,
                query=query,
                documents=docs,
                top_n=self.top_n,
            )

        return [(result.index, result.relevance_score) for result in response.results]


class CohereRerankProvider(BaseRerankProvider):
    RERANK_ENGLISH_V3 = "rerank-english-v3.0"

    @property
    def provider(
        self,
    ) -> Union[
        Type[BaseCrossEncoder],
        Type[Any],
    ]:
        return CohereClient

    def model(
        self,
        top_n: int,
    ) -> BaseRerankModel:
        return RerankCohere(
            top_n=top_n,
            model_name=self.value,
            client=self.provider,
        )
