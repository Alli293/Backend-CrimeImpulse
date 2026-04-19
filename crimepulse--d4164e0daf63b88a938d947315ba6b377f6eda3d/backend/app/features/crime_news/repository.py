"""Repository for crime news database operations."""

from datetime import UTC, datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.features.crime_news.models import CrimeNewsModel, ScrapedArticleModel
from app.features.crime_news.schemas import CrimeNewsResponse
from app.features.crime_news.scraper import ScrapedArticle


class ScrapedArticleRepository:
    """Repository for scraped article database operations."""

    def __init__(self, db: Session) -> None:
        """Initialize the repository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create_scraped_article(
        self, article: ScrapedArticle, source: str = "La Nación"
    ) -> ScrapedArticleModel:
        """Create a new scraped article in the database.

        Args:
            article: ScrapedArticle from scraper
            source: News source name

        Returns:
            Created ScrapedArticleModel instance
        """
        db_article = ScrapedArticleModel(
            article_id=article.article_id,
            title=article.title,
            url=article.url,
            description=article.description,
            publication_date=article.publication_date,
            image_url=article.image_url,
            full_content=article.full_content,
            source=source,
        )

        self.db.add(db_article)
        self.db.commit()
        self.db.refresh(db_article)

        return db_article

    def get_by_article_id(self, article_id: str) -> ScrapedArticleModel | None:
        """Get scraped article by article_id.

        Args:
            article_id: Unique article identifier

        Returns:
            ScrapedArticleModel if found, None otherwise
        """
        return (
            self.db.query(ScrapedArticleModel)
            .filter(ScrapedArticleModel.article_id == article_id)
            .first()
        )

    def get_by_url(self, url: str) -> ScrapedArticleModel | None:
        """Get scraped article by URL.

        Args:
            url: Article URL

        Returns:
            ScrapedArticleModel if found, None otherwise
        """
        return (
            self.db.query(ScrapedArticleModel)
            .filter(ScrapedArticleModel.url == url)
            .first()
        )

    def get_unprocessed_articles(self, limit: int = 100) -> list[ScrapedArticleModel]:
        """Get unprocessed scraped articles.

        Args:
            limit: Maximum number of articles to return

        Returns:
            List of unprocessed ScrapedArticleModel instances
        """
        return (
            self.db.query(ScrapedArticleModel)
            .filter(ScrapedArticleModel.is_processed == False)  # noqa: E712
            .limit(limit)
            .all()
        )

    def mark_as_processed(self, article_id: int) -> None:
        """Mark a scraped article as processed.

        Args:
            article_id: Database ID of the article
        """
        article = (
            self.db.query(ScrapedArticleModel)
            .filter(ScrapedArticleModel.id == article_id)
            .first()
        )

        if article:
            article.is_processed = True
            article.processed_at = datetime.now(UTC)
            self.db.commit()

    def article_exists(self, article_id: str) -> bool:
        """Check if an article already exists in the database.

        Args:
            article_id: Unique article identifier

        Returns:
            True if article exists, False otherwise
        """
        return (
            self.db.query(ScrapedArticleModel)
            .filter(ScrapedArticleModel.article_id == article_id)
            .count()
            > 0
        )

    def bulk_create_if_not_exists(
        self, articles: list[ScrapedArticle], source: str = "La Nación"
    ) -> tuple[int, int]:
        """Bulk create scraped articles, skipping duplicates idempotently.

        Uses PostgreSQL's INSERT ... ON CONFLICT DO NOTHING to handle duplicates
        at the database level based on article_id unique constraint. This ensures
        true idempotency even with concurrent requests.

        Args:
            articles: List of ScrapedArticle from scraper
            source: News source name

        Returns:
            Tuple of (created_count, skipped_count)
        """
        if not articles:
            return 0, 0

        # Prepare article data for bulk insert
        article_data = [
            {
                "article_id": article.article_id,
                "title": article.title,
                "url": article.url,
                "description": article.description,
                "publication_date": article.publication_date,
                "image_url": article.image_url,
                "full_content": article.full_content,
                "source": source,
            }
            for article in articles
        ]

        # Use PostgreSQL's INSERT ... ON CONFLICT DO NOTHING
        stmt = pg_insert(ScrapedArticleModel).values(article_data)
        stmt = stmt.on_conflict_do_nothing(index_elements=["article_id"])

        result = self.db.execute(stmt)
        self.db.commit()

        # rowcount gives us the number of rows actually inserted
        created = result.rowcount
        skipped = len(articles) - created

        return created, skipped

    def save_analyzed_article(
        self, analysis: CrimeNewsResponse, scraped_article_id: int
    ) -> CrimeNewsModel:
        """Save analyzed crime news to database.

        Args:
            analysis: The analyzed crime news data from LLM
            scraped_article_id: ID of the source scraped article

        Returns:
            Created CrimeNewsModel instance
        """
        db_crime_news = CrimeNewsModel(
            title=analysis.title,
            medium=analysis.medium,
            url=analysis.url,
            publication_date=analysis.publication_date,
            location=analysis.location.model_dump() if analysis.location else None,
            specific_location=analysis.specific_location,
            crime_type=analysis.crime_type,
            description=analysis.description,
            scraped_article_id=scraped_article_id,
        )

        self.db.add(db_crime_news)
        self.db.commit()
        self.db.refresh(db_crime_news)

        return db_crime_news


def get_scraped_article_repository(db: Session) -> ScrapedArticleRepository:
    """Get scraped article repository instance.

    Args:
        db: SQLAlchemy database session

    Returns:
        ScrapedArticleRepository instance
    """
    return ScrapedArticleRepository(db)
