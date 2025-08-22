"""Configuration module for Docker MCP Server."""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration management for Docker MCP Server."""
    
    def __init__(self):
        load_dotenv()
        
        # Docker daemon configuration
        self.docker_host = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
        self.docker_tls_verify = os.getenv("DOCKER_TLS_VERIFY", "").lower() == "true"
        self.docker_cert_path = os.getenv("DOCKER_CERT_PATH")
        
        # Default settings
        self.default_network = os.getenv("DOCKER_DEFAULT_NETWORK", "bridge")
        self.default_registry = os.getenv("DOCKER_DEFAULT_REGISTRY", "docker.io")
        self.compose_project_name = os.getenv("COMPOSE_PROJECT_NAME", "mcp-docker")
        
        # Security settings
        self.allow_privileged = os.getenv("DOCKER_ALLOW_PRIVILEGED", "false").lower() == "true"
        self.allowed_volumes = os.getenv("DOCKER_ALLOWED_VOLUMES", "").split(",") if os.getenv("DOCKER_ALLOWED_VOLUMES") else []
        
        # Performance settings
        self.timeout = int(os.getenv("DOCKER_TIMEOUT", "30"))
        
    def get_docker_client_kwargs(self) -> dict:
        """Get Docker client configuration."""
        kwargs = {
            "base_url": self.docker_host,
            "timeout": self.timeout
        }
        
        if self.docker_tls_verify and self.docker_cert_path:
            kwargs["tls"] = True
            kwargs["cert_path"] = self.docker_cert_path
            
        return kwargs
    
    def is_volume_allowed(self, volume_path: str) -> bool:
        """Check if volume mount is allowed."""
        if not self.allowed_volumes:
            return True  # Allow all if no restrictions
        
        return any(volume_path.startswith(allowed) for allowed in self.allowed_volumes)