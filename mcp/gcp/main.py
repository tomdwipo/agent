#!/usr/bin/env python3
"""
GCP MCP Server

A Model Context Protocol server for Google Cloud Platform integration.
Provides tools for managing GCP resources including Compute Engine, Storage, and IAM.
"""

import asyncio
import argparse
import os
from typing import Any, Sequence

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from src.gcp.compute import ComputeTools
from src.gcp.storage import StorageTools
from src.gcp.iam import IAMTools
from src.gcp.projects import ProjectTools
from src.config import Config


# Initialize server
server = Server("gcp-mcp")

# Global configuration
config = Config()

# Initialize tool classes
compute_tools = ComputeTools(config)
storage_tools = StorageTools(config)
iam_tools = IAMTools(config)
project_tools = ProjectTools(config)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available GCP tools."""
    tools = []
    
    # Compute Engine Tools
    tools.extend([
        types.Tool(
            name="list-instances",
            description="List all Compute Engine instances in a project/zone",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "GCP Project ID"
                    },
                    "zone": {
                        "type": "string",
                        "description": "GCP Zone (optional, lists all zones if not specified)"
                    }
                },
                "required": ["project_id"]
            }
        ),
        types.Tool(
            name="create-instance",
            description="Create a new Compute Engine instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "zone": {"type": "string", "description": "GCP Zone"},
                    "instance_name": {"type": "string", "description": "Instance name"},
                    "machine_type": {"type": "string", "description": "Machine type (default: e2-micro)"},
                    "image_family": {"type": "string", "description": "Image family (default: ubuntu-2204-lts)"},
                    "image_project": {"type": "string", "description": "Image project (default: ubuntu-os-cloud)"}
                },
                "required": ["project_id", "zone", "instance_name"]
            }
        ),
        types.Tool(
            name="stop-instance",
            description="Stop a Compute Engine instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "zone": {"type": "string", "description": "GCP Zone"},
                    "instance_name": {"type": "string", "description": "Instance name"}
                },
                "required": ["project_id", "zone", "instance_name"]
            }
        ),
        types.Tool(
            name="start-instance",
            description="Start a Compute Engine instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "zone": {"type": "string", "description": "GCP Zone"},
                    "instance_name": {"type": "string", "description": "Instance name"}
                },
                "required": ["project_id", "zone", "instance_name"]
            }
        ),
        types.Tool(
            name="delete-instance",
            description="Delete a Compute Engine instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "zone": {"type": "string", "description": "GCP Zone"},
                    "instance_name": {"type": "string", "description": "Instance name"}
                },
                "required": ["project_id", "zone", "instance_name"]
            }
        )
    ])
    
    # Cloud Storage Tools
    tools.extend([
        types.Tool(
            name="list-buckets",
            description="List all Cloud Storage buckets in a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"}
                },
                "required": ["project_id"]
            }
        ),
        types.Tool(
            name="create-bucket",
            description="Create a new Cloud Storage bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "bucket_name": {"type": "string", "description": "Bucket name"},
                    "location": {"type": "string", "description": "Bucket location (default: US)"}
                },
                "required": ["project_id", "bucket_name"]
            }
        ),
        types.Tool(
            name="list-objects",
            description="List objects in a Cloud Storage bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "Bucket name"},
                    "prefix": {"type": "string", "description": "Object prefix filter (optional)"}
                },
                "required": ["bucket_name"]
            }
        ),
        types.Tool(
            name="upload-object",
            description="Upload a file to Cloud Storage",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "Bucket name"},
                    "object_name": {"type": "string", "description": "Object name in bucket"},
                    "file_path": {"type": "string", "description": "Local file path"},
                    "content_type": {"type": "string", "description": "Content type (optional)"}
                },
                "required": ["bucket_name", "object_name", "file_path"]
            }
        ),
        types.Tool(
            name="download-object",
            description="Download a file from Cloud Storage",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "Bucket name"},
                    "object_name": {"type": "string", "description": "Object name in bucket"},
                    "destination_path": {"type": "string", "description": "Local destination path"}
                },
                "required": ["bucket_name", "object_name", "destination_path"]
            }
        )
    ])
    
    # IAM Tools
    tools.extend([
        types.Tool(
            name="list-service-accounts",
            description="List all service accounts in a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"}
                },
                "required": ["project_id"]
            }
        ),
        types.Tool(
            name="create-service-account",
            description="Create a new service account",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "account_id": {"type": "string", "description": "Service account ID"},
                    "display_name": {"type": "string", "description": "Display name"},
                    "description": {"type": "string", "description": "Description (optional)"}
                },
                "required": ["project_id", "account_id", "display_name"]
            }
        ),
        types.Tool(
            name="get-iam-policy",
            description="Get IAM policy for a resource",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"}
                },
                "required": ["project_id"]
            }
        )
    ])
    
    # Project Tools
    tools.extend([
        types.Tool(
            name="list-projects",
            description="List all accessible GCP projects",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="get-project",
            description="Get details of a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"}
                },
                "required": ["project_id"]
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
        # Compute Engine Tools
        if name == "list-instances":
            result = await compute_tools.list_instances(
                arguments["project_id"],
                arguments.get("zone")
            )
        elif name == "create-instance":
            result = await compute_tools.create_instance(
                project_id=arguments["project_id"],
                zone=arguments["zone"],
                instance_name=arguments["instance_name"],
                machine_type=arguments.get("machine_type", "e2-micro"),
                image_family=arguments.get("image_family", "ubuntu-2204-lts"),
                image_project=arguments.get("image_project", "ubuntu-os-cloud")
            )
        elif name == "stop-instance":
            result = await compute_tools.stop_instance(
                arguments["project_id"],
                arguments["zone"],
                arguments["instance_name"]
            )
        elif name == "start-instance":
            result = await compute_tools.start_instance(
                arguments["project_id"],
                arguments["zone"],
                arguments["instance_name"]
            )
        elif name == "delete-instance":
            result = await compute_tools.delete_instance(
                arguments["project_id"],
                arguments["zone"],
                arguments["instance_name"]
            )
        
        # Cloud Storage Tools
        elif name == "list-buckets":
            result = await storage_tools.list_buckets(arguments["project_id"])
        elif name == "create-bucket":
            result = await storage_tools.create_bucket(
                arguments["project_id"],
                arguments["bucket_name"],
                arguments.get("location", "US")
            )
        elif name == "list-objects":
            result = await storage_tools.list_objects(
                arguments["bucket_name"],
                arguments.get("prefix")
            )
        elif name == "upload-object":
            result = await storage_tools.upload_object(
                arguments["bucket_name"],
                arguments["object_name"],
                arguments["file_path"],
                arguments.get("content_type")
            )
        elif name == "download-object":
            result = await storage_tools.download_object(
                arguments["bucket_name"],
                arguments["object_name"],
                arguments["destination_path"]
            )
        
        # IAM Tools
        elif name == "list-service-accounts":
            result = await iam_tools.list_service_accounts(arguments["project_id"])
        elif name == "create-service-account":
            result = await iam_tools.create_service_account(
                arguments["project_id"],
                arguments["account_id"],
                arguments["display_name"],
                arguments.get("description")
            )
        elif name == "get-iam-policy":
            result = await iam_tools.get_iam_policy(arguments["project_id"])
        
        # Project Tools
        elif name == "list-projects":
            result = await project_tools.list_projects()
        elif name == "get-project":
            result = await project_tools.get_project(arguments["project_id"])
        
        else:
            result = f"Unknown tool: {name}"
        
        return [types.TextContent(type="text", text=str(result))]
    
    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main server entry point."""
    parser = argparse.ArgumentParser(description="GCP MCP Server")
    parser.add_argument(
        "--credentials-path",
        type=str,
        help="Path to GCP service account credentials JSON file"
    )
    parser.add_argument(
        "--project-id",
        type=str,
        help="Default GCP project ID"
    )
    
    args = parser.parse_args()
    
    # Set credentials if provided
    if args.credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.credentials_path
    
    # Set default project if provided
    if args.project_id:
        config.default_project_id = args.project_id
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="gcp-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())