"""LLM client infrastructure."""

from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from pydantic import SecretStr

from app.core.config import settings


class LLMClient:
    """LLM client wrapper for language model operations."""

    def __init__(self):
        """Initialize the LLM client."""
        self._langfuse_handler = CallbackHandler()
        self._model = ChatOpenAI(
            model=settings.genai_model,
            base_url=settings.genai_base_url,
            api_key=SecretStr(settings.genai_api_key or "EMPTY"),
            temperature=settings.llm_temperature,
            top_p=settings.llm_top_p,
            presence_penalty=settings.llm_presence_penalty,
            extra_body={
                "top_k": 20,
                "repetition_penalty": 1.0,
            },
        )

    @property
    def model(self) -> ChatOpenAI:
        """Get the configured language model.

        Returns:
            Configured ChatOpenAI model instance
        """
        return self._model

    @property
    def langfuse_handler(self) -> CallbackHandler:
        """Get the langfuse callback handler.

        Returns:
            Configured CallbackHandler instance
        """
        return self._langfuse_handler


llm_client = LLMClient()


def get_llm_client() -> LLMClient:
    """Dependency injection function for LLM client.

    Returns:
        The singleton LLM client instance
    """
    return llm_client
