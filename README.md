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


## Showcasing the actual config/secret management

`app.py` can work in two modes:
- when started locally: it will parse it's initial secret and config values from the corresponding `.yml` files. This is good for local development
- when running on kubernetes: it will take the config values from the created ConfigMaps. See: `k8s/k8s-configmap-configs.yml`. And see the corresponding deployment `k8s-deployment.yml` file how it is using that as environment variable.

**To validate that configs are being loaded from k8s ConfigMaps, see the logs of the app pod**
```bash
kubectl -n k8s-property-secret-poc logs $(kubectl -n k8s-property-secret-poc get pods | grep k8s-property-secret-poc | head -n 1 | cut -d ' ' -f 1)
```

You will see the following:

```
❯ kubectl -n k8s-property-secret-poc logs $(kubectl -n k8s-property-secret-poc get pods | grep k8s-property-secret-poc | head -n 1 | cut -d ' ' -f 1)
Starting K8s Property and Secret Management POC...
==================================================
🔧 Kubernetes environment detected
📦 Configuration will be loaded from environment variables
🔧 Running in Kubernetes environment - skipping YAML file loading
📦 Using environment variables from ConfigMaps/Secrets
==================================================
Available endpoints:
  GET /secrets    - Serve data from secrets
  GET /configs    - Serve data from configs
  GET /health     - Health check
  GET /env-status - Show environment variable status
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.244.0.3:5000
Press CTRL+C to quit
```

## Adding Vault

Idea is to have a locally running vault, then reference that from your `minikube` deployment via `http://host.minikube.internal:8200`.
To run vault, use

```bash
vault-local/vault-helper.sh start
```

# TODO: Expand readme with VSO usage

https://developer.hashicorp.com/vault/docs/platform/k8s/vso/api-reference#vaultauthconfigapprole

https://developer.hashicorp.com/vault/tutorials/kubernetes-introduction/vault-secrets-operator

