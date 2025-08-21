"""Docker Image management tools for Docker MCP Server."""

import asyncio
import os
from typing import Optional
import docker
from docker.errors import DockerException, APIError, NotFound, BuildError

from ..config import Config


class ImageTools:
    """Tools for Docker image operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = docker.DockerClient(**self.config.get_docker_client_kwargs())
        return self._client
    
    async def list_images(self, all_images: bool = False) -> str:
        """List Docker images."""
        try:
            images = await asyncio.to_thread(self.client.images.list, all=all_images)
            
            if not images:
                return "No images found"
            
            result = "Docker Images:\n\n"
            for image in images:
                # Get image name and tag
                tags = image.tags if image.tags else ["<none>:<none>"]
                
                for tag in tags:
                    result += f"• {tag}\n"
                    result += f"  ID: {image.short_id}\n"
                    result += f"  Size: {self._format_size(image.attrs.get('Size', 0))}\n"
                    result += f"  Created: {image.attrs.get('Created', 'Unknown')[:19]}\n"
                    result += "\n"
            
            return result
        except Exception as e:
            return f"Error listing images: {str(e)}"
    
    async def pull_image(self, image: str, tag: str = "latest") -> str:
        """Pull a Docker image."""
        try:
            # Construct full image name
            if ":" not in image:
                full_image = f"{image}:{tag}"
            else:
                full_image = image
            
            result_image = await asyncio.to_thread(
                self.client.images.pull, full_image
            )
            
            return f"Successfully pulled image: {full_image} ({result_image.short_id})"
        except APIError as e:
            return f"Docker API error pulling {image}: {str(e)}"
        except Exception as e:
            return f"Error pulling image: {str(e)}"
    
    async def build_image(self, path: str, tag: str, dockerfile: str = "Dockerfile") -> str:
        """Build a Docker image."""
        try:
            if not os.path.exists(path):
                return f"Build path does not exist: {path}"
            
            dockerfile_path = os.path.join(path, dockerfile)
            if not os.path.exists(dockerfile_path):
                return f"Dockerfile not found: {dockerfile_path}"
            
            # Build the image
            image, build_logs = await asyncio.to_thread(
                self.client.images.build,
                path=path,
                tag=tag,
                dockerfile=dockerfile,
                rm=True  # Remove intermediate containers
            )
            
            # Format build logs
            log_output = ""
            for log_entry in build_logs:
                if 'stream' in log_entry:
                    log_output += log_entry['stream']
            
            result = f"Successfully built image: {tag} ({image.short_id})\n\n"
            if log_output:
                result += f"Build output:\n{log_output[-1000:]}"  # Last 1000 chars
            
            return result
        except BuildError as e:
            return f"Build failed: {str(e)}"
        except Exception as e:
            return f"Error building image: {str(e)}"
    
    async def remove_image(self, image: str, force: bool = False) -> str:
        """Remove a Docker image."""
        try:
            self.client.images.remove(image, force=force)
            return f"Successfully removed image: {image}"
        except NotFound:
            return f"Image not found: {image}"
        except APIError as e:
            return f"Docker API error removing {image}: {str(e)}"
        except Exception as e:
            return f"Error removing image: {str(e)}"
    
    async def inspect_image(self, image: str) -> str:
        """Get detailed image information."""
        try:
            img = self.client.images.get(image)
            attrs = img.attrs
            
            result = f"Image Details: {image}\n\n"
            result += f"ID: {attrs['Id'][:19]}\n"
            result += f"Size: {self._format_size(attrs.get('Size', 0))}\n"
            result += f"Created: {attrs.get('Created', 'Unknown')[:19]}\n"
            
            # Tags
            if img.tags:
                result += f"Tags: {', '.join(img.tags)}\n"
            
            # Config information
            config = attrs.get('Config', {})
            if config.get('Env'):
                result += f"\nEnvironment Variables:\n"
                for env_var in config['Env'][:10]:  # Limit to first 10
                    result += f"  {env_var}\n"
            
            if config.get('ExposedPorts'):
                result += f"\nExposed Ports: {', '.join(config['ExposedPorts'].keys())}\n"
            
            # Layer information
            layers = attrs.get('RootFS', {}).get('Layers', [])
            if layers:
                result += f"\nLayers: {len(layers)} layers\n"
            
            return result
        except NotFound:
            return f"Image not found: {image}"
        except Exception as e:
            return f"Error inspecting image: {str(e)}"
    
    async def search_images(self, term: str, limit: int = 10) -> str:
        """Search for images on Docker Hub."""
        try:
            results = await asyncio.to_thread(
                self.client.images.search, term, limit=limit
            )
            
            if not results:
                return f"No images found for search term: {term}"
            
            result = f"Search results for '{term}':\n\n"
            for img_info in results:
                result += f"• {img_info['name']}\n"
                result += f"  Description: {img_info.get('description', 'N/A')[:100]}...\n"
                result += f"  Stars: {img_info.get('star_count', 0)}\n"
                result += f"  Official: {'Yes' if img_info.get('is_official') else 'No'}\n"
                result += "\n"
            
            return result
        except Exception as e:
            return f"Error searching images: {str(e)}"
    
    async def tag_image(self, image: str, repository: str, tag: str = "latest") -> str:
        """Tag a Docker image."""
        try:
            img = self.client.images.get(image)
            success = await asyncio.to_thread(img.tag, repository, tag)
            
            if success:
                return f"Successfully tagged {image} as {repository}:{tag}"
            else:
                return f"Failed to tag image {image}"
        except NotFound:
            return f"Image not found: {image}"
        except Exception as e:
            return f"Error tagging image: {str(e)}"
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"