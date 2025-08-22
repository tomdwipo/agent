#!/usr/bin/env python3
"""
Slack MCP Server

A Model Context Protocol server for Slack workspace automation and messaging.
Provides tools to interact with Slack channels, send messages, manage files,
and automate Slack workflows for SDLC integration.
"""

from mcp.server.fastmcp import FastMCP, Image
from contextlib import asynccontextmanager
from argparse import ArgumentParser
from src.slack import SlackClient
from textwrap import dedent
import asyncio


parser = ArgumentParser()
parser.add_argument('--bot-token', type=str, help='Slack Bot Token (xoxb-...)')
parser.add_argument('--user-token', type=str, help='Slack User Token (xoxp-...)')
parser.add_argument('--app-token', type=str, help='Slack App Token (xapp-...)')
parser.add_argument('--workspace', type=str, help='Slack workspace name')
parser.add_argument('--default-channel', type=str, default='general', help='Default channel for messages')
args = parser.parse_args()

instructions = dedent('''
Slack MCP server provides tools to interact with Slack workspaces,
enabling automated messaging, channel management, file sharing, and workflow automation.
Supports both bot and user token authentication for comprehensive Slack integration.
''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    await asyncio.sleep(1)  # Simulate startup latency
    yield

mcp = FastMCP(name="Slack-MCP", instructions=instructions)

# Initialize Slack client
slack_client = SlackClient(
    bot_token=args.bot_token,
    user_token=args.user_token,
    app_token=args.app_token,
    workspace=args.workspace,
    default_channel=args.default_channel
)

@mcp.tool(name='Send-Message-Tool', description='Send a message to a Slack channel or user')
def send_message_tool(channel: str, text: str, thread_ts: str = None, reply_broadcast: bool = False):
    """Send a message to a Slack channel or direct message."""
    result = slack_client.send_message(channel, text, thread_ts, reply_broadcast)
    return result

@mcp.tool(name='Get-Messages-Tool', description='Get messages from a Slack channel')
def get_messages_tool(channel: str, limit: int = 10, latest: str = None, oldest: str = None):
    """Get recent messages from a Slack channel."""
    result = slack_client.get_messages(channel, limit, latest, oldest)
    return result

@mcp.tool(name='Channel-List-Tool', description='List all channels in the workspace')
def channel_list_tool(types: str = "public_channel,private_channel", exclude_archived: bool = True):
    """
    List channels in the workspace.
    Types: public_channel, private_channel, mpim, im
    """
    result = slack_client.list_channels(types, exclude_archived)
    return result

@mcp.tool(name='Channel-Create-Tool', description='Create a new Slack channel')
def channel_create_tool(name: str, is_private: bool = False):
    """Create a new Slack channel."""
    result = slack_client.create_channel(name, is_private)
    return result

@mcp.tool(name='Channel-Join-Tool', description='Join a Slack channel')
def channel_join_tool(channel: str):
    """Join a Slack channel."""
    result = slack_client.join_channel(channel)
    return result

@mcp.tool(name='Channel-Leave-Tool', description='Leave a Slack channel')
def channel_leave_tool(channel: str):
    """Leave a Slack channel."""
    result = slack_client.leave_channel(channel)
    return result

@mcp.tool(name='Channel-Info-Tool', description='Get information about a Slack channel')
def channel_info_tool(channel: str):
    """Get detailed information about a Slack channel."""
    result = slack_client.get_channel_info(channel)
    return result

@mcp.tool(name='User-List-Tool', description='List users in the workspace')
def user_list_tool(limit: int = 100, presence: bool = False):
    """List users in the Slack workspace."""
    result = slack_client.list_users(limit, presence)
    return result

@mcp.tool(name='User-Info-Tool', description='Get information about a Slack user')
def user_info_tool(user: str):
    """Get detailed information about a Slack user."""
    result = slack_client.get_user_info(user)
    return result

@mcp.tool(name='Upload-File-Tool', description='Upload a file to Slack')
def upload_file_tool(file_path: str, channels: str = None, title: str = None, initial_comment: str = None):
    """Upload a file to Slack channels."""
    result = slack_client.upload_file(file_path, channels, title, initial_comment)
    return result

@mcp.tool(name='Download-File-Tool', description='Download a file from Slack')
def download_file_tool(file_url: str, save_path: str = None):
    """Download a file shared in Slack."""
    result = slack_client.download_file(file_url, save_path)
    return result

@mcp.tool(name='Search-Messages-Tool', description='Search for messages in Slack')
def search_messages_tool(query: str, sort: str = "timestamp", sort_dir: str = "desc", count: int = 20):
    """
    Search for messages in Slack.
    Sort options: timestamp, score
    Sort direction: asc, desc
    """
    result = slack_client.search_messages(query, sort, sort_dir, count)
    return result

@mcp.tool(name='Set-Status-Tool', description='Set user status in Slack')
def set_status_tool(status_text: str, status_emoji: str = None, status_expiration: int = 0):
    """Set your status in Slack."""
    result = slack_client.set_status(status_text, status_emoji, status_expiration)
    return result

@mcp.tool(name='React-Tool', description='Add reaction to a Slack message')
def react_tool(channel: str, timestamp: str, name: str):
    """Add an emoji reaction to a Slack message."""
    result = slack_client.add_reaction(channel, timestamp, name)
    return result

@mcp.tool(name='Pin-Message-Tool', description='Pin a message in a Slack channel')
def pin_message_tool(channel: str, timestamp: str):
    """Pin a message in a Slack channel."""
    result = slack_client.pin_message(channel, timestamp)
    return result

@mcp.tool(name='Unpin-Message-Tool', description='Unpin a message in a Slack channel')
def unpin_message_tool(channel: str, timestamp: str):
    """Unpin a message in a Slack channel."""
    result = slack_client.unpin_message(channel, timestamp)
    return result

@mcp.tool(name='Schedule-Message-Tool', description='Schedule a message to be sent later')
def schedule_message_tool(channel: str, text: str, post_at: int):
    """Schedule a message to be sent at a specific time (Unix timestamp)."""
    result = slack_client.schedule_message(channel, text, post_at)
    return result

@mcp.tool(name='Update-Message-Tool', description='Update an existing Slack message')
def update_message_tool(channel: str, timestamp: str, text: str):
    """Update an existing Slack message."""
    result = slack_client.update_message(channel, timestamp, text)
    return result

@mcp.tool(name='Delete-Message-Tool', description='Delete a Slack message')
def delete_message_tool(channel: str, timestamp: str):
    """Delete a Slack message."""
    result = slack_client.delete_message(channel, timestamp)
    return result

@mcp.tool(name='Create-Reminder-Tool', description='Create a reminder in Slack')
def create_reminder_tool(text: str, time: str, user: str = None):
    """Create a reminder in Slack."""
    result = slack_client.create_reminder(text, time, user)
    return result

@mcp.tool(name='Workspace-Info-Tool', description='Get information about the Slack workspace')
def workspace_info_tool():
    """Get information about the current Slack workspace."""
    result = slack_client.get_workspace_info()
    return result

@mcp.tool(name='Send-DM-Tool', description='Send a direct message to a user')
def send_dm_tool(user: str, text: str):
    """Send a direct message to a Slack user."""
    result = slack_client.send_direct_message(user, text)
    return result

@mcp.tool(name='Invite-User-Tool', description='Invite a user to a channel')
def invite_user_tool(channel: str, user: str):
    """Invite a user to a Slack channel."""
    result = slack_client.invite_user_to_channel(channel, user)
    return result

@mcp.tool(name='Remove-User-Tool', description='Remove a user from a channel')
def remove_user_tool(channel: str, user: str):
    """Remove a user from a Slack channel."""
    result = slack_client.remove_user_from_channel(channel, user)
    return result

@mcp.tool(name='Archive-Channel-Tool', description='Archive a Slack channel')
def archive_channel_tool(channel: str):
    """Archive a Slack channel."""
    result = slack_client.archive_channel(channel)
    return result

@mcp.tool(name='Unarchive-Channel-Tool', description='Unarchive a Slack channel')
def unarchive_channel_tool(channel: str):
    """Unarchive a Slack channel."""
    result = slack_client.unarchive_channel(channel)
    return result

if __name__ == '__main__':
    mcp.run()