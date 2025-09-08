# Vault configuration for local development
# This configuration enables development mode with file storage

# Storage backend - using file storage for simplicity
storage "file" {
  path = "/vault/data"
}

# Listener configuration
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true  # Disable TLS for development
}

# Development mode settings
disable_mlock = true

# UI configuration
ui = true

# API address
api_addr = "http://0.0.0.0:8200"
cluster_addr = "http://0.0.0.0:8201"

# Log level
log_level = "INFO"

# Default lease TTL
default_lease_ttl = "168h"  # 7 days

# Maximum lease TTL
max_lease_ttl = "720h"  # 30 days
