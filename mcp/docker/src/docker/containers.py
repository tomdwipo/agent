"""Docker Container management tools for Docker MCP Server."""

import asyncio
from typing import Dict, Any, Optional
import docker
from docker.errors import DockerException, APIError, NotFound

from ..config import Config


class ContainerTools:
    """Tools for Docker container operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = docker.DockerClient(**self.config.get_docker_client_kwargs())
        return self._client
    
    async def list_containers(self, all_containers: bool = False, filters: Dict[str, Any] = None) -> str:
        """List Docker containers."""
        try:
            containers = await asyncio.to_thread(
                self.client.containers.list, all=all_containers, filters=filters
            )
            
            if not containers:
                status = "all" if all_containers else "running"
                return f"No {status} containers found"
            
            result = "Docker Containers:\n\n"
            for container in containers:
                result += f"• {container.name}\n"
                result += f"  ID: {container.short_id}\n"
                result += f"  Image: {container.image.tags[0] if container.image.tags else container.image.id[:12]}\n"
                result += f"  Status: {container.status}\n"
                
                if container.status == "running":
                    result += f"  Ports: {self._format_ports(container.ports)}\n"
                
                result += "\n"
            
            return result
        except Exception as e:
            return f"Error listing containers: {str(e)}"
    
    async def create_container(self, image: str, name: str = None, **kwargs) -> str:
        """Create a new Docker container."""
        try:
            # Extract and validate parameters
            command = kwargs.get("command")
            ports = kwargs.get("ports", {})
            environment = kwargs.get("environment", {})
            volumes = kwargs.get("volumes", {})
            detach = kwargs.get("detach", True)
            
            # Validate volumes if restrictions are set
            if volumes and self.config.allowed_volumes:
                for host_path in volumes.keys():
                    if not self.config.is_volume_allowed(host_path):
                        return f"Volume mount not allowed: {host_path}"
            
            container = await asyncio.to_thread(
                self.client.containers.create,
                image=image,
                name=name,
                command=command,
                ports=ports,
                environment=environment,
                volumes=volumes,
                detach=detach
            )
            
            return f"Container created: {container.name} ({container.short_id})"
        except APIError as e:
            return f"Docker API error: {str(e)}"
        except Exception as e:
            return f"Error creating container: {str(e)}"
    
    async def start_container(self, container_id: str) -> str:
        """Start a Docker container."""
        try:
            container = self.client.containers.get(container_id)
            await asyncio.to_thread(container.start)
            return f"Container {container.name} started successfully"
        except NotFound:
            return f"Container {container_id} not found"
        except Exception as e:
            return f"Error starting container: {str(e)}"
    
    async def stop_container(self, container_id: str, timeout: int = 10) -> str:
        """Stop a Docker container."""
        try:
            container = self.client.containers.get(container_id)
            await asyncio.to_thread(container.stop, timeout=timeout)
            return f"Container {container.name} stopped successfully"
        except NotFound:
            return f"Container {container_id} not found"
        except Exception as e:
            return f"Error stopping container: {str(e)}"
    
    async def remove_container(self, container_id: str, force: bool = False) -> str:
        """Remove a Docker container."""
        try:
            container = self.client.containers.get(container_id)
            container_name = container.name
            await asyncio.to_thread(container.remove, force=force)
            return f"Container {container_name} removed successfully"
        except NotFound:
            return f"Container {container_id} not found"
        except Exception as e:
            return f"Error removing container: {str(e)}"
    
    async def get_logs(self, container_id: str, tail: int = 100, follow: bool = False) -> str:
        """Get container logs."""
        try:
            container = self.client.containers.get(container_id)
            
            if follow:
                # For following logs, we'll just get recent logs due to MCP limitations
                logs = await asyncio.to_thread(
                    container.logs, tail=tail, timestamps=True
                )
            else:
                logs = await asyncio.to_thread(
                    container.logs, tail=tail, timestamps=True
                )
            
            if isinstance(logs, bytes):
                logs = logs.decode('utf-8', errors='replace')
            
            if not logs.strip():
                return f"No logs available for container {container.name}"
            
            return f"Logs for {container.name}:\n\n{logs}"
        except NotFound:
            return f"Container {container_id} not found"
        except Exception as e:
            return f"Error getting logs: {str(e)}"
    
    async def inspect_container(self, container_id: str) -> str:
        """Get detailed container information."""
        try:
            container = self.client.containers.get(container_id)
            attrs = container.attrs
            
            result = f"Container Details: {container.name}\n\n"
            result += f"ID: {attrs['Id'][:12]}\n"
            result += f"Image: {attrs['Config']['Image']}\n"
            result += f"Status: {attrs['State']['Status']}\n"
            result += f"Created: {attrs['Created']}\n"
            
            if attrs['State']['Running']:
                result += f"Started: {attrs['State']['StartedAt']}\n"
            
            # Network information
            networks = attrs.get('NetworkSettings', {}).get('Networks', {})
            if networks:
                result += "\nNetworks:\n"
                for net_name, net_info in networks.items():
                    result += f"  {net_name}: {net_info.get('IPAddress', 'N/A')}\n"
            
            # Port mappings
            ports = attrs.get('NetworkSettings', {}).get('Ports', {})
            if ports:
                result += "\nPort Mappings:\n"
                for container_port, host_info in ports.items():
                    if host_info:
                        host_port = host_info[0]['HostPort']
                        result += f"  {container_port} → {host_port}\n"
            
            return result
        except NotFound:
            return f"Container {container_id} not found"
        except Exception as e:
            return f"Error inspecting container: {str(e)}"
    
    def _format_ports(self, ports: Dict) -> str:
        """Format container port mappings."""
        if not ports:
            return "None"
        
        port_mappings = []
        for container_port, host_info in ports.items():
            if host_info and len(host_info) > 0:
                host_port = host_info[0]['HostPort']
                port_mappings.append(f"{host_port}:{container_port}")
        
        return ", ".join(port_mappings) if port_mappings else "None"