#!/usr/bin/env python3
"""
Kubernetes Property and Secret Management POC
A Flask application that serves data from secrets.yml and configs.yml files
"""

import yaml
import os
from flask import Flask, jsonify, abort
from pathlib import Path

app = Flask(__name__)

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

@app.route('/secrets', methods=['GET'])
def get_secrets():
    """GET endpoint to serve data from secrets.yml"""
    secrets_data = load_yaml_file('secrets.yml')

    if secrets_data is None:
        abort(404, description="secrets.yml file not found or could not be loaded")

    return jsonify({
        "status": "success",
        "data": secrets_data,
        "source": "secrets.yml"
    })

@app.route('/configs', methods=['GET'])
def get_configs():
    """GET endpoint to serve data from configs.yml"""
    configs_data = load_yaml_file('configs.yml')

    if configs_data is None:
        abort(404, description="configs.yml file not found or could not be loaded")

    return jsonify({
        "status": "success",
        "data": configs_data,
        "source": "configs.yml"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "K8s Property and Secret Management POC is running"
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
    # Check if YAML files exist
    if not Path('secrets.yml').exists():
        print("Warning: secrets.yml not found")
    if not Path('configs.yml').exists():
        print("Warning: configs.yml not found")

    print("Starting K8s Property and Secret Management POC...")
    print("Available endpoints:")
    print("  GET /secrets  - Serve data from secrets.yml")
    print("  GET /configs  - Serve data from configs.yml")
    print("  GET /health   - Health check")

    app.run(host='0.0.0.0', port=5000, debug=True)
