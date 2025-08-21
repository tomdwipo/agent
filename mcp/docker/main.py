#!/usr/bin/env python3
"""
Docker MCP Server

A Model Context Protocol server for Docker container management.
Provides tools for managing containers, images, networks, and Docker Compose services.
"""

import asyncio
import argparse
import os
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from src.docker.containers import ContainerTools
from src.docker.images import ImageTools
from src.docker.networks import NetworkTools, VolumeTools
from src.docker.compose import ComposeTools
from src.config import Config


# Initialize server
server = Server("docker-mcp")

# Global configuration
config = Config()

# Initialize tool classes
container_tools = ContainerTools(config)
image_tools = ImageTools(config)
network_tools = NetworkTools(config)
compose_tools = ComposeTools(config)
volume_tools = VolumeTools(config)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available Docker tools."""
    tools = []
    
    # Container Management Tools
    tools.extend([
        types.Tool(
            name="list-containers",
            description="List Docker containers",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {
                        "type": "boolean",
                        "description": "Show all containers (default: only running)"
                    },
                    "filters": {
                        "type": "object", 
                        "description": "Filters to apply (e.g., {'status': 'running'})"
                    }
                }
            }
        ),
        types.Tool(
            name="create-container",
            description="Create a new Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Container image"},
                    "name": {"type": "string", "description": "Container name"},
                    "command": {"type": "string", "description": "Command to run (optional)"},
                    "ports": {"type": "object", "description": "Port mappings (e.g., {'80/tcp': 8080})"},
                    "environment": {"type": "object", "description": "Environment variables"},
                    "volumes": {"type": "object", "description": "Volume mounts"},
                    "detach": {"type": "boolean", "description": "Run in background (default: true)"}
                },
                "required": ["image"]
            }
        ),
        types.Tool(
            name="start-container",
            description="Start a Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_id": {"type": "string", "description": "Container ID or name"}
                },
                "required": ["container_id"]
            }
        ),
        types.Tool(
            name="stop-container",
            description="Stop a Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_id": {"type": "string", "description": "Container ID or name"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds (default: 10)"}
                },
                "required": ["container_id"]
            }
        ),
        types.Tool(
            name="remove-container",
            description="Remove a Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_id": {"type": "string", "description": "Container ID or name"},
                    "force": {"type": "boolean", "description": "Force removal (default: false)"}
                },
                "required": ["container_id"]
            }
        ),
        types.Tool(
            name="container-logs",
            description="Get container logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_id": {"type": "string", "description": "Container ID or name"},
                    "tail": {"type": "integer", "description": "Number of lines from end (default: 100)"},
                    "follow": {"type": "boolean", "description": "Follow log output (default: false)"}
                },
                "required": ["container_id"]
            }
        )
    ])
    
    # Image Management Tools
    tools.extend([
        types.Tool(
            name="list-images",
            description="List Docker images",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {"type": "boolean", "description": "Show all images including intermediates"}
                }
            }
        ),
        types.Tool(
            name="pull-image",
            description="Pull a Docker image",
            inputSchema={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name with optional tag"},
                    "tag": {"type": "string", "description": "Specific tag (default: latest)"}
                },
                "required": ["image"]
            }
        ),
        types.Tool(
            name="build-image",
            description="Build a Docker image",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Build context path"},
                    "tag": {"type": "string", "description": "Image tag"},
                    "dockerfile": {"type": "string", "description": "Dockerfile path (default: Dockerfile)"}
                },
                "required": ["path", "tag"]
            }
        ),
        types.Tool(
            name="remove-image",
            description="Remove a Docker image",
            inputSchema={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Image name or ID"},
                    "force": {"type": "boolean", "description": "Force removal (default: false)"}
                },
                "required": ["image"]
            }
        )
    ])
    
    # Network Management Tools
    tools.extend([
        types.Tool(
            name="list-networks",
            description="List Docker networks",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="create-network",
            description="Create a Docker network",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Network name"},
                    "driver": {"type": "string", "description": "Network driver (default: bridge)"}
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="remove-network",
            description="Remove a Docker network",
            inputSchema={
                "type": "object",
                "properties": {
                    "network_id": {"type": "string", "description": "Network ID or name"}
                },
                "required": ["network_id"]
            }
        )
    ])
    
    # Volume Management Tools
    tools.extend([
        types.Tool(
            name="list-volumes",
            description="List Docker volumes",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="create-volume",
            description="Create a Docker volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Volume name"}
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="remove-volume",
            description="Remove a Docker volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume_name": {"type": "string", "description": "Volume name"}
                },
                "required": ["volume_name"]
            }
        )
    ])
    
    # Docker Compose Tools
    tools.extend([
        types.Tool(
            name="compose-up",
            description="Start Docker Compose services",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "docker-compose.yml path"},
                    "detach": {"type": "boolean", "description": "Run in background (default: true)"},
                    "build": {"type": "boolean", "description": "Build images before starting"}
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="compose-down",
            description="Stop Docker Compose services",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "docker-compose.yml path"},
                    "remove_volumes": {"type": "boolean", "description": "Remove volumes (default: false)"}
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="compose-ps",
            description="List Docker Compose services",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "docker-compose.yml path"}
                },
                "required": ["file_path"]
            }
        )
    ])
    
    return tools


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
    """Handle tool execution."""
    if arguments is None:
        arguments = {}
    
    try:
        # Container Tools
        if name == "list-containers":
            result = await container_tools.list_containers(
                all_containers=arguments.get("all", False),
                filters=arguments.get("filters", {})
            )
        elif name == "create-container":
            result = await container_tools.create_container(**arguments)
        elif name == "start-container":
            result = await container_tools.start_container(arguments["container_id"])
        elif name == "stop-container":
            result = await container_tools.stop_container(
                arguments["container_id"],
                timeout=arguments.get("timeout", 10)
            )
        elif name == "remove-container":
            result = await container_tools.remove_container(
                arguments["container_id"],
                force=arguments.get("force", False)
            )
        elif name == "container-logs":
            result = await container_tools.get_logs(
                arguments["container_id"],
                tail=arguments.get("tail", 100),
                follow=arguments.get("follow", False)
            )
        
        # Image Tools
        elif name == "list-images":
            result = await image_tools.list_images(all_images=arguments.get("all", False))
        elif name == "pull-image":
            result = await image_tools.pull_image(
                arguments["image"],
                tag=arguments.get("tag", "latest")
            )
        elif name == "build-image":
            result = await image_tools.build_image(**arguments)
        elif name == "remove-image":
            result = await image_tools.remove_image(
                arguments["image"],
                force=arguments.get("force", False)
            )
        
        # Network Tools
        elif name == "list-networks":
            result = await network_tools.list_networks()
        elif name == "create-network":
            result = await network_tools.create_network(
                arguments["name"],
                driver=arguments.get("driver", "bridge")
            )
        elif name == "remove-network":
            result = await network_tools.remove_network(arguments["network_id"])
        
        # Volume Tools
        elif name == "list-volumes":
            result = await volume_tools.list_volumes()
        elif name == "create-volume":
            result = await volume_tools.create_volume(arguments["name"])
        elif name == "remove-volume":
            result = await volume_tools.remove_volume(arguments["volume_name"])
        
        # Compose Tools
        elif name == "compose-up":
            result = await compose_tools.up(
                arguments["file_path"],
                detach=arguments.get("detach", True),
                build=arguments.get("build", False)
            )
        elif name == "compose-down":
            result = await compose_tools.down(
                arguments["file_path"],
                remove_volumes=arguments.get("remove_volumes", False)
            )
        elif name == "compose-ps":
            result = await compose_tools.ps(arguments["file_path"])
        
        else:
            result = f"Unknown tool: {name}"
        
        return [types.TextContent(type="text", text=str(result))]
    
    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main server entry point."""
    parser = argparse.ArgumentParser(description="Docker MCP Server")
    parser.add_argument(
        "--docker-host",
        type=str,
        help="Docker daemon host (default: unix:///var/run/docker.sock)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Docker client timeout in seconds"
    )
    
    args = parser.parse_args()
    
    # Override config if arguments provided
    if args.docker_host:
        config.docker_host = args.docker_host
    if args.timeout:
        config.timeout = args.timeout
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="docker-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())