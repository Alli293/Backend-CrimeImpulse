"""Celery tasks for crime news processing."""

import asyncio
from typing import Any

from celery import Task
from sqlalchemy.orm import Session

from app.features.crime_news.repository import get_scraped_article_repository
from app.features.crime_news.schemas import CrimeNewsRequest
from app.features.crime_news.service import get_crime_news_service
from app.infrastructure.celery_app import celery_app
from app.infrastructure.database import SessionLocal


class DatabaseTask(Task):
    """Base task with database session management."""

    _db: Session | None = None

    @property
    def db(self) -> Session:
        """Get database session."""
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(
        self,
        status: str,
        retval: Any,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Any,
    ) -> None:
        """Close database session after task completes."""
        if self._db is not None:
            self._db.close()
            self._db = None


@celery_app.task(bind=True, base=DatabaseTask, name="process_single_article")
def process_single_article(self: DatabaseTask, article_id: int) -> dict[str, Any]:
    """Process a single scraped article with LLM.

    Args:
        article_id: Database ID of the scraped article

    Returns:
        Dict with processing result: {
            "article_id": int,
            "success": bool,
            "error": str | None
        }
    """
    from app.features.crime_news.models import ScrapedArticleModel

    repository = get_scraped_article_repository(self.db)
    crime_news_service = get_crime_news_service()

    # Get article
    article = (
        self.db.query(ScrapedArticleModel)
        .filter(ScrapedArticleModel.id == article_id)
        .first()
    )

    if not article:
        return {
            "article_id": article_id,
            "success": False,
            "error": "Article not found",
        }

    # Skip if already processed
    if article.is_processed:
        return {
            "article_id": article_id,
            "success": True,
            "error": "Already processed",
        }

    # Skip if no content
    if not article.full_content or not article.full_content.strip():
        return {
            "article_id": article_id,
            "success": False,
            "error": "No content available",
        }

    try:
        # Create request
        request = CrimeNewsRequest(
            url=article.url,
            article_text=article.full_content,
            medium=article.source,
            publication_date=article.publication_date,
        )

        # Analyze with LLM (run async function in sync context)
        analysis = asyncio.run(crime_news_service.analyze_article(request))

        # Save results
        repository.save_analyzed_article(
            analysis=analysis,
            scraped_article_id=article.id,
        )

        # Mark as processed
        repository.mark_as_processed(article.id)

        return {
            "article_id": article_id,
            "success": True,
            "error": None,
        }

    except Exception as e:
        return {
            "article_id": article_id,
            "success": False,
            "error": str(e),
        }


@celery_app.task(bind=True, base=DatabaseTask, name="process_unprocessed_batch")
def process_unprocessed_batch(self: DatabaseTask, limit: int = 10) -> dict[str, Any]:
    """Process a batch of unprocessed articles synchronously (one at a time).

    Processes articles sequentially to avoid overloading the local LLM.

    Args:
        limit: Maximum number of articles to process

    Returns:
        Dict with batch processing results: {
            "total": int,
            "successful": int,
            "failed": int,
            "results": list[dict]
        }
    """
    repository = get_scraped_article_repository(self.db)

    # Get unprocessed articles
    unprocessed = repository.get_unprocessed_articles(limit=limit)

    if not unprocessed:
        return {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "results": [],
        }

    results = []
    successful = 0
    failed = 0

    # Process each article synchronously
    for article in unprocessed:
        # Update task state to show progress
        self.update_state(
            state="PROCESSING",
            meta={
                "current": len(results) + 1,
                "total": len(unprocessed),
                "article_id": article.id,
            },
        )

        # Process the article
        result = process_single_article(article.id)
        results.append(result)

        if result["success"]:
            successful += 1
        else:
            failed += 1

    return {
        "total": len(unprocessed),
        "successful": successful,
        "failed": failed,
        "results": results,
    }
