# Kubernetes Deployment

## Cluster Setup

Start a 3-node Minikube cluster:

```
minikube start --nodes=3 --driver=docker
```

Apply node labels:

```
kubectl label node minikube type=application
kubectl label node minikube-m02 type=database
kubectl label node minikube-m03 type=dependent_services
```

## Prerequisites

- External Secrets Operator installed
- Hashicorp Vault installed and configured

### Install External Secrets Operator

```
helm repo add external-secrets https://charts.external-secrets.io
helm repo update
helm install external-secrets external-secrets/external-secrets --namespace external-secrets --create-namespace
```

### Install Vault

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

## Deploy

Load the image into Minikube:

```
docker build -t student-api:1.0.1 .
minikube image load student-api:1.0.1
```

Apply manifests:

```
kubectl apply -f k8s/database.yml
kubectl apply -f k8s/application.yml
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
