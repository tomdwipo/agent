#!/usr/bin/env python3
"""
Firebase Crashlytics MCP Server

A Model Context Protocol server for Firebase Crashlytics integration.
Provides crash analysis, data retrieval, and AI-powered solution suggestions.
"""

import asyncio
import argparse
import os
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from src.firebase.crashlytics import CrashlyticsTools
from src.firebase.analysis import AnalysisTools
from src.ai.solutions import SolutionGenerator
from src.config import Config


# Initialize server
server = Server("firebase-crashlytics-mcp")

# Global configuration
config = Config()

# Initialize tool classes
crashlytics_tools = CrashlyticsTools(config)
analysis_tools = AnalysisTools(config)
solution_generator = SolutionGenerator(config)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available Firebase Crashlytics tools."""
    tools = []
    
    # Crash Data Retrieval Tools
    tools.extend([
        types.Tool(
            name="list-crashes",
            description="List recent crashes for an app",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {
                        "type": "string",
                        "description": "Firebase app ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of crashes to return (default: 20)"
                    },
                    "severity": {
                        "type": "string",
                        "description": "Filter by severity: CRITICAL, HIGH, MEDIUM, LOW"
                    },
                    "platform": {
                        "type": "string",
                        "description": "Filter by platform: ios, android"
                    }
                },
                "required": ["app_id"]
            }
        ),
        types.Tool(
            name="get-crash-details",
            description="Get detailed information about a specific crash",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "crash_id": {"type": "string", "description": "Specific crash ID"},
                    "include_stacktrace": {"type": "boolean", "description": "Include stack trace (default: true)"}
                },
                "required": ["app_id", "crash_id"]
            }
        ),
        types.Tool(
            name="get-crash-trends",
            description="Get crash trends and statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "time_period": {"type": "string", "description": "Time period: 1d, 7d, 30d (default: 7d)"},
                    "group_by": {"type": "string", "description": "Group by: severity, platform, version"}
                },
                "required": ["app_id"]
            }
        )
    ])
    
    # Crash Analysis Tools
    tools.extend([
        types.Tool(
            name="analyze-crash-pattern",
            description="Analyze crash patterns and identify common issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "crash_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of crash IDs to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "description": "Type of analysis: similarity, frequency, impact"
                    }
                },
                "required": ["app_id", "crash_ids"]
            }
        ),
        types.Tool(
            name="get-affected-users",
            description="Get information about users affected by crashes",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "crash_id": {"type": "string", "description": "Specific crash ID"},
                    "time_range": {"type": "string", "description": "Time range: 1h, 6h, 24h, 7d"}
                },
                "required": ["app_id", "crash_id"]
            }
        )
    ])
    
    # AI Solution Tools
    tools.extend([
        types.Tool(
            name="generate-solution",
            description="Generate AI-powered solution suggestions for a crash",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "crash_id": {"type": "string", "description": "Crash ID to analyze"},
                    "detail_level": {
                        "type": "string",
                        "description": "Solution detail level: basic, detailed, expert"
                    },
                    "include_code": {"type": "boolean", "description": "Include code examples (default: true)"},
                    "platform_context": {"type": "string", "description": "Additional platform context"}
                },
                "required": ["app_id", "crash_id"]
            }
        ),
        types.Tool(
            name="bulk-solution-analysis",
            description="Generate solutions for multiple related crashes",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "crash_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of crash IDs to analyze"
                    },
                    "priority_order": {"type": "boolean", "description": "Order by severity/impact"}
                },
                "required": ["app_id", "crash_ids"]
            }
        ),
        types.Tool(
            name="suggest-preventive-measures",
            description="Suggest preventive measures based on crash patterns",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "time_period": {"type": "string", "description": "Analysis period: 7d, 30d, 90d"},
                    "focus_area": {"type": "string", "description": "Focus area: performance, memory, network, ui"}
                },
                "required": ["app_id"]
            }
        )
    ])
    
    # Reporting and Export Tools
    tools.extend([
        types.Tool(
            name="generate-crash-report",
            description="Generate comprehensive crash report",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Firebase app ID"},
                    "time_period": {"type": "string", "description": "Report period: 7d, 30d"},
                    "include_solutions": {"type": "boolean", "description": "Include AI solutions"},
                    "format": {"type": "string", "description": "Report format: markdown, json"}
                },
                "required": ["app_id"]
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
        # Crash Data Tools
        if name == "list-crashes":
            result = await crashlytics_tools.list_crashes(
                app_id=arguments["app_id"],
                limit=arguments.get("limit", 20),
                severity=arguments.get("severity"),
                platform=arguments.get("platform")
            )
        elif name == "get-crash-details":
            result = await crashlytics_tools.get_crash_details(
                app_id=arguments["app_id"],
                crash_id=arguments["crash_id"],
                include_stacktrace=arguments.get("include_stacktrace", True)
            )
        elif name == "get-crash-trends":
            result = await crashlytics_tools.get_crash_trends(
                app_id=arguments["app_id"],
                time_period=arguments.get("time_period", "7d"),
                group_by=arguments.get("group_by")
            )
        
        # Analysis Tools
        elif name == "analyze-crash-pattern":
            result = await analysis_tools.analyze_crash_pattern(
                app_id=arguments["app_id"],
                crash_ids=arguments["crash_ids"],
                analysis_type=arguments.get("analysis_type", "similarity")
            )
        elif name == "get-affected-users":
            result = await analysis_tools.get_affected_users(
                app_id=arguments["app_id"],
                crash_id=arguments["crash_id"],
                time_range=arguments.get("time_range", "24h")
            )
        
        # AI Solution Tools
        elif name == "generate-solution":
            result = await solution_generator.generate_solution(
                app_id=arguments["app_id"],
                crash_id=arguments["crash_id"],
                detail_level=arguments.get("detail_level", config.solution_detail_level),
                include_code=arguments.get("include_code", True),
                platform_context=arguments.get("platform_context")
            )
        elif name == "bulk-solution-analysis":
            result = await solution_generator.bulk_solution_analysis(
                app_id=arguments["app_id"],
                crash_ids=arguments["crash_ids"],
                priority_order=arguments.get("priority_order", True)
            )
        elif name == "suggest-preventive-measures":
            result = await solution_generator.suggest_preventive_measures(
                app_id=arguments["app_id"],
                time_period=arguments.get("time_period", "30d"),
                focus_area=arguments.get("focus_area")
            )
        
        # Reporting Tools
        elif name == "generate-crash-report":
            result = await analysis_tools.generate_crash_report(
                app_id=arguments["app_id"],
                time_period=arguments.get("time_period", "7d"),
                include_solutions=arguments.get("include_solutions", True),
                format=arguments.get("format", "markdown")
            )
        
        else:
            result = f"Unknown tool: {name}"
        
        return [types.TextContent(type="text", text=str(result))]
    
    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main server entry point."""
    parser = argparse.ArgumentParser(description="Firebase Crashlytics MCP Server")
    parser.add_argument(
        "--firebase-project-id",
        type=str,
        help="Firebase project ID"
    )
    parser.add_argument(
        "--credentials-path",
        type=str,
        help="Path to Firebase credentials JSON file"
    )
    parser.add_argument(
        "--enable-ai",
        action="store_true",
        help="Enable AI solution generation"
    )
    
    args = parser.parse_args()
    
    # Override config if arguments provided
    if args.firebase_project_id:
        config.firebase_project_id = args.firebase_project_id
    if args.credentials_path:
        config.firebase_credentials_path = args.credentials_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.credentials_path
    if args.enable_ai:
        config.enable_ai_solutions = True
    
    # Validate configuration
    issues = config.validate_configuration()
    if issues:
        print("⚠️  Configuration issues found:")
        for key, issue in issues.items():
            print(f"  - {key}: {issue}")
        print("\nPlease fix configuration issues before starting the server.")
        return
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="firebase-crashlytics-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())