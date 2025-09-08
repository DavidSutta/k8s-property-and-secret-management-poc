# K8s Property and Secret Management POC

The project's scope is to showcase Configuration and Secret management in Kubernetes.
The main service is a Python Flask application that serves data via REST API endpoints.

## Endpoints

- **Two REST GET endpoints:**
  - `/secrets` - Serves data that is supposed to be "secret"
  - `/configs` - Serves data that is supposed to be regular "config parameter"
- **Health check endpoint:** `/health`

## Quick Start

### Requirements

- Docker
- Minikube

### 1. Setup Minikube on your machine

Minikube will be used to set up a mini Kubernetes cluster locally

`brew install minikube`

### 2. Start the application

```bash
./deploy-minikube.sh
```

This will deploy the app to your minikube "cluster" to the `k8s-property-secret-poc` namespace.

### 3. Accessing the application locally

```bash
minikube service k8s-property-secret-poc-service -n k8s-property-secret-poc
```
After this, the app will get published to your localhost, where you can access the endpoints via a browser, or using `curl`.
