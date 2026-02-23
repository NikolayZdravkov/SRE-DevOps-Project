# Student CRUD REST API

A Student CRUD REST API built with Python and Flask.

## Features

- Create, read, update, and delete student records
- API versioning (api/v1)
- Health check endpoint
- Database migrations with Flask-Migrate
- Structured logging
- Unit tests

## Tech Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-Migrate

## Prerequisites

- Python 3.x
- PostgreSQL
- Docker
- Docker Compose
- Make
- Vagrant
- VirtualBox

## Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/NikolayZdravkov/SRE-DevOps-Project.git
   cd SRE-DevOps-Project
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   make install
   ```

4. Set up PostgreSQL:
   ```
   sudo -u postgres psql
   CREATE USER student_user WITH PASSWORD 'your_password';
   CREATE DATABASE student_db OWNER student_user;
   \q
   ```

5. Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://student_user:your_password@localhost:5432/student_db
   FLASK_APP=run.py
   DEBUG=True
   ```

6. Run database migrations:
   ```
   flask db upgrade
   ```

7. Start the server:
   ```
   make run
   ```

## API Endpoints

| Method | Endpoint                  | Description        |
|--------|---------------------------|--------------------|
| GET    | /api/v1/healthcheck       | Health check       |
| POST   | /api/v1/students          | Create a student   |
| GET    | /api/v1/students          | Get all students   |
| GET    | /api/v1/students/\<id\>   | Get student by ID  |
| PUT    | /api/v1/students/\<id\>   | Update a student   |
| DELETE | /api/v1/students/\<id\>   | Delete a student   |

## Docker

### Build the image
```
make docker-build
```

### Run the container (standalone)
```
make docker-run
```

Environment variables are injected at runtime via the `.env` file. Make sure your `.env` file exists before running the container. Never commit `.env` to the repository.

## One-Click Local Development Setup

The easiest way to run the full stack locally is with a single command:

```
make start-api
```

This will automatically:
1. Build the Docker image
2. Start the PostgreSQL database container
3. Run database migrations
4. Start the API container

### Running targets individually (in order)

If you prefer to run each step manually:

```
make start-db       # 1. Start the database container
make migrate        # 2. Run database migrations
make docker-build   # 3. Build the API Docker image
make start-api      # 4. Start the API container
```

## Production Deployment (Vagrant)

The production setup runs 2 API containers, 1 DB container, and 1 Nginx container for load balancing.

### Architecture
```
Internet
    ↓
Nginx (port 8080)
    ↓ load balances
┌──────┬──────┐
API 1  API 2
    ↓
   DB (PostgreSQL)
```

### Setup

1. Install Vagrant and VirtualBox
2. Spin up the VM:
   ```
   vagrant up
   ```
3. SSH into the VM:
   ```
   vagrant ssh
   ```
4. Navigate to the project and deploy:
   ```
   cd /vagrant
   make deploy
   ```
5. Run database migrations:
   ```
   docker exec -e FLASK_APP=run.py api1 flask db upgrade
   ```
6. The API is now accessible at `http://localhost:8080/api/v1/`

### Stopping the VM
```
vagrant halt
```

### Destroying the VM
```
vagrant destroy
```

## Makefile Commands

| Command             | Description                            |
|---------------------|----------------------------------------|
| `make install`      | Install dependencies                   |
| `make run`          | Start the server locally               |
| `make test`         | Run unit tests                         |
| `make lint`         | Run code linting                       |
| `make docker-build` | Build the Docker image                 |
| `make docker-run`   | Run the API container (standalone)     |
| `make start-db`     | Start the PostgreSQL container         |
| `make migrate`      | Run database migrations                |
| `make start-api`    | Start the full stack (DB + API)        |
| `make deploy`       | Build image and deploy full stack      |

## Running Tests

```
make test
```

## CI Pipeline

The project uses GitHub Actions for CI, running on a self-hosted runner.

### Pipeline stages
1. Install dependencies
2. Run tests
3. Lint
4. Docker login to GHCR
5. Docker build and push

### Triggers
- Automatically on push to `app/`, `tests/`, `requirements.txt`, `Dockerfile`, or `Makefile`
- Manually from the GitHub Actions tab using **Run workflow**

### Self-hosted runner setup
1. Go to your GitHub repository → **Settings** → **Actions** → **Runners**
2. Click **New self-hosted runner** and follow the instructions
3. Start the runner with `./run.sh` from the runner directory

## Postman Collection

A Postman collection is included in the repository (`student-api.postman_collection.json`). Import it into Postman to test all API endpoints.
