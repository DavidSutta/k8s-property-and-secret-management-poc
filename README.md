# K8s Property and Secret Management POC

A Python Flask application that serves data from YAML configuration files via REST API endpoints. This is a proof-of-concept for managing Kubernetes properties and secrets through HTTP endpoints.

## Features

- **Two REST GET endpoints:**
  - `/secrets` - Serves data from `secrets.yml`
  - `/configs` - Serves data from `configs.yml`
- **Health check endpoint:** `/health`
- **Error handling** for missing files and server errors
- **YAML file parsing** with proper error handling
- **JSON responses** with structured data

## Quick Start

### 1. Setup Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 4. Test the Endpoints

```bash
# Test all endpoints
python test_endpoints.py

# Or test manually with curl:
curl http://localhost:5000/health
curl http://localhost:5000/secrets
curl http://localhost:5000/configs
```

## API Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "K8s Property and Secret Management POC is running"
}
```

### GET /secrets
Serves data from `secrets.yml` file.

**Response:**
```json
{
  "status": "success",
  "data": {
    "database": { ... },
    "api_keys": { ... },
    "jwt": { ... },
    "redis": { ... },
    "environments": { ... }
  },
  "source": "secrets.yml"
}
```

### GET /configs
Serves data from `configs.yml` file.

**Response:**
```json
{
  "status": "success",
  "data": {
    "application": { ... },
    "server": { ... },
    "database": { ... },
    "redis": { ... },
    "logging": { ... },
    "features": { ... },
    "environments": { ... }
  },
  "source": "configs.yml"
}
```

## File Structure

```
├── app.py                           # Main Flask application
├── secrets.yml                      # Sample secrets configuration
├── configs.yml                      # Sample application configuration
├── requirements.txt                 # Python dependencies
├── test_endpoints.py                # Test script for endpoints
├── Dockerfile                       # Docker container configuration
├── k8s-namespace.yaml              # Kubernetes namespace
├── k8s-deployment.yaml             # Kubernetes deployment
├── k8s-service.yaml                # Kubernetes service
├── k8s-configmap-secrets.yaml      # ConfigMap for secrets data
├── k8s-configmap-configs.yaml      # ConfigMap for configs data
├── deploy-minikube.sh              # Minikube deployment script
├── cleanup-minikube.sh             # Minikube cleanup script
├── MINIKUBE_DEPLOYMENT.md          # Minikube deployment guide
├── README.md                       # This file
└── venv/                           # Virtual environment (created after setup)
```

## Configuration Files

### secrets.yml
Contains sensitive data like passwords, API keys, and encryption keys. This file should be managed as a Kubernetes Secret in production.

### configs.yml
Contains non-sensitive configuration data like server settings, database connection parameters, and feature flags.

## Kubernetes Deployment (Minikube)

The application can be deployed to minikube for local Kubernetes testing:

### Quick Deploy to Minikube

1. **Start minikube**:
   ```bash
   minikube start
   ```

2. **Deploy the application**:
   ```bash
   ./deploy-minikube.sh
   ```

3. **Access the application**:
   The script will output the application URL (e.g., `http://192.168.49.2:30080`)

4. **Clean up**:
   ```bash
   ./cleanup-minikube.sh
   ```

For detailed minikube deployment instructions, see [MINIKUBE_DEPLOYMENT.md](MINIKUBE_DEPLOYMENT.md).

### Kubernetes Resources

The deployment includes:
- **Dockerfile** - Containerizes the Flask application
- **k8s-deployment.yaml** - Kubernetes Deployment with 2 replicas
- **k8s-service.yaml** - NodePort service exposing port 30080
- **k8s-configmap-*.yaml** - ConfigMaps for configuration data
- **k8s-namespace.yaml** - Dedicated namespace for the application

## Production Deployment

For production deployment, consider:

1. **Security:** Never commit real secrets to version control
2. **Kubernetes Secrets:** Use Kubernetes Secret objects for sensitive data
3. **ConfigMaps:** Use Kubernetes ConfigMaps for non-sensitive configuration
4. **WSGI Server:** Use Gunicorn or similar WSGI server instead of Flask's development server
5. **Environment Variables:** Use environment variables for runtime configuration

## Dependencies

- **Flask 3.0.0** - Web framework
- **PyYAML 6.0.1** - YAML file parsing
- **Gunicorn 21.2.0** - WSGI server for production
- **python-dotenv 1.0.0** - Environment variable management
- **structlog 23.2.0** - Enhanced logging
- **requests 2.31.0** - HTTP client for testing
