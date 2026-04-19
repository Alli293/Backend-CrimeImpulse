"""Service layer for crime news analysis."""

import json
from dataclasses import asdict
from typing import cast

from langchain_core.prompts import ChatPromptTemplate
from pydantic import ValidationError

from app.features.crime_news.schemas import (
    CrimeNewsInferInfo,
    CrimeNewsRequest,
    CrimeNewsResponse,
)
from app.infrastructure.llm.client import LLMClient, get_llm_client


class CrimeNewsService:
    """Service for analyzing crime news articles using LLM."""

    def __init__(self, llm_client: LLMClient):
        """Initialize the crime news service.

        Args:
            llm_client: The LLM client for language model operations
        """
        self.llm_client = llm_client

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un asistente de extracción de datos "
                    "estructurados para una base de datos de noticias "
                    "de crimen. Extrae información de artículos "
                    "periodísticos en español y devuélvela como JSON "
                    "estructurado.\n\n"
                    "REGLAS ESTRICTAS:\n"
                    "- 'location' DEBE usar únicamente nombres de "
                    "provincias y cantones de Costa Rica. Si la "
                    "ubicación está fuera de Costa Rica o no es "
                    "reconocible, establécela en None\n"
                    "- 'crime_type' DEBE ser uno de los valores del "
                    "enum permitidos.\n"
                    "- NO inventes campos. Solo devuelve los campos "
                    "definidos en el esquema.",
                ),
                (
                    "human",
                    "Artículo de noticias:\n{article}\n\n"
                    "Extrae los campos estructurados.",
                ),
            ]
        )

        self.chain = self.prompt | self.llm_client.model.with_structured_output(
            CrimeNewsInferInfo
        )

    def _map_inferred_data_to_response(
        self, request: CrimeNewsRequest, inferred_data: str
    ) -> CrimeNewsResponse:
        try:
            inferred_data_to_json = json.loads(
                inferred_data
            )  # Convert to JSON string for validation
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM response is not valid JSON: {inferred_data}") from e

        crime_news_inferred = CrimeNewsInferInfo(**inferred_data_to_json)

        return CrimeNewsResponse(
            url=request.url,
            medium=request.medium,
            publication_date=request.publication_date,
            **asdict(crime_news_inferred),
        )

    async def analyze_article(self, request: CrimeNewsRequest) -> CrimeNewsResponse:
        """Analyze a crime news article and extract structured data.

        Args:
            request: The crime news request containing article text

        Returns:
            Structured crime news data
        """
        try:
            response = cast(
                str,
                await self.chain.ainvoke(
                    {"article": request.article_text},
                    config={"callbacks": [self.llm_client.langfuse_handler]},
                ),
            )
            return self._map_inferred_data_to_response(request, response)

        except ValidationError as e:
            raise ValueError(f"LLM response validation failed: {e.errors()}") from e
        except RuntimeError as e:
            raise RuntimeError(f"LLM invocation failed: {e}") from e


# Singleton instance
crime_news_service = CrimeNewsService(get_llm_client())


def get_crime_news_service() -> CrimeNewsService:
    """Dependency injection function for crime news service.

    Returns:
        The singleton crime news service instance
    """
    return crime_news_service
