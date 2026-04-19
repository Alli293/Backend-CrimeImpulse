# Multi-stage build for optimized Python FastAPI application
# Stage 1: Base image with Python and UV package manager
FROM python:3.13-slim AS base

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Stage 2: Dependencies installation
FROM base AS deps

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install production dependencies only using UV
RUN uv sync --frozen --no-dev --no-cache

# Stage 3: Development environment (optional, for local dev)
FROM base AS development

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install all dependencies including dev tools
RUN uv sync --frozen --no-cache

# Copy application code
COPY . .

# Expose port for development
EXPOSE 8000

# Development command with hot reload
CMD ["uv", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

# Stage 4: Production build
FROM base AS builder

WORKDIR /app

# Copy dependency files and install
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-cache

# Copy application code
COPY app ./app
COPY alembic ./alembic
COPY LICENSE ./

# Stage 5: Final production runtime
FROM python:3.13-slim AS production

# Security: Create non-root user
RUN groupadd -g 1001 -r appgroup && \
    useradd -r -u 1001 -g appgroup appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment and application from builder
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/app /app/app
COPY --from=builder --chown=appuser:appgroup /app/alembic /app/alembic

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
