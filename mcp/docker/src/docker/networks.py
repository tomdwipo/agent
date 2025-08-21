"""Docker Network management tools for Docker MCP Server."""

import asyncio
import docker
from docker.errors import DockerException, APIError, NotFound

from ..config import Config


class NetworkTools:
    """Tools for Docker network operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = docker.DockerClient(**self.config.get_docker_client_kwargs())
        return self._client
    
    async def list_networks(self) -> str:
        """List Docker networks."""
        try:
            networks = await asyncio.to_thread(self.client.networks.list)
            
            if not networks:
                return "No networks found"
            
            result = "Docker Networks:\n\n"
            for network in networks:
                result += f"• {network.name}\n"
                result += f"  ID: {network.short_id}\n"
                result += f"  Driver: {network.attrs.get('Driver', 'unknown')}\n"
                result += f"  Scope: {network.attrs.get('Scope', 'unknown')}\n"
                
                # Connected containers
                containers = network.attrs.get('Containers', {})
                if containers:
                    result += f"  Containers: {len(containers)} connected\n"
                
                result += "\n"
            
            return result
        except Exception as e:
            return f"Error listing networks: {str(e)}"
    
    async def create_network(self, name: str, driver: str = "bridge") -> str:
        """Create a Docker network."""
        try:
            network = await asyncio.to_thread(
                self.client.networks.create, name, driver=driver
            )
            return f"Network created: {name} ({network.short_id})"
        except APIError as e:
            return f"Docker API error creating network: {str(e)}"
        except Exception as e:
            return f"Error creating network: {str(e)}"
    
    async def remove_network(self, network_id: str) -> str:
        """Remove a Docker network."""
        try:
            network = self.client.networks.get(network_id)
            network_name = network.name
            await asyncio.to_thread(network.remove)
            return f"Network {network_name} removed successfully"
        except NotFound:
            return f"Network {network_id} not found"
        except Exception as e:
            return f"Error removing network: {str(e)}"


class VolumeTools:
    """Tools for Docker volume operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = docker.DockerClient(**self.config.get_docker_client_kwargs())
        return self._client
    
    async def list_volumes(self) -> str:
        """List Docker volumes."""
        try:
            volumes = await asyncio.to_thread(self.client.volumes.list)
            
            if not volumes:
                return "No volumes found"
            
            result = "Docker Volumes:\n\n"
            for volume in volumes:
                result += f"• {volume.name}\n"
                result += f"  Driver: {volume.attrs.get('Driver', 'unknown')}\n"
                result += f"  Mount Point: {volume.attrs.get('Mountpoint', 'unknown')}\n"
                result += f"  Created: {volume.attrs.get('CreatedAt', 'unknown')[:19]}\n"
                result += "\n"
            
            return result
        except Exception as e:
            return f"Error listing volumes: {str(e)}"
    
    async def create_volume(self, name: str) -> str:
        """Create a Docker volume."""
        try:
            volume = await asyncio.to_thread(self.client.volumes.create, name)
            return f"Volume created: {name}"
        except APIError as e:
            return f"Docker API error creating volume: {str(e)}"
        except Exception as e:
            return f"Error creating volume: {str(e)}"
    
    async def remove_volume(self, volume_name: str) -> str:
        """Remove a Docker volume."""
        try:
            volume = self.client.volumes.get(volume_name)
            await asyncio.to_thread(volume.remove)
            return f"Volume {volume_name} removed successfully"
        except NotFound:
            return f"Volume {volume_name} not found"
        except Exception as e:
            return f"Error removing volume: {str(e)}"