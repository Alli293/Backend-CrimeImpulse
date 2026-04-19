# Celery Background Task Processing Guide

This guide explains how to use Celery for asynchronous background processing of scraped crime news articles.

## Overview

The system uses **Celery** with **Redis** as a message broker to process articles asynchronously. Articles are processed **synchronously** (one at a time) to avoid overloading the local LLM.

### Architecture

```
┌──────────────┐      ┌────────────┐      ┌─────────────┐
│   FastAPI    │─────▶│   Redis    │◀─────│   Celery    │
│   Backend    │      │  (Broker)  │      │   Worker    │
└──────────────┘      └────────────┘      └─────────────┘
       │                                          │
       │                                          │
       ▼                                          ▼
┌──────────────────────────────────────────────────────┐
│              PostgreSQL Database                      │
│  ┌─────────────────┐      ┌──────────────────┐      │
│  │ scraped_articles│─────▶│   crime_news     │      │
│  │  (raw data)     │      │ (analyzed data)  │      │
│  └─────────────────┘      └──────────────────┘      │
└──────────────────────────────────────────────────────┘
```

## Running with Docker Compose

### Production

Start all services including Celery worker:

```bash
docker-compose up -d
```

This starts:
- `crimepulse-backend` - FastAPI application
- `crimepulse-celery-worker` - Celery worker (1 concurrent task)
- `redis` - Message broker (shared with Langfuse)
- `crimepulse-postgres` - Database
- `langfuse-*` - Observability services

Check worker logs:

```bash
docker-compose logs -f crimepulse-celery-worker
```

### Development

Start with development configuration:

```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up
```

This enables:
- Hot reload for both FastAPI and Celery worker
- Debug ports exposed
- Source code mounted as volumes

## API Usage

### 1. Scrape Articles

First, scrape articles from La Nación:

```bash
curl -X POST "http://localhost:8000/crime-news/scrape/la-nacion?max_articles=50&fetch_full_content=true"
```

Response:
```json
{
  "total_scraped": 50,
  "new_articles": 45,
  "duplicates": 5,
  "source": "La Nación"
}
```

### 2. Process Articles with Celery

Trigger background processing:

```bash
curl -X POST "http://localhost:8000/crime-news/process-unprocessed?limit=10"
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PENDING",
  "message": "Processing task submitted. 10 articles will be processed synchronously."
}
```

### 3. Check Task Status

Monitor task progress:

```bash
curl "http://localhost:8000/crime-news/tasks/550e8400-e29b-41d4-a716-446655440000"
```

**While processing:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PROCESSING",
  "progress": {
    "current": 3,
    "total": 10,
    "article_id": 12345
  }
}
```

**When complete:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "SUCCESS",
  "result": {
    "total": 10,
    "successful": 8,
    "failed": 2,
    "results": [
      {"article_id": 1, "success": true, "error": null},
      {"article_id": 2, "success": false, "error": "No content available"}
    ]
  }
}
```

## Configuration

### Environment Variables

Add to `.env` file:

```bash
# Redis Configuration (shared with Langfuse)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_AUTH=myredissecret

# GenAI Configuration for LLM
GENAI_API_KEY=
GENAI_BASE_URL=http://172.18.16.1:8080/v1
GENAI_MODEL=unsloth/Qwen3.5-35B-A3B-GGUF:Q4_K_M
```

### Celery Worker Settings

Located in `app/infrastructure/celery_app.py`:

```python
celery_app.conf.update(
    worker_prefetch_multiplier=1,  # Process one task at a time
    task_time_limit=7200,           # 2 hours max per task
    worker_max_tasks_per_child=50,  # Restart after 50 tasks
)
```

## Monitoring

### View Celery Worker Status

```bash
# Docker
docker exec -it crimepulse-celery-worker celery -A app.infrastructure.celery_app:celery_app inspect active

# Local
celery -A app.infrastructure.celery_app:celery_app inspect active
```

### View Redis Queue

```bash
# Connect to Redis
docker exec -it redis redis-cli -a myredissecret

# Check queue length
LLEN celery

# View tasks
LRANGE celery 0 -1
```

### Task Results

Results are stored in Redis for 24 hours:

```bash
# Get task result
GET celery-task-meta-<task_id>
```

## Performance Considerations

### Processing Time

- **Average**: 2 minutes per article
- **10 articles**: ~20 minutes
- **50 articles**: ~100 minutes (1h 40m)
- **100 articles**: ~200 minutes (3h 20m)

### Concurrency

The worker is configured with `concurrency=1` to avoid overloading the local LLM:

```yaml
command: ["celery", "-A", "app.infrastructure.celery_app:celery_app", "worker", "--loglevel=info", "--concurrency=1"]
```

To process multiple batches in parallel, deploy multiple worker instances:

```bash
docker-compose up --scale crimepulse-celery-worker=3
```

⚠️ **Warning**: Only increase if your LLM server can handle parallel requests.

## Troubleshooting

### Worker Not Processing Tasks

1. Check worker is running:
   ```bash
   docker-compose ps crimepulse-celery-worker
   ```

2. Check worker logs:
   ```bash
   docker-compose logs -f crimepulse-celery-worker
   ```

3. Verify Redis connection:
   ```bash
   docker exec crimepulse-celery-worker env | grep REDIS
   ```

### Tasks Stuck in PENDING

- Worker might be down
- Redis connection issue
- Check worker can connect to database and LLM

### High Memory Usage

- Increase worker memory limit in docker-compose.yaml
- Reduce `worker_max_tasks_per_child` to restart worker more frequently
- Check for memory leaks in LLM client

### Task Timeout

Tasks timeout after 2 hours. If LLM is very slow:

1. Reduce batch size (`limit` parameter)
2. Increase `task_time_limit` in celery_app.py
3. Optimize LLM configuration

## Development

### Running Celery Worker Locally

```bash
# Install dependencies
uv sync

# Run worker with auto-reload
watchfiles --filter python "celery -A app.infrastructure.celery_app:celery_app worker --loglevel=info --concurrency=1" app
```

### Testing Tasks

```python
from app.features.crime_news.tasks import process_single_article

# Synchronous execution (for testing)
result = process_single_article(article_id=123)
print(result)
```

## Production Recommendations

1. **Monitor task failures**: Set up alerts for high failure rates
2. **Scale workers**: Add more workers during high traffic
3. **Database connection pooling**: Configure SQLAlchemy pool size
4. **LLM rate limiting**: Implement exponential backoff for LLM errors
5. **Dead letter queue**: Configure for permanently failed tasks
6. **Metrics**: Integrate Prometheus for Celery metrics
7. **Log aggregation**: Use ELK or similar for centralized logging

## Additional Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
