# HashiCorp Vault Dockerfile for local development
FROM hashicorp/vault:latest

# Set environment variables for Vault
ENV VAULT_DEV_ROOT_TOKEN_ID="root-token"
ENV VAULT_DEV_LISTEN_ADDRESS="0.0.0.0:8200"
ENV VAULT_ADDR="http://0.0.0.0:8200"

# Create vault data directory
RUN mkdir -p /vault/data

# Copy Vault configuration
COPY vault.hcl /vault/config/vault.hcl

# Expose Vault port
EXPOSE 8200

# Set the working directory
WORKDIR /vault

# Create a startup script for development mode
RUN echo '#!/bin/sh' > /vault/start-vault.sh && \
    echo 'echo "Starting HashiCorp Vault in development mode..."' >> /vault/start-vault.sh && \
    echo 'echo "Vault UI will be available at: http://localhost:8200"' >> /vault/start-vault.sh && \
    echo 'echo "Root Token: $VAULT_DEV_ROOT_TOKEN_ID"' >> /vault/start-vault.sh && \
    echo 'echo "Unseal Key: $VAULT_DEV_ROOT_TOKEN_ID"' >> /vault/start-vault.sh && \
    echo 'echo "==========================================="' >> /vault/start-vault.sh && \
    echo 'vault server -dev -dev-root-token-id=$VAULT_DEV_ROOT_TOKEN_ID -dev-listen-address=$VAULT_DEV_LISTEN_ADDRESS' >> /vault/start-vault.sh && \
    chmod +x /vault/start-vault.sh

# Default command
CMD ["/vault/start-vault.sh"]
