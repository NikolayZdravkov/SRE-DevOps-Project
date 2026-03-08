# Docker

## Build the image

```
make docker-build
```

## Run the container (standalone)

```
make docker-run
```

Environment variables are injected via `.env`. Never commit `.env`.

## One-Click Local Development Setup

```
make start-api
```

This will:
1. Build the Docker image
2. Start the PostgreSQL container
3. Run database migrations
4. Start the API container

## Running targets individually

```
make start-db       # 1. Start the database
make migrate        # 2. Run migrations
make docker-build   # 3. Build the image
make start-api      # 4. Start the API
```
