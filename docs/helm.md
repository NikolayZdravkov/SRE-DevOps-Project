# Helm Deployment

Charts are located in the `helm/` directory:

```
helm/
├── database/        # PostgreSQL chart
└── student-api/     # REST API chart
```

## Prerequisites

- Minikube cluster running with correct node labels
- External Secrets Operator installed
- Vault installed and configured (see [kubernetes.md](kubernetes.md))
- Docker image loaded into Minikube:
  ```
  docker build -t student-api:1.0.1 .
  minikube image load student-api:1.0.1
  ```

## Install

```
helm install database ./helm/database
helm install student-api ./helm/student-api
```

## Verify

```
kubectl get pods -n student-api
kubectl get externalsecret -n student-api
```

## Access the API

```
kubectl port-forward svc/student-api 5000:5000 -n student-api
```

Then access at `http://localhost:5000/api/v1/`

## Upgrade

```
helm upgrade database ./helm/database
helm upgrade student-api ./helm/student-api
```

## Uninstall

```
helm uninstall student-api
helm uninstall database
```
