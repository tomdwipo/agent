"""
Slack Client Management Module

Handles Slack API connections, messaging operations, and workspace management
using the official Slack SDK for Python.
"""

import os
import time
import json
from typing import Optional, Union, Dict, Any, List
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from dotenv import load_dotenv


class SlackClient:
    """Main Slack client management class."""
    
    def __init__(
        self,
        bot_token: Optional[str] = None,
        user_token: Optional[str] = None,
        app_token: Optional[str] = None,
        workspace: Optional[str] = None,
        default_channel: str = "general"
    ):
        """
        Initialize Slack client with tokens.
        
        Args:
            bot_token: Slack Bot Token (xoxb-...)
            user_token: Slack User Token (xoxp-...)
            app_token: Slack App Token (xapp-...)
            workspace: Slack workspace name
            default_channel: Default channel for messages
        """
        # Load environment variables
        load_dotenv()
        
        # Set tokens from parameters or environment
        self.bot_token = bot_token or os.getenv('SLACK_BOT_TOKEN')
        self.user_token = user_token or os.getenv('SLACK_USER_TOKEN')
        self.app_token = app_token or os.getenv('SLACK_APP_TOKEN')
        self.workspace = workspace or os.getenv('SLACK_WORKSPACE')
        self.default_channel = default_channel
        
        # Initialize WebClients
        self.bot_client = None
        self.user_client = None
        
        if self.bot_token:
            self.bot_client = WebClient(token=self.bot_token)
        
        if self.user_token:
            self.user_client = WebClient(token=self.user_token)
        
        if not self.bot_client and not self.user_client:
            raise ValueError("At least one of bot_token or user_token must be provided")
        
        # Use bot client as primary, fall back to user client
        self.client = self.bot_client or self.user_client
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test Slack API connection."""
        try:
            response = self.client.auth_test()
            self.user_id = response.get('user_id')
            self.team_id = response.get('team_id')
            self.team_name = response.get('team')
            print(f"Connected to Slack workspace: {self.team_name}")
        except SlackApiError as e:
            raise ConnectionError(f"Failed to connect to Slack: {e.response['error']}")
    
    def send_message(
        self,
        channel: str,
        text: str,
        thread_ts: Optional[str] = None,
        reply_broadcast: bool = False,
        blocks: Optional[List[Dict]] = None
    ) -> str:
        """Send a message to a channel or user."""
        try:
            # Resolve channel if it's a name
            channel_id = self._resolve_channel(channel)
            
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=text,
                thread_ts=thread_ts,
                reply_broadcast=reply_broadcast,
                blocks=blocks
            )
            
            return f"Message sent to {channel}: {text[:50]}..."
            
        except SlackApiError as e:
            return f"Error sending message: {e.response['error']}"
    
    def get_messages(
        self,
        channel: str,
        limit: int = 10,
        latest: Optional[str] = None,
        oldest: Optional[str] = None
    ) -> str:
        """Get messages from a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.conversations_history(
                channel=channel_id,
                limit=limit,
                latest=latest,
                oldest=oldest
            )
            
            messages = response['messages']
            result = f"Messages from {channel} (showing {len(messages)}):\n\n"
            
            for msg in messages:
                user = msg.get('user', 'Unknown')
                text = msg.get('text', '')
                timestamp = msg.get('ts', '')
                dt = datetime.fromtimestamp(float(timestamp))
                
                # Get user info for display name
                user_info = self._get_user_display_name(user)
                
                result += f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}] {user_info}: {text}\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error getting messages: {e.response['error']}"
    
    def list_channels(self, types: str = "public_channel,private_channel", exclude_archived: bool = True) -> str:
        """List channels in the workspace."""
        try:
            response = self.client.conversations_list(
                types=types,
                exclude_archived=exclude_archived
            )
            
            channels = response['channels']
            result = f"Channels ({len(channels)}):\n\n"
            
            for channel in channels:
                name = channel.get('name', 'Unknown')
                channel_id = channel.get('id', '')
                is_private = channel.get('is_private', False)
                member_count = channel.get('num_members', 0)
                purpose = channel.get('purpose', {}).get('value', '')
                
                privacy = "Private" if is_private else "Public"
                result += f"#{name} ({channel_id}) - {privacy}, {member_count} members\n"
                if purpose:
                    result += f"  Purpose: {purpose}\n"
                result += "\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error listing channels: {e.response['error']}"
    
    def create_channel(self, name: str, is_private: bool = False) -> str:
        """Create a new channel."""
        try:
            response = self.client.conversations_create(
                name=name,
                is_private=is_private
            )
            
            channel = response['channel']
            channel_id = channel['id']
            privacy = "private" if is_private else "public"
            
            return f"Created {privacy} channel #{name} ({channel_id})"
            
        except SlackApiError as e:
            return f"Error creating channel: {e.response['error']}"
    
    def join_channel(self, channel: str) -> str:
        """Join a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.conversations_join(channel=channel_id)
            
            return f"Joined channel {channel}"
            
        except SlackApiError as e:
            return f"Error joining channel: {e.response['error']}"
    
    def leave_channel(self, channel: str) -> str:
        """Leave a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.conversations_leave(channel=channel_id)
            
            return f"Left channel {channel}"
            
        except SlackApiError as e:
            return f"Error leaving channel: {e.response['error']}"
    
    def get_channel_info(self, channel: str) -> str:
        """Get information about a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.conversations_info(channel=channel_id)
            
            channel_info = response['channel']
            name = channel_info.get('name', 'Unknown')
            purpose = channel_info.get('purpose', {}).get('value', 'No purpose set')
            topic = channel_info.get('topic', {}).get('value', 'No topic set')
            member_count = channel_info.get('num_members', 0)
            created = channel_info.get('created', 0)
            is_private = channel_info.get('is_private', False)
            is_archived = channel_info.get('is_archived', False)
            
            created_date = datetime.fromtimestamp(created).strftime('%Y-%m-%d %H:%M:%S')
            privacy = "Private" if is_private else "Public"
            status = "Archived" if is_archived else "Active"
            
            result = f"Channel Information for #{name}:\n"
            result += f"ID: {channel_id}\n"
            result += f"Privacy: {privacy}\n"
            result += f"Status: {status}\n"
            result += f"Members: {member_count}\n"
            result += f"Created: {created_date}\n"
            result += f"Purpose: {purpose}\n"
            result += f"Topic: {topic}\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error getting channel info: {e.response['error']}"
    
    def list_users(self, limit: int = 100, presence: bool = False) -> str:
        """List users in the workspace."""
        try:
            response = self.client.users_list(limit=limit)
            
            users = response['members']
            result = f"Users ({len(users)}):\n\n"
            
            for user in users:
                if user.get('deleted') or user.get('is_bot'):
                    continue
                
                name = user.get('name', 'Unknown')
                real_name = user.get('real_name', '')
                user_id = user.get('id', '')
                title = user.get('profile', {}).get('title', '')
                email = user.get('profile', {}).get('email', '')
                
                result += f"@{name} ({user_id})\n"
                if real_name:
                    result += f"  Real name: {real_name}\n"
                if title:
                    result += f"  Title: {title}\n"
                if email:
                    result += f"  Email: {email}\n"
                result += "\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error listing users: {e.response['error']}"
    
    def get_user_info(self, user: str) -> str:
        """Get information about a user."""
        try:
            user_id = self._resolve_user(user)
            
            response = self.client.users_info(user=user_id)
            
            user_info = response['user']
            name = user_info.get('name', 'Unknown')
            real_name = user_info.get('real_name', '')
            display_name = user_info.get('profile', {}).get('display_name', '')
            title = user_info.get('profile', {}).get('title', '')
            email = user_info.get('profile', {}).get('email', '')
            phone = user_info.get('profile', {}).get('phone', '')
            timezone = user_info.get('tz', '')
            is_admin = user_info.get('is_admin', False)
            is_owner = user_info.get('is_owner', False)
            
            result = f"User Information for @{name}:\n"
            result += f"ID: {user_id}\n"
            if real_name:
                result += f"Real name: {real_name}\n"
            if display_name:
                result += f"Display name: {display_name}\n"
            if title:
                result += f"Title: {title}\n"
            if email:
                result += f"Email: {email}\n"
            if phone:
                result += f"Phone: {phone}\n"
            if timezone:
                result += f"Timezone: {timezone}\n"
            
            roles = []
            if is_owner:
                roles.append("Owner")
            if is_admin:
                roles.append("Admin")
            if roles:
                result += f"Roles: {', '.join(roles)}\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error getting user info: {e.response['error']}"
    
    def upload_file(
        self,
        file_path: str,
        channels: Optional[str] = None,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None
    ) -> str:
        """Upload a file to Slack."""
        try:
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            channel_ids = None
            if channels:
                channel_ids = [self._resolve_channel(ch.strip()) for ch in channels.split(',')]
            
            response = self.client.files_upload_v2(
                file=file_path,
                title=title,
                initial_comment=initial_comment,
                channel=channel_ids[0] if channel_ids else None
            )
            
            file_info = response['file']
            file_name = file_info.get('name', 'Unknown')
            file_url = file_info.get('url_private', '')
            
            return f"Uploaded file: {file_name} to {channels or 'workspace'}"
            
        except SlackApiError as e:
            return f"Error uploading file: {e.response['error']}"
        except Exception as e:
            return f"Error uploading file: {str(e)}"
    
    def download_file(self, file_url: str, save_path: Optional[str] = None) -> str:
        """Download a file from Slack."""
        try:
            headers = {'Authorization': f'Bearer {self.client.token}'}
            response = requests.get(file_url, headers=headers)
            
            if response.status_code == 200:
                if not save_path:
                    # Extract filename from URL
                    filename = file_url.split('/')[-1].split('?')[0]
                    save_path = f"downloads/{filename}"
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                return f"Downloaded file to: {save_path}"
            else:
                return f"Error downloading file: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error downloading file: {str(e)}"
    
    def search_messages(self, query: str, sort: str = "timestamp", sort_dir: str = "desc", count: int = 20) -> str:
        """Search for messages in Slack."""
        try:
            response = self.client.search_messages(
                query=query,
                sort=sort,
                sort_dir=sort_dir,
                count=count
            )
            
            matches = response['messages']['matches']
            total = response['messages']['total']
            
            result = f"Search results for '{query}' ({len(matches)} of {total}):\n\n"
            
            for match in matches:
                text = match.get('text', '')
                user = match.get('user', '')
                channel = match.get('channel', {})
                channel_name = channel.get('name', 'Unknown')
                timestamp = match.get('ts', '')
                
                if timestamp:
                    dt = datetime.fromtimestamp(float(timestamp))
                    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    date_str = 'Unknown time'
                
                user_name = self._get_user_display_name(user)
                
                result += f"[{date_str}] #{channel_name} - {user_name}:\n"
                result += f"  {text}\n\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error searching messages: {e.response['error']}"
    
    def set_status(self, status_text: str, status_emoji: Optional[str] = None, status_expiration: int = 0) -> str:
        """Set user status."""
        try:
            if not self.user_client:
                return "User token required for setting status"
            
            response = self.user_client.users_profile_set(
                profile={
                    'status_text': status_text,
                    'status_emoji': status_emoji or '',
                    'status_expiration': status_expiration
                }
            )
            
            return f"Status set to: {status_emoji or ''} {status_text}"
            
        except SlackApiError as e:
            return f"Error setting status: {e.response['error']}"
    
    def add_reaction(self, channel: str, timestamp: str, name: str) -> str:
        """Add reaction to a message."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.reactions_add(
                channel=channel_id,
                timestamp=timestamp,
                name=name
            )
            
            return f"Added reaction :{name}: to message"
            
        except SlackApiError as e:
            return f"Error adding reaction: {e.response['error']}"
    
    def pin_message(self, channel: str, timestamp: str) -> str:
        """Pin a message in a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.pins_add(
                channel=channel_id,
                timestamp=timestamp
            )
            
            return f"Pinned message in {channel}"
            
        except SlackApiError as e:
            return f"Error pinning message: {e.response['error']}"
    
    def unpin_message(self, channel: str, timestamp: str) -> str:
        """Unpin a message in a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.pins_remove(
                channel=channel_id,
                timestamp=timestamp
            )
            
            return f"Unpinned message in {channel}"
            
        except SlackApiError as e:
            return f"Error unpinning message: {e.response['error']}"
    
    def schedule_message(self, channel: str, text: str, post_at: int) -> str:
        """Schedule a message to be sent later."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.chat_scheduleMessage(
                channel=channel_id,
                text=text,
                post_at=post_at
            )
            
            scheduled_time = datetime.fromtimestamp(post_at)
            return f"Message scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
            
        except SlackApiError as e:
            return f"Error scheduling message: {e.response['error']}"
    
    def update_message(self, channel: str, timestamp: str, text: str) -> str:
        """Update an existing message."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.chat_update(
                channel=channel_id,
                ts=timestamp,
                text=text
            )
            
            return f"Updated message in {channel}"
            
        except SlackApiError as e:
            return f"Error updating message: {e.response['error']}"
    
    def delete_message(self, channel: str, timestamp: str) -> str:
        """Delete a message."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.chat_delete(
                channel=channel_id,
                ts=timestamp
            )
            
            return f"Deleted message in {channel}"
            
        except SlackApiError as e:
            return f"Error deleting message: {e.response['error']}"
    
    def create_reminder(self, text: str, time: str, user: Optional[str] = None) -> str:
        """Create a reminder."""
        try:
            response = self.client.reminders_add(
                text=text,
                time=time,
                user=user
            )
            
            return f"Reminder created: {text} at {time}"
            
        except SlackApiError as e:
            return f"Error creating reminder: {e.response['error']}"
    
    def get_workspace_info(self) -> str:
        """Get workspace information."""
        try:
            response = self.client.team_info()
            
            team = response['team']
            name = team.get('name', 'Unknown')
            domain = team.get('domain', 'Unknown')
            email_domain = team.get('email_domain', 'Unknown')
            enterprise_name = team.get('enterprise_name', '')
            
            result = f"Workspace Information:\n"
            result += f"Name: {name}\n"
            result += f"Domain: {domain}\n"
            result += f"Email Domain: {email_domain}\n"
            if enterprise_name:
                result += f"Enterprise: {enterprise_name}\n"
            
            return result
            
        except SlackApiError as e:
            return f"Error getting workspace info: {e.response['error']}"
    
    def send_direct_message(self, user: str, text: str) -> str:
        """Send a direct message to a user."""
        try:
            user_id = self._resolve_user(user)
            
            # Open DM channel
            response = self.client.conversations_open(users=[user_id])
            channel_id = response['channel']['id']
            
            # Send message
            return self.send_message(channel_id, text)
            
        except SlackApiError as e:
            return f"Error sending DM: {e.response['error']}"
    
    def invite_user_to_channel(self, channel: str, user: str) -> str:
        """Invite a user to a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            user_id = self._resolve_user(user)
            
            response = self.client.conversations_invite(
                channel=channel_id,
                users=[user_id]
            )
            
            return f"Invited {user} to {channel}"
            
        except SlackApiError as e:
            return f"Error inviting user: {e.response['error']}"
    
    def remove_user_from_channel(self, channel: str, user: str) -> str:
        """Remove a user from a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            user_id = self._resolve_user(user)
            
            response = self.client.conversations_kick(
                channel=channel_id,
                user=user_id
            )
            
            return f"Removed {user} from {channel}"
            
        except SlackApiError as e:
            return f"Error removing user: {e.response['error']}"
    
    def archive_channel(self, channel: str) -> str:
        """Archive a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.conversations_archive(channel=channel_id)
            
            return f"Archived channel {channel}"
            
        except SlackApiError as e:
            return f"Error archiving channel: {e.response['error']}"
    
    def unarchive_channel(self, channel: str) -> str:
        """Unarchive a channel."""
        try:
            channel_id = self._resolve_channel(channel)
            
            response = self.client.conversations_unarchive(channel=channel_id)
            
            return f"Unarchived channel {channel}"
            
        except SlackApiError as e:
            return f"Error unarchiving channel: {e.response['error']}"
    
    def _resolve_channel(self, channel: str) -> str:
        """Resolve channel name to ID."""
        if channel.startswith('C') or channel.startswith('D') or channel.startswith('G'):
            return channel
        
        # Remove # if present
        channel = channel.lstrip('#')
        
        try:
            response = self.client.conversations_list(types="public_channel,private_channel")
            for ch in response['channels']:
                if ch['name'] == channel:
                    return ch['id']
            
            # If not found, try as-is (might be a valid ID)
            return channel
            
        except SlackApiError:
            return channel
    
    def _resolve_user(self, user: str) -> str:
        """Resolve username to user ID."""
        if user.startswith('U'):
            return user
        
        # Remove @ if present
        user = user.lstrip('@')
        
        try:
            response = self.client.users_list()
            for u in response['members']:
                if u['name'] == user or u.get('real_name') == user:
                    return u['id']
            
            # If not found, try as-is
            return user
            
        except SlackApiError:
            return user
    
    def _get_user_display_name(self, user_id: str) -> str:
        """Get display name for a user ID."""
        try:
            response = self.client.users_info(user=user_id)
            user_info = response['user']
            return user_info.get('display_name') or user_info.get('real_name') or user_info.get('name', user_id)
        except SlackApiError:
            return user_id