# Test Environment Setup with Docker, Kubernetes (Kind), and NGINX Ingress

This guide outlines the steps to set up the required environment for the test task.
## Prerequisites

Ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-started/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)

## How To Run

### Step 1: Install Docker, Kubectl, Kind 

#### Important: Navigate to the project directory before building the Docker images, as the build process is configured from this directory. For example:

```bash
cd home-assignment/
```

#### Build the Docker images

```bash
docker build -f dockerfiles/Dockerfile-front -t frontend-image:1.0 .
docker build -f dockerfiles/Dockerfile-mongo -t mongo-image:1.0 .
docker build -f dockerfiles/Dockerfile-back -t backend-image:1.0 .
docker build -f dockerfiles/Dockerfile-import_data -t import-image:1.0 .
docker build -f dockerfiles/Dockerfile-posts -t posts-image:1.0 .
```

#### Alternatively, if you want to pull images from DockerHub, update the image names in the manifests. For example:

```yaml
image: grisard/home-assignment:backend-1.0
```

### Step 2: Create a Kubernetes Cluster with Kind

#### Don't forget to change the hostPath in kind-config.yaml, specifying the path to the init script.

```bash
kind create cluster --name=dropit-cluster --config ./cluster/kind-config.yaml
```

#### If you built images locally, don't forget to load the built Docker images into the Kind cluster:

```bash
kind load docker-image frontend-image:1.0 --name dropit-cluster
kind load docker-image mongo-image:1.0 --name dropit-cluster
kind load docker-image backend-image:1.0 --name dropit-cluster
kind load docker-image import-image:1.0 --name dropit-cluster
kind load docker-image posts-image:1.0 --name dropit-cluster
```

### Step 3: Install Local Path Provisioner for managing Persistent Volumes:

```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

### Step 4: Install the NGINX Ingress Controller for ingress management:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl label node dropit-cluster-control-plane ingress-ready=true
```

### Step 5: Apply Kubernetes Manifests

```bash
kubectl apply -f manifests/ingress.yaml 
kubectl apply -f manifests/mongodb-secret.yaml
kubectl apply -f manifests/mongodb-config.yaml
kubectl apply -f manifests/rbac.yaml
kubectl apply -f manifests/frontend-deployment.yaml
kubectl apply -f manifests/mongodb-statefulset.yaml
kubectl apply -f manifests/backend-deployment.yaml
kubectl apply -f manifests/mongo-import-job.yaml
kubectl apply -f manifests/posts-job.yaml
```

### Step 6: Delete the Kubernetes Cluster
#### Once you are finished, delete the Kind cluster:

```bash
kind delete cluster --name=dropit-cluster
```