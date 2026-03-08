# Vagrant Deployment

Runs 2 API containers, 1 DB container, and 1 Nginx load balancer.

## Setup

1. Install Vagrant and VirtualBox
2. Spin up the VM:
   ```
   vagrant up
   ```
3. SSH into the VM:
   ```
   vagrant ssh
   ```
4. Deploy:
   ```
   cd /vagrant
   make deploy
   ```
5. Run migrations:
   ```
   docker exec -e FLASK_APP=run.py api1 flask db upgrade
   ```

API is accessible at `http://localhost:8080/api/v1/`

## Stop / Destroy

```
vagrant halt
vagrant destroy
```
