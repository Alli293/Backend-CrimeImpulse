"""CrimePulse API - Main application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.features.crime_news import router as crime_news_router
from app.infrastructure.database import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Run database migrations
    run_migrations()
    yield
    # Shutdown (add cleanup here if needed)

app = FastAPI(
    title=settings.app_name,
    description="API for analyzing and tracking crime news in Costa Rica",
    version="1.0.0",
    docs_url="/docs",
    root_path="/api/v1",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include feature routers
app.include_router(crime_news_router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "app": settings.app_name,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
