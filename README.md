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
- Minikube
- kubectl

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

```mermaid
flowchart TD
    Client([Client]) --> Nginx

    subgraph Vagrant VM
        Nginx[Nginx :8080] --> API1[API Container 1 :5000]
        Nginx --> API2[API Container 2 :5000]
        API1 --> DB[(PostgreSQL :5432)]
        API2 --> DB
    end
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

## Kubernetes Cluster Setup

A 3-node Minikube cluster is used as the production Kubernetes environment.

### Node roles

| Node          | Label                      | Purpose               |
|---------------|----------------------------|-----------------------|
| minikube      | type=application           | Runs the API          |
| minikube-m02  | type=database              | Runs the database     |
| minikube-m03  | type=dependent_services    | Runs observability stack and other services |

### Start the cluster

```
minikube start --nodes=3 --driver=docker
```

### Apply node labels

```
kubectl label node minikube type=application
kubectl label node minikube-m02 type=database
kubectl label node minikube-m03 type=dependent_services
```

### Verify nodes and labels

```
kubectl get nodes --show-labels
```

### Stop the cluster

```
minikube stop
```

## Kubernetes Deployment

The application and database are deployed in the `student-api` namespace using Kubernetes manifests located in the `k8s/` directory.

### Architecture

```mermaid
flowchart TD
    Client([Client]) --> NodePort

    subgraph Minikube Cluster
        NodePort[NodePort Service :30000] --> API1[API Pod 1]
        NodePort --> API2[API Pod 2]
        API1 --> DB[(PostgreSQL Pod)]
        API2 --> DB
        Vault[Hashicorp Vault] --> ESO[External Secrets Operator]
        ESO --> Secret[K8s Secret]
        Secret --> API1
        Secret --> API2
        Secret --> DB
    end
```

### Prerequisites

- Minikube cluster running with 3 nodes and correct labels
- External Secrets Operator installed
- Hashicorp Vault installed and configured

### Install External Secrets Operator

```
helm repo add external-secrets https://charts.external-secrets.io
helm repo update
helm install external-secrets external-secrets/external-secrets --namespace external-secrets --create-namespace
```

### Install Hashicorp Vault

```
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault --namespace vault --create-namespace --set server.dev.enabled=true
```

### Configure Vault

```
kubectl exec -it vault-0 -n vault -- /bin/sh
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'
vault auth enable kubernetes
vault write auth/kubernetes/config kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443"
vault kv put secret/student-api/database username=student_user password=student_password
vault policy write student-api-policy /tmp/policy.hcl
vault write auth/kubernetes/role/student-api-role bound_service_account_names=student-api-sa bound_service_account_namespaces=student-api policies=student-api-policy ttl=24h
exit
```

### Load the Docker image into Minikube

```
docker build -t student-api:1.0.1 .
minikube image load student-api:1.0.1
```

### Apply manifests

```
kubectl apply -f k8s/database.yml
kubectl apply -f k8s/application.yml
```

### Verify deployment

```
kubectl get pods -n student-api
kubectl get externalsecret -n student-api
```

### Access the API

```
kubectl port-forward svc/student-api 5000:5000 -n student-api
```

Then access the API at `http://localhost:5000/api/v1/`

## Postman Collection

A Postman collection is included in the repository (`student-api.postman_collection.json`). Import it into Postman to test all API endpoints.
