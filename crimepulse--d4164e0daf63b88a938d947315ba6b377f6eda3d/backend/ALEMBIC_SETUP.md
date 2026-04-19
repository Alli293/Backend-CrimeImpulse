# Alembic Database Migrations Setup

This document describes how Alembic is configured in this project for automatic database migrations.

## Overview

Alembic is configured to:

- Automatically detect model changes via autogenerate
- Run migrations on application startup
- Work with Supabase PostgreSQL database
- Support both local development and Docker deployments

## Configuration Steps

### 1. Database Base Class Setup

Added SQLAlchemy declarative base to `app/infrastructure/database.py`:

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all database models."""
    pass
```

All models inherit from this base class:

```python
from app.infrastructure.database import Base

class MyModel(Base):
    __tablename__ = "my_table"
    # ... fields
```

### 2. Alembic Environment Configuration

Modified `alembic/env.py` to enable autogenerate:

**Key changes:**

- Import the `Base` class and all models
- Set `target_metadata = Base.metadata` (enables autogenerate)
- Configure database URL from settings (supports environment variables)
- Import all model files so Alembic can detect them

```python
from app.core.config import settings
from app.infrastructure.database import Base

# Import all models so Alembic can detect them
from app.features.crime_news.models import CrimeNewsModel, ScrapedArticleModel

# Configure database URL from settings
DATABASE_URL = f"postgresql+psycopg2://{settings.supabase_user}:{settings.supabase_password}@{settings.supabase_host}:{settings.supabase_port}/{settings.supabase_database}?sslmode=require"
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Enable autogenerate
target_metadata = Base.metadata
```

### 3. Programmatic Migration Runner

Added `run_migrations()` function to `app/infrastructure/database.py`:

```python
from pathlib import Path
from alembic import command
from alembic.config import Config

def run_migrations() -> None:
    """Run Alembic migrations programmatically."""
    backend_dir = Path(__file__).parent.parent.parent

    alembic_cfg = Config(str(backend_dir / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    print("Running database migrations...")
    command.upgrade(alembic_cfg, "head")
    print("✓ Migrations completed successfully")
```

### 4. FastAPI Integration

Integrated migrations into FastAPI startup in `app/main.py`:

```python
from contextlib import asynccontextmanager
from app.infrastructure.database import run_migrations

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Run database migrations
    run_migrations()
    yield
    # Shutdown (cleanup if needed)

app = FastAPI(
    title=settings.app_name,
    # ... other config
    lifespan=lifespan,
)
```

## Usage

### Development Workflow

#### 1. Create or Modify Models

Edit your SQLAlchemy models in `app/features/*/models.py`:

```python
from app.infrastructure.database import Base
from sqlalchemy import Column, Integer, String

class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
```

#### 2. Generate Migration

Alembic will automatically detect changes:

```bash
cd backend
alembic revision --autogenerate -m "add my_table"
```

This creates a new migration file in `alembic/versions/`.

#### 3. Review Migration

Check the generated migration file:

```bash
cat alembic/versions/<revision_id>_add_my_table.py
```

Verify the `upgrade()` and `downgrade()` functions are correct.

#### 4. Test Migration

Run the test script to verify migrations work:

```bash
python -m app.infrastructure.database
```

Or start your FastAPI app (migrations run automatically):

```bash
uvicorn app.main:app --reload
```

#### 5. Commit Migration

Add the migration file to git:

```bash
git add alembic/versions/<revision_id>_add_my_table.py
git commit -m "feat: add my_table migration"
```

### Manual Migration Commands

#### Check Current Version

```bash
alembic current
```

#### View Migration History

```bash
alembic history
```

#### Upgrade to Specific Revision

```bash
alembic upgrade <revision_id>
```

#### Downgrade One Revision

```bash
alembic downgrade -1
```

#### Rollback All Migrations

```bash
alembic downgrade base
```

## Docker Deployment

### Automatic Migrations on Startup

Migrations run automatically when the FastAPI app starts:

1. Docker builds the image with migration files included
2. Container starts and runs `app/main.py`
3. FastAPI `lifespan` event calls `run_migrations()`
4. Alembic applies any pending migrations
5. App becomes ready to serve requests

### No Additional Configuration Needed

- **Docker Compose**: No changes needed, migrations run automatically
- **Dockerfile**: No special commands needed, migration files are part of the build
- **Environment Variables**: Database credentials from `.env` or docker-compose environment

## Adding New Models

When adding a new feature with models:

1. **Create the model file**: `app/features/my_feature/models.py`
2. **Import in `alembic/env.py`**: Add to the imports section

   ```python
   from app.features.my_feature.models import MyFeatureModel  # noqa: F401
   ```

3. **Generate migration**: `alembic revision --autogenerate -m "add my_feature tables"`
4. **Test and commit**

## Troubleshooting

### Migrations Don't Detect Changes

**Problem**: `alembic revision --autogenerate` creates empty migration

**Solutions**:

1. Ensure model is imported in `alembic/env.py`
2. Verify model inherits from `Base`
3. Check `target_metadata = Base.metadata` is set in `alembic/env.py`

### Database Connection Errors

**Problem**: `connection to server failed` or `Network is unreachable`

**Solutions**:

1. Check environment variables are set correctly (`.env` file)
2. For Supabase IPv6 issues in WSL2, verify you're using the connection pooler port (6543) or that IPv6 is configured
3. Verify database credentials are correct

### Circular Import Errors

**Problem**: `ImportError` when running migrations

**Solutions**:

1. Ensure `run_migrations()` is not called at module import time in `database.py`
2. Only call `run_migrations()` from `main.py` lifespan event
3. Check for circular dependencies between models

### Empty or Incorrect Migrations

**Problem**: Migration file has `pass` in `upgrade()` function

**Solutions**:

1. Delete the empty migration file
2. Verify all models are imported in `alembic/env.py`
3. Re-run `alembic revision --autogenerate`

## Security Considerations

### Supabase-Specific

When creating tables via migrations, remember to:

1. **Enable RLS** on all tables in the `public` schema:

   ```sql
   ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;
   ```

2. **Create appropriate policies**:

   ```sql
   CREATE POLICY "Users can read own data"
   ON my_table FOR SELECT
   USING (auth.uid() = user_id);
   ```

3. **Never expose `service_role` key** in application code

### Migration Safety

- **Review all generated migrations** before applying to production
- **Test migrations on a copy** of production data first
- **Keep downgrade functions** working for rollback capability
- **Use transactions** (Alembic does this by default for DDL)

## Best Practices

1. **Descriptive migration names**: Use clear, meaningful messages
   - ✅ `alembic revision --autogenerate -m "add user_email_index"`
   - ❌ `alembic revision --autogenerate -m "update"`

2. **One logical change per migration**: Don't mix unrelated changes

3. **Review before committing**: Always review generated SQL

4. **Test both directions**: Verify `upgrade()` and `downgrade()` work

5. **Commit migrations with code**: Migration files are part of your codebase

6. **Never edit applied migrations**: Create a new migration to fix issues

## Files Modified

- `app/infrastructure/database.py` - Added `Base` class and `run_migrations()`
- `alembic/env.py` - Configured autogenerate and database connection
- `app/main.py` - Added lifespan event to run migrations on startup
- `app/core/config.py` - Database settings (already existed)

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [Supabase Database Migrations](https://supabase.com/docs/guides/database/migrations)
