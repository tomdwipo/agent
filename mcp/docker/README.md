# Docker MCP Server

A Model Context Protocol (MCP) server for Docker container management. This server provides AI assistants with comprehensive access to Docker operations including containers, images, networks, volumes, and Docker Compose services.

## Features

- 🐳 **Container Management** - Create, start, stop, remove, and monitor Docker containers
- 🖼️ **Image Operations** - Pull, build, tag, and manage Docker images
- 🔗 **Network Management** - Create and manage Docker networks
- 💾 **Volume Operations** - Handle Docker volumes and data persistence
- 🐙 **Docker Compose Support** - Full Docker Compose workflow automation
- 🔒 **Security Controls** - Configurable volume mount restrictions and privileged mode controls
- ⚡ **Async Operations** - Non-blocking Docker operations for better performance

## Prerequisites

- **Python** >= 3.10
- **Docker** installed and running
- **Docker Compose** (for compose operations)
- **uv** package manager (recommended)

## Installation

1. **Navigate to the Docker MCP directory**
   ```bash
   cd mcp/docker
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Verify Docker is running**
   ```bash
   docker ps
   ```

## Configuration

1. **Create environment file** (optional)
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   # Docker daemon configuration
   DOCKER_HOST=unix:///var/run/docker.sock
   DOCKER_TLS_VERIFY=false
   DOCKER_CERT_PATH=/path/to/certs
   
   # Default settings
   DOCKER_DEFAULT_NETWORK=bridge
   DOCKER_DEFAULT_REGISTRY=docker.io
   COMPOSE_PROJECT_NAME=mcp-docker
   
   # Security settings
   DOCKER_ALLOW_PRIVILEGED=false
   DOCKER_ALLOWED_VOLUMES=/tmp,/var/log,/home/user/data
   
   # Performance
   DOCKER_TIMEOUT=30
   ```

## Usage

### As MCP Server (Recommended)

Run the server in stdio mode for MCP client integration:

```bash
uv run main.py
```

### With Custom Configuration

```bash
uv run main.py --docker-host unix:///var/run/docker.sock --timeout 60
```

## Available Tools

### Container Management

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-containers` | List Docker containers | Optional: `all`, `filters` |
| `create-container` | Create new container | `image`, optional: `name`, `ports`, `environment`, `volumes` |
| `start-container` | Start container | `container_id` |
| `stop-container` | Stop container | `container_id`, optional: `timeout` |
| `remove-container` | Remove container | `container_id`, optional: `force` |
| `container-logs` | Get container logs | `container_id`, optional: `tail`, `follow` |

### Image Management

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-images` | List Docker images | Optional: `all` |
| `pull-image` | Pull image from registry | `image`, optional: `tag` |
| `build-image` | Build image from Dockerfile | `path`, `tag`, optional: `dockerfile` |
| `remove-image` | Remove image | `image`, optional: `force` |

### Network & Volume Management

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-networks` | List Docker networks | None |
| `create-network` | Create network | `name`, optional: `driver` |
| `remove-network` | Remove network | `network_id` |
| `list-volumes` | List Docker volumes | None |
| `create-volume` | Create volume | `name` |
| `remove-volume` | Remove volume | `volume_name` |

### Docker Compose

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `compose-up` | Start Compose services | `file_path`, optional: `detach`, `build` |
| `compose-down` | Stop Compose services | `file_path`, optional: `remove_volumes` |
| `compose-ps` | List Compose services | `file_path` |

## MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "docker-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/agent/mcp/docker && uv run main.py"
      ],
      "alwaysAllow": [
        "list-containers",
        "list-images",
        "list-networks",
        "list-volumes"
      ]
    }
  }
}
```

## Security Considerations

### Volume Mount Restrictions
Configure allowed volume paths in `.env`:
```env
DOCKER_ALLOWED_VOLUMES=/tmp,/var/log,/home/user/projects
```

### Privileged Mode
Disable privileged containers by default:
```env
DOCKER_ALLOW_PRIVILEGED=false
```

### Network Access
Control Docker daemon access via `DOCKER_HOST` configuration.

## Examples

### Container Operations
```
List all running containers
Create a new nginx container with port mapping 80:8080
Start container my-app
Get logs from container web-server with last 50 lines
```

### Image Operations
```
Pull the latest ubuntu image
Build an image from ./app directory with tag my-app:v1.0
List all Docker images
Remove image old-app:v1.0
```

### Docker Compose
```
Start services from docker-compose.yml in detached mode
Stop all services and remove volumes
List all running compose services
```

## Development

### Project Structure

```
src/
├── config.py          # Configuration management
├── docker/           # Docker service modules
│   ├── containers.py # Container operations
│   ├── images.py     # Image operations
│   ├── networks.py   # Network & volume operations
│   └── compose.py    # Docker Compose operations
└── main.py           # MCP server entry point
```

### Running Tests

```bash
# Install test dependencies
uv sync --dev

# Run tests
uv run pytest
```

## Troubleshooting

### Docker Connection Issues
- Verify Docker daemon is running: `docker ps`
- Check Docker socket permissions: `ls -la /var/run/docker.sock`
- For remote Docker: ensure `DOCKER_HOST` is correctly set

### Permission Denied
- Add user to docker group: `sudo usermod -aG docker $USER`
- Restart terminal session
- Verify with: `docker run hello-world`

### Container Creation Fails
- Check image availability: `docker images`
- Verify port conflicts: `netstat -tulpn | grep :8080`
- Review volume mount permissions

### Compose Issues
- Validate compose file: `docker-compose config`
- Check service dependencies
- Verify network connectivity

## Performance Tips

- Use `.dockerignore` files to reduce build context
- Implement multi-stage builds for smaller images
- Use volume mounts for development
- Configure resource limits for containers

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request