#!/bin/bash

# HashiCorp Vault Helper Script
# This script provides common Vault operations for local development

set -e

# Configuration
VAULT_ADDR="http://localhost:8200"
VAULT_TOKEN="root-token"
CONTAINER_NAME="vault-local"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Vault is running
check_vault_status() {
    if curl -s "$VAULT_ADDR/v1/sys/health" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Wait for Vault to be ready
wait_for_vault() {
    print_status "Waiting for Vault to be ready..."
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if check_vault_status; then
            print_success "Vault is ready!"
            return 0
        fi

        echo -n "."
        sleep 2
        ((attempt++))
    done

    print_error "Vault failed to start within 60 seconds"
    return 1
}

# Start Vault
start_vault() {
    print_status "Starting Vault..."
    docker-compose up -d

    if wait_for_vault; then
        print_success "Vault started successfully!"
        echo "Vault UI: $VAULT_ADDR"
        echo "Root Token: $VAULT_TOKEN"
    else
        print_error "Failed to start Vault"
        exit 1
    fi
}

# Stop Vault
stop_vault() {
    print_status "Stopping Vault..."
    docker-compose down
    print_success "Vault stopped"
}

# Show Vault status
show_status() {
    if check_vault_status; then
        print_success "Vault is running"
        echo "URL: $VAULT_ADDR"
        echo "Status:"
        curl -s "$VAULT_ADDR/v1/sys/health" | jq '.' 2>/dev/null || curl -s "$VAULT_ADDR/v1/sys/health"
    else
        print_error "Vault is not running"
    fi
}

# Show logs
show_logs() {
    print_status "Showing Vault logs..."
    docker-compose logs -f vault
}

# Enable KV secrets engine
enable_kv() {
    print_status "Enabling KV secrets engine..."
    docker exec $CONTAINER_NAME vault secrets enable -path=secret kv-v2
    print_success "KV secrets engine enabled at /secret"
}

# Create sample secrets
create_sample_secrets() {
    print_status "Creating sample secrets..."

    # Enable KV if not already enabled
    enable_kv > /dev/null 2>&1 || true

    # Create sample secrets
    docker exec $CONTAINER_NAME vault kv put secret/myapp/database \
        username="dbuser" \
        password="dbpass123" \
        host="localhost" \
        port="5432"

    docker exec $CONTAINER_NAME vault kv put secret/myapp/api \
        api_key="sk_live_1234567890abcdef" \
        secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    docker exec $CONTAINER_NAME vault kv put secret/myapp/jwt \
        secret="your-super-secret-jwt-key" \
        algorithm="HS256" \
        expiration="24h"

    print_success "Sample secrets created:"
    echo "  - secret/myapp/database"
    echo "  - secret/myapp/api"
    echo "  - secret/myapp/jwt"
}

# List secrets
list_secrets() {
    print_status "Listing secrets..."
    docker exec $CONTAINER_NAME vault kv list secret/ 2>/dev/null || echo "No secrets found or KV engine not enabled"
}

# Get a secret
get_secret() {
    local path="$1"
    if [ -z "$path" ]; then
        print_error "Please provide a secret path (e.g., secret/myapp/database)"
        exit 1
    fi

    print_status "Getting secret: $path"
    docker exec $CONTAINER_NAME vault kv get "$path"
}

# Reset Vault (remove all data)
reset_vault() {
    print_warning "This will remove all Vault data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Resetting Vault..."
        docker-compose down -v
        print_success "Vault data reset"
    else
        print_status "Reset cancelled"
    fi
}

# Show help
show_help() {
    echo "HashiCorp Vault Helper Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start           Start Vault"
    echo "  stop            Stop Vault"
    echo "  restart         Restart Vault"
    echo "  status          Show Vault status"
    echo "  logs            Show Vault logs"
    echo "  enable-kv       Enable KV secrets engine"
    echo "  create-samples  Create sample secrets"
    echo "  list            List all secrets"
    echo "  get <path>      Get a specific secret"
    echo "  reset           Reset Vault (remove all data)"
    echo "  help            Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 get secret/myapp/database"
    echo "  $0 create-samples"
}

# Main script logic
case "${1:-help}" in
    start)
        start_vault
        ;;
    stop)
        stop_vault
        ;;
    restart)
        stop_vault
        start_vault
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    enable-kv)
        enable_kv
        ;;
    create-samples)
        create_sample_secrets
        ;;
    list)
        list_secrets
        ;;
    get)
        get_secret "$2"
        ;;
    reset)
        reset_vault
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
