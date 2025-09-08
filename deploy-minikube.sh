#!/bin/bash

# K8s Property and Secret Management POC - Minikube Deployment Script
# This script deploys the Flask application to minikube

set -e

echo "🚀 Starting K8s Property and Secret Management POC deployment to minikube..."

# Check if minikube is running
if ! minikube status > /dev/null 2>&1; then
    echo "❌ Minikube is not running. Please start minikube first:"
    echo "   minikube start"
    exit 1
fi

echo "✅ Minikube is running"

# Set minikube docker environment
echo "🔧 Setting up minikube docker environment..."
eval $(minikube docker-env)

# Build the Docker image
echo "🏗️  Building Docker image..."
docker build -t k8s-property-secret-poc:latest .

echo "✅ Docker image built successfully"

# Cleaning k8s-property-secret-poc namespace
echo "🧹 Cleaning k8s-property-secret-poc namespace..."
kubectl delete namespace k8s-property-secret-poc --ignore-not-found=true

# Apply Kubernetes resources
echo "📦 Applying Kubernetes resources..."

# Create namespace
kubectl apply -f k8s/k8s-namespace.yaml

# Apply ConfigMaps
kubectl apply -f k8s/k8s-configmap-secrets.yaml
kubectl apply -f k8s/k8s-configmap-configs.yaml

# Apply deployment
kubectl apply -f k8s/k8s-deployment.yaml

# Apply service
kubectl apply -f k8s/k8s-service.yaml

echo "✅ Kubernetes resources applied successfully"

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/k8s-property-secret-poc -n k8s-property-secret-poc

echo "✅ Deployment is ready!"

# Get service information
echo "🌐 Service information:"
kubectl get services -n k8s-property-secret-poc

# Get the minikube IP and NodePort
MINIKUBE_IP=$(minikube ip)
NODE_PORT=$(kubectl get service k8s-property-secret-poc-service -n k8s-property-secret-poc -o jsonpath='{.spec.ports[0].nodePort}')

echo ""
echo "🎉 Deployment completed successfully!"
echo "📱 Application is accessible at:"
echo "   http://${MINIKUBE_IP}:${NODE_PORT}"
echo ""
echo "🔗 Available endpoints:"
echo "   http://${MINIKUBE_IP}:${NODE_PORT}/health"
echo "   http://${MINIKUBE_IP}:${NODE_PORT}/secrets"
echo "   http://${MINIKUBE_IP}:${NODE_PORT}/configs"
echo "   http://${MINIKUBE_IP}:${NODE_PORT}/env-status"
echo ""
echo "📊 To check pod status:"
echo "   kubectl get pods -n k8s-property-secret-poc"
echo ""
echo "📋 To view logs:"
echo "   kubectl logs -f deployment/k8s-property-secret-poc -n k8s-property-secret-poc"
echo ""
echo "🗑️  To clean up:"
echo "   kubectl delete namespace k8s-property-secret-poc"
