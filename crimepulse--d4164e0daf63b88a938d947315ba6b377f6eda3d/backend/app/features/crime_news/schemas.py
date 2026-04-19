"""Pydantic schemas for crime news feature."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.geolocations import LocationData
from app.shared.types import CrimeType


class CrimeNewsRequest(BaseModel):
    """Request schema for analyzing crime news articles."""

    url: str = Field(..., description="The URL of the news article")
    article_text: str = Field(..., description="The news article text to analyze")
    medium: str = Field(..., description="The news medium/source")
    publication_date: datetime = Field(
        ..., description="When the article was published"
    )


class CrimeNewsInferInfo(BaseModel):
    """Infered information from llm model."""

    model_config = ConfigDict(extra="forbid")

    title: str
    location: LocationData | None = Field(
        default=None,
        description="Provincia/cantón/distrito de Costa Rica donde ocurrió el crimen."
        " Debe ser None si la ubicación no puede identificarse a partir del artículo.",
    )
    specific_location: str | None = Field(
        default=None,
        description="Ubicación específica por ejemplo el nombre del lugar/edificio.",
    )
    crime_type: CrimeType
    description: str


class CrimeNewsResponse(BaseModel):
    """Response schema for crime news analysis."""

    model_config = ConfigDict(extra="forbid")

    title: str
    url: str
    medium: str
    publication_date: datetime
    location: LocationData | None = Field(
        default=None,
        description="Provincia/cantón/distrito de Costa Rica donde ocurrió el crimen."
        " Debe ser None si la ubicación no puede identificarse a partir del artículo.",
    )
    specific_location: str | None = Field(
        default=None,
        description="Ubicación específica por ejemplo el nombre del lugar/edificio.",
    )
    crime_type: CrimeType
    description: str
