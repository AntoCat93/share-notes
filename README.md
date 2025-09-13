# share-notes
Monorepo for shared notes system.

## Stack
Python 3, FastAPI, PostgreSQL, Redis, Docker.

## How to run (dev)
```bash
docker compose -f infra/docker-compose.dev.yml up -d --build

# check heathchecks
curl -f http://localhost:8001/healthz   # Auth API
curl -f http://localhost:8002/healthz   # Notes API

# check logs
docker compose -f infra/docker-compose.dev.yml logs -f auth
docker compose -f infra/docker-compose.dev.yml logs -f notes

# turn-off
docker compose -f infra/docker-compose.dev.yml down
