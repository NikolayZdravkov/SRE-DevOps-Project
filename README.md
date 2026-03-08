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

- Python / Flask
- PostgreSQL / SQLAlchemy / Flask-Migrate
- Docker / Docker Compose
- Nginx
- GitHub Actions CI/CD
- Kubernetes / Helm
- Hashicorp Vault + External Secrets Operator

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

4. Set up PostgreSQL and create a `.env` file:
   ```
   DATABASE_URL=postgresql://student_user:your_password@localhost:5432/student_db
   FLASK_APP=run.py
   DEBUG=True
   ```

5. Run migrations and start the server:
   ```
   flask db upgrade
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

## Makefile Commands

| Command             | Description                       |
|---------------------|-----------------------------------|
| `make install`      | Install dependencies              |
| `make run`          | Start the server locally          |
| `make test`         | Run unit tests                    |
| `make lint`         | Run code linting                  |
| `make docker-build` | Build the Docker image            |
| `make start-api`    | Start the full stack (DB + API)   |
| `make deploy`       | Build image and deploy full stack |

## CI Pipeline

GitHub Actions runs on a self-hosted runner on push to `app/`, `tests/`, `requirements.txt`, `Dockerfile`, or `Makefile`.

Stages: install → test → lint → docker build & push to GHCR

## Deployment Guides

- [Docker](docs/docker.md)
- [Vagrant](docs/vagrant.md)
- [Kubernetes](docs/kubernetes.md)
- [Helm](docs/helm.md)

## Postman Collection

Import `student-api.postman_collection.json` into Postman to test all endpoints.
