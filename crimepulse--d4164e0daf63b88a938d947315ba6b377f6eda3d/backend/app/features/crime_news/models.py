"""Database models for crime news feature."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON

from app.infrastructure.database import Base


class ScrapedArticleModel(Base):
    """SQLAlchemy model for raw scraped news articles."""

    __tablename__ = "scraped_articles"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(String(500), unique=True, nullable=False, index=True)
    title = Column(String(1000), nullable=False)
    url = Column(String(2000), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    publication_date = Column(DateTime, nullable=True)
    image_url = Column(String(2000), nullable=True)
    full_content = Column(Text, nullable=True)
    source = Column(String(200), nullable=False, default="La Nación")

    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )


class CrimeNewsModel(Base):
    """SQLAlchemy model for analyzed crime news articles."""

    __tablename__ = "crime_news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1000), nullable=False)
    medium = Column(String(200), nullable=False)
    url = Column(String(2000), nullable=True)
    publication_date = Column(DateTime, nullable=True)

    # Location stored as JSON for flexibility with the complex structure
    location = Column(JSON, nullable=True)
    specific_location = Column(String(500), nullable=True)

    crime_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    # Link to source scraped article
    scraped_article_id = Column(Integer, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
