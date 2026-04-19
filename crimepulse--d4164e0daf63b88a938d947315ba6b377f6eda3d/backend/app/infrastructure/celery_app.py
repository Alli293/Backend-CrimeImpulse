"""Celery application configuration."""

from celery import Celery

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "crimepulse",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=7200,  # 2 hours max per task
    task_soft_time_limit=7000,  # Soft limit at 1h 56m
    result_expires=86400,  # Results expire after 24 hours
    worker_prefetch_multiplier=1,  # Process one task at a time
    worker_max_tasks_per_child=50,  # Restart worker after 50 tasks
)

# Auto-discover tasks in features
celery_app.autodiscover_tasks(["app.features.crime_news"])
