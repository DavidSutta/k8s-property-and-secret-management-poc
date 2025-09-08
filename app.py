#!/usr/bin/env python3
"""
Kubernetes Property and Secret Management POC
A Flask application that serves data from secrets.yml and configs.yml files
YAML files are pre-processed at startup and stored as environment variables
"""

import yaml
import os
import json
from flask import Flask, jsonify, abort
from pathlib import Path

app = Flask(__name__)

# Global variables to store pre-processed YAML data
SECRETS_DATA = None
CONFIGS_DATA = None

def load_yaml_file(filename):
    """Load and parse a YAML file, return the data or None if file doesn't exist"""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def is_kubernetes_environment():
    """Check if running in Kubernetes environment"""
    # Check for Kubernetes-specific environment variables or files
    return (
        os.environ.get('KUBERNETES_SERVICE_HOST') is not None or
        os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount') or
        os.environ.get('CONFIGS_DATA') is not None or
        os.environ.get('SECRETS_DATA') is not None
    )

def preprocess_yaml_files():
    """Pre-process YAML files at application startup and store as environment variables"""
    global SECRETS_DATA, CONFIGS_DATA

    # Only load YAML files in local development, not in Kubernetes
    if is_kubernetes_environment():
        print("🔧 Running in Kubernetes environment - skipping YAML file loading")
        print("📦 Using environment variables from ConfigMaps/Secrets")
        return

    print("🏠 Running in local development mode - loading YAML files...")

    # Load secrets.yml
    secrets_data = load_yaml_file('secrets.yml')
    if secrets_data is not None:
        SECRETS_DATA = secrets_data
        # Store as environment variable (JSON string)
        os.environ['SECRETS_DATA'] = json.dumps(secrets_data)
        print("✓ secrets.yml loaded and stored as environment variable")
    else:
        print("⚠ Warning: secrets.yml not found or could not be loaded")

    # Load configs.yml
    configs_data = load_yaml_file('configs.yml')
    if configs_data is not None:
        CONFIGS_DATA = configs_data
        # Store as environment variable (JSON string)
        os.environ['CONFIGS_DATA'] = json.dumps(configs_data)
        print("✓ configs.yml loaded and stored as environment variable")
    else:
        print("⚠ Warning: configs.yml not found or could not be loaded")

    print("YAML file pre-processing completed!")

def get_secrets_data():
    """Get secrets data from environment variable or global variable"""
    global SECRETS_DATA

    if SECRETS_DATA is not None:
        return SECRETS_DATA

    # Fallback to environment variable
    secrets_json = os.environ.get('SECRETS_DATA')
    if secrets_json:
        try:
            return json.loads(secrets_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing SECRETS_DATA from environment: {e}")

    return None

def get_configs_data():
    """Get configs data from environment variable or global variable"""
    global CONFIGS_DATA

    if CONFIGS_DATA is not None:
        return CONFIGS_DATA

    # Fallback to environment variable
    configs_json = os.environ.get('CONFIGS_DATA')
    if configs_json:
        try:
            return json.loads(configs_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing CONFIGS_DATA from environment: {e}")

    return None

@app.route('/secrets', methods=['GET'])
def get_secrets():
    """GET endpoint to serve data from secrets (YAML file or ConfigMap)"""
    secrets_data = get_secrets_data()

    if secrets_data is None:
        abort(404, description="secrets data not available (file not found or environment variable not set)")

    # Determine data source for response
    if is_kubernetes_environment():
        source = "Kubernetes ConfigMap (environment variable)"
    else:
        source = "secrets.yml (local development)"

    return jsonify({
        "status": "success",
        "data": secrets_data,
        "source": source
    })

@app.route('/configs', methods=['GET'])
def get_configs():
    """GET endpoint to serve data from configs (YAML file or ConfigMap)"""
    configs_data = get_configs_data()

    if configs_data is None:
        abort(404, description="configs data not available (file not found or environment variable not set)")

    # Determine data source for response
    if is_kubernetes_environment():
        source = "Kubernetes ConfigMap (environment variable)"
    else:
        source = "configs.yml (local development)"

    return jsonify({
        "status": "success",
        "data": configs_data,
        "source": source
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "K8s Property and Secret Management POC is running"
    })

@app.route('/env-status', methods=['GET'])
def env_status():
    """Endpoint to show environment variable status"""
    secrets_available = os.environ.get('SECRETS_DATA') is not None
    configs_available = os.environ.get('CONFIGS_DATA') is not None

    return jsonify({
        "status": "success",
        "environment_variables": {
            "SECRETS_DATA": "available" if secrets_available else "not available",
            "CONFIGS_DATA": "available" if configs_available else "not available"
        },
        "preprocessing_status": {
            "secrets_loaded": secrets_available,
            "configs_loaded": configs_available
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler"""
    return jsonify({
        "status": "error",
        "message": error.description
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error handler"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("Starting K8s Property and Secret Management POC...")
    print("=" * 50)

    # Detect environment and pre-process accordingly
    if is_kubernetes_environment():
        print("🔧 Kubernetes environment detected")
        print("📦 Configuration will be loaded from environment variables")
    else:
        print("🏠 Local development environment detected")
        print("📁 Configuration will be loaded from YAML files")

    # Pre-process YAML files at startup (only in local dev)
    preprocess_yaml_files()

    print("=" * 50)
    print("Available endpoints:")
    print("  GET /secrets    - Serve data from secrets")
    print("  GET /configs    - Serve data from configs")
    print("  GET /health     - Health check")
    print("  GET /env-status - Show environment variable status")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5000, debug=True)
