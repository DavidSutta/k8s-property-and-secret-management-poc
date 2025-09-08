# HashiCorp Vault Local Development Setup

This directory contains a Docker-based setup for running HashiCorp Vault locally for development and testing purposes.

## Features

- **HashiCorp Vault 1.15.2** running in development mode
- **File storage backend** for persistence
- **Web UI** accessible via browser
- **Docker Compose** for easy management
- **Nginx proxy** for additional routing options
- **Pre-configured** with development settings

## Quick Start

### 1. Start Vault

```bash
# Start Vault using Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t vault-local .
docker run -d --name vault-local -p 8200:8200 vault-local
```

### 2. Access Vault

- **Vault UI**: http://localhost:8200
- **API Endpoint**: http://localhost:8200
- **Nginx Proxy**: http://localhost:8080 (if using docker-compose)

### 3. Authentication

**Root Token**: `root-token`

**Unseal Key**: `root-token` (same as root token in dev mode)

## Configuration

### Vault Configuration (`vault.hcl`)

- **Storage**: File-based storage in `/vault/data`
- **Listener**: TCP on port 8200 (TLS disabled for development)
- **UI**: Enabled
- **Log Level**: INFO
- **Default Lease TTL**: 7 days
- **Max Lease TTL**: 30 days

### Environment Variables

- `VAULT_DEV_ROOT_TOKEN_ID`: Root token for authentication
- `VAULT_DEV_LISTEN_ADDRESS`: Listen address for Vault
- `VAULT_ADDR`: Vault API address

## Usage Examples

### 1. Using Vault CLI

```bash
# Set environment variables
export VAULT_ADDR="http://localhost:8200"
export VAULT_TOKEN="root-token"

# Check Vault status
vault status

# Enable KV secrets engine
vault secrets enable -path=secret kv-v2

# Write a secret
vault kv put secret/myapp/database username="dbuser" password="dbpass"

# Read a secret
vault kv get secret/myapp/database

# List secrets
vault kv list secret/
```

### 2. Using Vault API

```bash
# Check Vault status
curl http://localhost:8200/v1/sys/health

# Authenticate and get token
curl -X POST -d '{"password": "root-token"}' http://localhost:8200/v1/auth/userpass/login/root

# Write a secret (requires authentication)
curl -X POST \
  -H "X-Vault-Token: root-token" \
  -d '{"data": {"username": "dbuser", "password": "dbpass"}}' \
  http://localhost:8200/v1/secret/data/myapp/database

# Read a secret
curl -H "X-Vault-Token: root-token" \
  http://localhost:8200/v1/secret/data/myapp/database
```

### 3. Using Vault UI

1. Open http://localhost:8200 in your browser
2. Enter the root token: `root-token`
3. Navigate to "Secrets Engines" to enable KV storage
4. Create and manage secrets through the web interface

## Management Commands

### Start Services

```bash
# Start all services
docker-compose up -d

# Start with logs
docker-compose up

# Start only Vault
docker-compose up vault
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs

```bash
# View Vault logs
docker-compose logs vault

# Follow logs
docker-compose logs -f vault
```

### Access Container

```bash
# Access Vault container
docker exec -it vault-local sh

# Run Vault CLI commands
docker exec -it vault-local vault status
```

## File Structure

```
vault-local/
├── Dockerfile              # Vault container definition
├── docker-compose.yml      # Multi-service orchestration
├── vault.hcl              # Vault configuration
├── nginx.conf             # Nginx proxy configuration
└── README.md              # This file
```

## Development Notes

### Security Considerations

⚠️ **This setup is for development only!**

- TLS is disabled
- Root token is hardcoded
- File storage is not encrypted
- Do not use in production

### Data Persistence

- Vault data is stored in Docker volume `vault-data`
- Data persists between container restarts
- To reset data: `docker-compose down -v`

### Ports

- **8200**: Vault API and UI
- **8080**: Nginx proxy (optional)

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using port 8200
   lsof -i :8200

   # Kill the process or change port in docker-compose.yml
   ```

2. **Vault not starting**
   ```bash
   # Check logs
   docker-compose logs vault

   # Check container status
   docker-compose ps
   ```

3. **Permission issues**
   ```bash
   # Ensure Docker has proper permissions
   sudo chown -R $USER:$USER .
   ```

### Health Checks

```bash
# Check if Vault is running
curl http://localhost:8200/v1/sys/health

# Check Vault status via CLI
docker exec vault-local vault status
```

## Next Steps

Once Vault is running, you can:

1. **Enable secrets engines** (KV, AWS, Azure, etc.)
2. **Configure authentication methods** (userpass, LDAP, etc.)
3. **Set up policies** for access control
4. **Integrate with your applications** using Vault API
5. **Use Vault Agent** for automatic token renewal

## Resources

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [Vault API Reference](https://www.vaultproject.io/api)
- [Vault CLI Commands](https://www.vaultproject.io/docs/commands)
- [Docker Compose Reference](https://docs.docker.com/compose/)
