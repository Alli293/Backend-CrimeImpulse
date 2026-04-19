"""Database configuration and session management."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from alembic import command
from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


DATABASE_URL = f"postgresql+psycopg2://{settings.supabase_user}:{settings.supabase_password}@{settings.supabase_host}:{settings.supabase_port}/{settings.supabase_database}?sslmode=require"

engine = create_engine(DATABASE_URL)

session = sessionmaker(engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Dependency for database sessions."""
    db = session()
    try:
        print("Database session created")
        yield db
    finally:
        db.close()


def run_migrations() -> None:
    """Run Alembic migrations programmatically."""
    # Get the backend directory (where alembic.ini is located)
    backend_dir = Path(__file__).parent.parent.parent

    alembic_cfg = Config(str(backend_dir / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))

    # Override the database URL
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    print("Running database migrations...")
    command.upgrade(alembic_cfg, "head")
    print("✓ Migrations completed successfully")


if __name__ == "__main__":
    print("Testing database connection and migrations...")
    try:
        # Test database connection
        with get_db() as db:
            print("✓ Database connection successful!")

        # Test migrations
        run_migrations()

    except Exception as e:
        print(f"✗ Error: {e}")
