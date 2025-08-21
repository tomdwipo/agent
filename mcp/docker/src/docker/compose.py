"""Docker Compose management tools for Docker MCP Server."""

import asyncio
import os
import subprocess
import yaml
from typing import Optional

from ..config import Config


class ComposeTools:
    """Tools for Docker Compose operations."""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def up(self, file_path: str, detach: bool = True, build: bool = False) -> str:
        """Start Docker Compose services."""
        try:
            if not os.path.exists(file_path):
                return f"Docker Compose file not found: {file_path}"
            
            cmd = ["docker-compose", "-f", file_path]
            
            if self.config.compose_project_name:
                cmd.extend(["-p", self.config.compose_project_name])
            
            cmd.append("up")
            
            if detach:
                cmd.append("-d")
            if build:
                cmd.append("--build")
            
            result = await asyncio.to_thread(
                subprocess.run, cmd, capture_output=True, text=True, timeout=300
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                return f"Docker Compose services started successfully\n\n{output}"
            else:
                return f"Docker Compose up failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Docker Compose up timed out after 5 minutes"
        except Exception as e:
            return f"Error running docker-compose up: {str(e)}"
    
    async def down(self, file_path: str, remove_volumes: bool = False) -> str:
        """Stop Docker Compose services."""
        try:
            if not os.path.exists(file_path):
                return f"Docker Compose file not found: {file_path}"
            
            cmd = ["docker-compose", "-f", file_path]
            
            if self.config.compose_project_name:
                cmd.extend(["-p", self.config.compose_project_name])
            
            cmd.append("down")
            
            if remove_volumes:
                cmd.append("-v")
            
            result = await asyncio.to_thread(
                subprocess.run, cmd, capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                return f"Docker Compose services stopped successfully\n\n{output}"
            else:
                return f"Docker Compose down failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Docker Compose down timed out after 2 minutes"
        except Exception as e:
            return f"Error running docker-compose down: {str(e)}"
    
    async def ps(self, file_path: str) -> str:
        """List Docker Compose services."""
        try:
            if not os.path.exists(file_path):
                return f"Docker Compose file not found: {file_path}"
            
            cmd = ["docker-compose", "-f", file_path]
            
            if self.config.compose_project_name:
                cmd.extend(["-p", self.config.compose_project_name])
            
            cmd.append("ps")
            
            result = await asyncio.to_thread(
                subprocess.run, cmd, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                return f"Docker Compose services:\n\n{output}"
            else:
                return f"Docker Compose ps failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Docker Compose ps timed out"
        except Exception as e:
            return f"Error running docker-compose ps: {str(e)}"
    
    async def logs(self, file_path: str, service: Optional[str] = None, tail: int = 100) -> str:
        """Get Docker Compose service logs."""
        try:
            if not os.path.exists(file_path):
                return f"Docker Compose file not found: {file_path}"
            
            cmd = ["docker-compose", "-f", file_path]
            
            if self.config.compose_project_name:
                cmd.extend(["-p", self.config.compose_project_name])
            
            cmd.extend(["logs", "--tail", str(tail)])
            
            if service:
                cmd.append(service)
            
            result = await asyncio.to_thread(
                subprocess.run, cmd, capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                service_info = f" for service {service}" if service else ""
                return f"Docker Compose logs{service_info}:\n\n{output}"
            else:
                return f"Docker Compose logs failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Docker Compose logs timed out"
        except Exception as e:
            return f"Error getting docker-compose logs: {str(e)}"
    
    async def validate_compose_file(self, file_path: str) -> str:
        """Validate Docker Compose file syntax."""
        try:
            if not os.path.exists(file_path):
                return f"Docker Compose file not found: {file_path}"
            
            # Basic YAML validation
            with open(file_path, 'r') as f:
                try:
                    compose_data = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    return f"Invalid YAML syntax: {str(e)}"
            
            # Check for required sections
            if not isinstance(compose_data, dict):
                return "Docker Compose file must be a YAML object"
            
            if 'services' not in compose_data:
                return "Docker Compose file must contain a 'services' section"
            
            # Use docker-compose config to validate
            cmd = ["docker-compose", "-f", file_path, "config", "--quiet"]
            
            result = await asyncio.to_thread(
                subprocess.run, cmd, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                services = list(compose_data['services'].keys())
                return f"Docker Compose file is valid\nServices: {', '.join(services)}"
            else:
                return f"Docker Compose validation failed: {result.stderr}"
                
        except Exception as e:
            return f"Error validating compose file: {str(e)}"