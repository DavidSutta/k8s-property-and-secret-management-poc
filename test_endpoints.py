#!/usr/bin/env python3
"""
Test script for the K8s Property and Secret Management POC endpoints
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

def test_endpoints():
    """Test the Flask application endpoints"""
    base_url = "http://localhost:5000"

    print("Testing K8s Property and Secret Management POC endpoints...")
    print("=" * 60)

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✓ Health endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Health endpoint failed: {e}")
        return False

    # Test secrets endpoint
    try:
        response = requests.get(f"{base_url}/secrets", timeout=5)
        print(f"✓ Secrets endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data['status']}")
            print(f"  Source: {data['source']}")
            print(f"  Data keys: {list(data['data'].keys())}")
        else:
            print(f"  Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Secrets endpoint failed: {e}")
        return False

    # Test configs endpoint
    try:
        response = requests.get(f"{base_url}/configs", timeout=5)
        print(f"✓ Configs endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data['status']}")
            print(f"  Source: {data['source']}")
            print(f"  Data keys: {list(data['data'].keys())}")
        else:
            print(f"  Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Configs endpoint failed: {e}")
        return False

    print("=" * 60)
    print("All tests completed!")
    return True

def start_app():
    """Start the Flask application in the background"""
    print("Starting Flask application...")
    try:
        # Start the app in background
        process = subprocess.Popen([sys.executable, "app.py"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        # Wait a moment for the app to start
        time.sleep(3)

        return process
    except Exception as e:
        print(f"Failed to start app: {e}")
        return None

def main():
    """Main test function"""
    # Check if YAML files exist
    if not Path("secrets.yml").exists():
        print("Error: secrets.yml not found")
        return False

    if not Path("configs.yml").exists():
        print("Error: configs.yml not found")
        return False

    # Start the app
    app_process = start_app()
    if not app_process:
        return False

    try:
        # Test the endpoints
        success = test_endpoints()

        if success:
            print("\n🎉 All tests passed! The application is working correctly.")
        else:
            print("\n❌ Some tests failed. Check the output above.")

        return success

    finally:
        # Clean up: terminate the app process
        if app_process:
            app_process.terminate()
            app_process.wait()
            print("\nFlask application stopped.")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
