# Docker Deployment Guide - CrimePulse

This guide covers Docker containerization for the CrimePulse FastAPI backend with PostgreSQL database.

## Architecture Overview

The Docker setup includes:

1. **crimepulse-backend**: FastAPI application (Python 3.13)
2. **crimepulse-postgres**: Dedicated PostgreSQL 17 database with persistent volume
3. **langfuse-***: LLM observability stack (optional, for production monitoring)

### Network Architecture

```
├── frontend (network)
│   ├── crimepulse-backend:8000
│   └── langfuse-web:3000
├── backend (network)
│   ├── crimepulse-backend
│   └── crimepulse-postgres:5432
└── langfuse-network (internal)
    ├── langfuse-worker
    ├── langfuse-web
    ├── langfuse-postgres
    ├── clickhouse
    ├── redis
    └── minio
```

## Quick Start

### 1. Environment Setup

Copy the example environment file:

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Update these values
OPENAI_API_KEY="your-openai-api-key"
POSTGRES_PASSWORD="your-secure-password"
LANGFUSE_POSTGRES_PASSWORD="your-langfuse-password"
```

### 2. Start All Services

```bash
# From project root
docker-compose up -d
```

### 3. Start Only CrimePulse Services

```bash
# Start only backend and database
docker-compose up -d crimepulse-backend crimepulse-postgres
```

### 4. Check Service Health

```bash
# View running containers
docker-compose ps

# Check backend logs
docker-compose logs -f crimepulse-backend

# Check database logs
docker-compose logs -f crimepulse-postgres
```

### 5. Access Services

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Langfuse UI**: http://localhost:3000 (if running)

## Dockerfile Details

The multi-stage Dockerfile optimizes for:

### Production Build Features

- **Base Image**: Python 3.13-slim (minimal attack surface)
- **Package Manager**: UV (faster than pip, lockfile support)
- **Multi-stage Build**: Separates build and runtime dependencies
- **Security**:
  - Non-root user (UID 1001)
  - Minimal runtime dependencies
  - No unnecessary build tools in production
- **Health Checks**: Built-in health monitoring
- **Resource Limits**: CPU and memory constraints

### Build Stages

1. **base**: Python + UV installation
2. **deps**: Production dependencies only
3. **development**: All dependencies + hot reload (optional)
4. **builder**: Build artifacts
5. **production**: Minimal runtime image

## Development Workflow

### Local Development with Docker

Use the development target for hot reloading:

```bash
# Build development image
docker-compose -f docker-compose.dev.yml up --build

# Or target development stage
docker-compose build --target development crimepulse-backend
```

### Run Database Migrations

```bash
# Execute migrations inside container
docker-compose exec crimepulse-backend alembic upgrade head

# Or from host (requires backend running)
docker-compose exec crimepulse-backend uv run alembic upgrade head
```

### Access Database

```bash
# Connect to CrimePulse database
docker-compose exec crimepulse-postgres psql -U crimepulse -d crimepulse

# Or from host
psql postgresql://crimepulse:crimepulse_secure_password@localhost:5433/crimepulse
```

## Volume Management

### Persistent Volumes

Data persists across container restarts:

- **crimepulse_postgres_data**: CrimePulse application database
- **langfuse_postgres_data**: Langfuse observability database

### Backup Database

```bash
# Backup CrimePulse database
docker-compose exec crimepulse-postgres pg_dump -U crimepulse crimepulse > backup.sql

# Restore from backup
docker-compose exec -T crimepulse-postgres psql -U crimepulse crimepulse < backup.sql
```

### Reset Database (Development Only)

```bash
# WARNING: This deletes all data
docker-compose down -v
docker volume rm crimepulse_postgres_data
docker-compose up -d crimepulse-postgres
```

## Security Best Practices

### Change Default Credentials

Edit `docker-compose.yaml` or use environment variables:

```yaml
# In docker-compose.yaml or .env
POSTGRES_PASSWORD: "your-strong-password-here"
LANGFUSE_POSTGRES_PASSWORD: "different-strong-password"
```

### Production Deployment Checklist

- [ ] Change all default passwords marked with `# CHANGEME`
- [ ] Use Docker secrets instead of environment variables
- [ ] Restrict network access (remove port bindings for internal services)
- [ ] Enable TLS/SSL for database connections
- [ ] Configure CORS properly (not `allow_origins=["*"]`)
- [ ] Set up log aggregation
- [ ] Implement backup strategy
- [ ] Enable resource limits

### Using Docker Secrets (Production)

```yaml
services:
  crimepulse-backend:
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker-compose logs crimepulse-backend

# Common issues:
# 1. Database not ready - wait for health check
# 2. Missing environment variables - check .env
# 3. Port conflict - ensure 8000 is available
```

### Database Connection Issues

```bash
# Verify database is healthy
docker-compose ps crimepulse-postgres

# Check connection from backend
docker-compose exec crimepulse-backend curl -v crimepulse-postgres:5432

# Test credentials
docker-compose exec crimepulse-postgres psql -U crimepulse -d crimepulse -c "SELECT 1"
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Adjust resource limits in docker-compose.yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
```

## Build Optimization

### Layer Caching

The Dockerfile optimizes build cache:

1. Dependencies installed before copying code
2. .dockerignore excludes unnecessary files
3. Multi-stage builds separate concerns

### Faster Rebuilds

```bash
# Use BuildKit for parallel builds
DOCKER_BUILDKIT=1 docker-compose build

# Build specific service
docker-compose build crimepulse-backend
```

### Image Size Optimization

Current optimizations:

- Multi-stage build: ~200MB reduction
- Alpine-based PostgreSQL: Smaller footprint
- .dockerignore: Faster context transfers
- Production dependencies only: Minimal runtime

## Monitoring & Health Checks

### Health Check Configuration

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### View Health Status

```bash
# Check health status
docker-compose ps

# Watch logs for health checks
docker-compose logs -f crimepulse-backend | grep health
```

## Advanced Configuration

### Custom Networks

Services are isolated across three networks:

- **frontend**: External-facing services
- **backend**: Database access (internal only)
- **langfuse-network**: Observability stack

### Resource Limits

Configured per service:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Development Override

Create `docker-compose.override.yml` for local development:

```yaml
services:
  crimepulse-backend:
    build:
      target: development
    volumes:
      - ./backend:/app
      - /app/.venv
    environment:
      - LOG_LEVEL=debug
```

## CI/CD Integration

### Build for Production

```bash
# Build production image
docker build -t crimepulse-backend:latest ./backend

# Tag for registry
docker tag crimepulse-backend:latest registry.example.com/crimepulse-backend:v1.0.0

# Push to registry
docker push registry.example.com/crimepulse-backend:v1.0.0
```

### GitHub Actions Example

```yaml
- name: Build and Push Docker Image
  run: |
    docker build -t ${{ secrets.REGISTRY }}/crimepulse:${{ github.sha }} ./backend
    docker push ${{ secrets.REGISTRY }}/crimepulse:${{ github.sha }}
```

## Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Guide](https://hub.docker.com/_/postgres)
- [UV Package Manager](https://github.com/astral-sh/uv)
