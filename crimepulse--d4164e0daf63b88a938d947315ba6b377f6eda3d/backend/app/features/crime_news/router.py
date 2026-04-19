"""API routes for crime news feature."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.features.crime_news.repository import get_scraped_article_repository
from app.features.crime_news.schemas import (
    CrimeNewsRequest,
    CrimeNewsResponse,
)
from app.features.crime_news.scraper import LaNacionCrimeScraper
from app.features.crime_news.service import CrimeNewsService, get_crime_news_service
from app.features.crime_news.tasks import process_unprocessed_batch
from app.infrastructure.celery_app import celery_app
from app.infrastructure.database import get_db

router = APIRouter(prefix="/crime-news", tags=["crime-news"])


class ScrapeResponse(BaseModel):
    """Response for scraping operation."""

    total_scraped: int
    new_articles: int
    duplicates: int
    source: str


class ProcessResponse(BaseModel):
    """Response for batch processing operation."""

    total_processed: int
    successful: int
    failed: int
    errors: list[str]


class TaskResponse(BaseModel):
    """Response for async task submission."""

    task_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    """Response for task status check."""

    task_id: str
    status: str
    result: dict | None = None
    progress: dict | None = None


@router.post("/scrape/la-nacion")
def scrape_la_nacion_articles(
    db: Annotated[Session, Depends(get_db)],
    max_articles: Annotated[int, Query(ge=1, le=200)] = 100,
    fetch_full_content: Annotated[bool, Query()] = True,
) -> ScrapeResponse:
    """Scrape crime news articles from La Nación and save to database.

    Args:
        max_articles: Maximum number of articles to scrape (1-200, default: 100)
        fetch_full_content: Whether to fetch full article text (default: True)
        db: Database session

    Returns:
        Summary of scraping operation

    Raises:
        HTTPException: If scraping fails
    """
    try:
        # Scrape articles
        scraper = LaNacionCrimeScraper()
        articles = scraper.scrape_articles_with_pagination(
            max_articles=max_articles,
            fetch_full_content=fetch_full_content,
        )

        # Save to database
        repository = get_scraped_article_repository(db)
        created, skipped = repository.bulk_create_if_not_exists(
            articles, source="La Nación"
        )

        return ScrapeResponse(
            total_scraped=len(articles),
            new_articles=created,
            duplicates=skipped,
            source="La Nación",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to scrape articles: {e!s}",
        ) from e


@router.post("/analyze")
async def analyze_crime_news(
    request: CrimeNewsRequest,
    crime_news_service: Annotated[CrimeNewsService, Depends(get_crime_news_service)],
) -> CrimeNewsResponse:
    """Analyze a crime news article and extract structured information.

    Args:
        request: The article text and metadata
        crime_news_service: The service to analyze crime news articles

    Returns:
        Structured crime news data including location, crime type, and description

    Raises:
        HTTPException: If analysis fails
    """
    try:
        return await crime_news_service.analyze_article(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze article: {e!s}",
        ) from e


@router.post("/process-unprocessed")
def process_unprocessed_articles(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> TaskResponse:
    """Trigger async processing of unprocessed articles with Celery.

    Articles are processed synchronously (one at a time) in a background worker
    to avoid overloading the local LLM. Use the /tasks/{task_id} endpoint to
    check processing status and results.

    Args:
        limit: Maximum number of articles to process (1-100, default: 10)

    Returns:
        Task ID and status for tracking the background job

    Raises:
        HTTPException: If task submission fails
    """
    try:
        # Submit Celery task
        task = process_unprocessed_batch.apply_async(args=[limit])

        return TaskResponse(
            task_id=task.id,
            status="PENDING",
            message=(
                f"Processing task submitted. {limit} articles will be "
                "processed synchronously."
            ),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit processing task: {e!s}",
        ) from e


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str) -> TaskStatusResponse:
    """Check the status of a background processing task.

    Args:
        task_id: The Celery task ID returned from /process-unprocessed

    Returns:
        Task status, progress, and results (if complete)

    Raises:
        HTTPException: If task not found or error occurs
    """
    try:
        task_result = celery_app.AsyncResult(task_id)

        response = TaskStatusResponse(
            task_id=task_id,
            status=task_result.status,
        )

        # Add progress info for running tasks
        if task_result.state == "PROCESSING":
            response.progress = task_result.info

        # Add results for completed tasks
        elif task_result.state == "SUCCESS":
            response.result = task_result.result

        # Add error info for failed tasks
        elif task_result.state == "FAILURE":
            response.result = {"error": str(task_result.info)}

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task status: {e!s}",
        ) from e
