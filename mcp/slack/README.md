# Slack MCP Server

A Model Context Protocol (MCP) server for Slack workspace automation and messaging. This server provides comprehensive Slack integration capabilities, enabling automated messaging, channel management, file sharing, and workflow automation for SDLC teams.

## Features

- 💬 **Complete Messaging** - Send, update, delete, and schedule messages
- 🏢 **Channel Management** - Create, join, archive, and manage channels
- 👥 **User Management** - List users, manage channel membership, and direct messaging
- 📁 **File Operations** - Upload and download files with full metadata
- 🔍 **Search & Discovery** - Search messages, channels, and users
- 📌 **Message Actions** - Pin, react, and thread conversations
- ⏰ **Scheduling & Reminders** - Schedule messages and create reminders
- 🎯 **Status Management** - Set user status and presence
- 🔗 **Workspace Integration** - Full workspace information and administration

## Prerequisites

- **Python** >= 3.10
- **Slack Workspace** with appropriate permissions
- **Slack App** with required OAuth scopes
- **uv** package manager (recommended)

### Required Slack Scopes

For Bot Token (xoxb-):
- `chat:write` - Send messages
- `channels:read` - Read public channel information
- `groups:read` - Read private channel information
- `im:read` - Read direct message information
- `mpim:read` - Read group message information
- `users:read` - Read user information
- `files:write` - Upload files
- `files:read` - Read file information

For User Token (xoxp-) - Optional for enhanced features:
- `users.profile:write` - Set user status
- `search:read` - Search messages

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: using pip
pip install uv
```

### 2. Set up the project

```bash
# Navigate to the Slack MCP directory
cd mcp/slack

# Install dependencies
uv sync

# Activate virtual environment (optional)
source .venv/bin/activate
```

### 3. Slack App Setup

#### Create a Slack App:

1. Go to [Slack API Applications](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Enter app name and select workspace
4. Configure OAuth & Permissions:
   - Add required scopes (see Prerequisites)
   - Install app to workspace
   - Copy Bot User OAuth Token (xoxb-...)

#### Optional User Token:
1. In OAuth & Permissions, add User Token Scopes
2. Copy User OAuth Token (xoxp-...)

## Configuration

### Environment Variables

Create a `.env` file:

```env
# Required: Slack Bot Token
SLACK_BOT_TOKEN=xoxb-your-bot-token-here

# Optional: Enhanced features
SLACK_USER_TOKEN=xoxp-your-user-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Workspace settings
SLACK_WORKSPACE=your-workspace-name
DEFAULT_CHANNEL=general
```

### Command Line Options

```bash
# Using environment variables
uv run main.py

# Using command line arguments
uv run main.py --bot-token xoxb-... --workspace myteam --default-channel dev
```

## Usage

### Running the Server

#### Basic Usage:
```bash
uv run main.py
```

#### With Custom Configuration:
```bash
uv run main.py --bot-token xoxb-... --user-token xoxp-... --workspace myteam
```

## MCP Server Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "slack-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/agent/mcp/slack && source .venv/bin/activate && uv run main.py"
      ],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here",
        "SLACK_WORKSPACE": "your-workspace"
      },
      "alwaysAllow": [
        "Send-Message-Tool",
        "Get-Messages-Tool",
        "Channel-List-Tool",
        "User-List-Tool"
      ]
    }
  }
}
```

**Note**: Update the path and tokens according to your setup.

## Available Tools

### Messaging Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **Send-Message-Tool** | Send message to channel/user | `channel: str, text: str, thread_ts: str = None` |
| **Get-Messages-Tool** | Get recent messages | `channel: str, limit: int = 10, latest: str = None` |
| **Update-Message-Tool** | Update existing message | `channel: str, timestamp: str, text: str` |
| **Delete-Message-Tool** | Delete message | `channel: str, timestamp: str` |
| **Schedule-Message-Tool** | Schedule future message | `channel: str, text: str, post_at: int` |
| **Send-DM-Tool** | Send direct message | `user: str, text: str` |

### Channel Management

| Tool | Description | Parameters |
|------|-------------|------------|
| **Channel-List-Tool** | List workspace channels | `types: str = "public_channel,private_channel"` |
| **Channel-Create-Tool** | Create new channel | `name: str, is_private: bool = False` |
| **Channel-Join-Tool** | Join channel | `channel: str` |
| **Channel-Leave-Tool** | Leave channel | `channel: str` |
| **Channel-Info-Tool** | Get channel information | `channel: str` |
| **Archive-Channel-Tool** | Archive channel | `channel: str` |
| **Unarchive-Channel-Tool** | Unarchive channel | `channel: str` |

### User Management

| Tool | Description | Parameters |
|------|-------------|------------|
| **User-List-Tool** | List workspace users | `limit: int = 100, presence: bool = False` |
| **User-Info-Tool** | Get user information | `user: str` |
| **Invite-User-Tool** | Invite user to channel | `channel: str, user: str` |
| **Remove-User-Tool** | Remove user from channel | `channel: str, user: str` |
| **Set-Status-Tool** | Set user status | `status_text: str, status_emoji: str = None` |

### File Operations

| Tool | Description | Parameters |
|------|-------------|------------|
| **Upload-File-Tool** | Upload file to Slack | `file_path: str, channels: str = None, title: str = None` |
| **Download-File-Tool** | Download Slack file | `file_url: str, save_path: str = None` |

### Advanced Features

| Tool | Description | Parameters |
|------|-------------|------------|
| **Search-Messages-Tool** | Search workspace messages | `query: str, sort: str = "timestamp", count: int = 20` |
| **React-Tool** | Add emoji reaction | `channel: str, timestamp: str, name: str` |
| **Pin-Message-Tool** | Pin message in channel | `channel: str, timestamp: str` |
| **Unpin-Message-Tool** | Unpin message | `channel: str, timestamp: str` |
| **Create-Reminder-Tool** | Create reminder | `text: str, time: str, user: str = None` |
| **Workspace-Info-Tool** | Get workspace info | None |

## Usage Examples

### Basic Messaging

```bash
# Send a message to a channel
Send-Message-Tool --channel "#general" --text "Hello team! 👋"

# Send a direct message
Send-DM-Tool --user "@john.doe" --text "Hey John, can we chat about the project?"

# Get recent messages from a channel
Get-Messages-Tool --channel "#dev" --limit 5
```

### Channel Management

```bash
# List all channels
Channel-List-Tool --types "public_channel,private_channel"

# Create a new project channel
Channel-Create-Tool --name "project-alpha" --is_private false

# Get channel information
Channel-Info-Tool --channel "#project-alpha"

# Join a channel
Channel-Join-Tool --channel "#project-alpha"
```

### Team Collaboration

```bash
# List team members
User-List-Tool --limit 50

# Invite user to project channel
Invite-User-Tool --channel "#project-alpha" --user "@jane.smith"

# Set your status
Set-Status-Tool --status_text "In a meeting" --status_emoji ":calendar:"
```

### File Sharing

```bash
# Upload a document
Upload-File-Tool --file_path "/path/to/document.pdf" --channels "#project-alpha" --title "Project Requirements"

# Upload with comment
Upload-File-Tool --file_path "/path/to/screenshot.png" --channels "#dev" --initial_comment "Here's the bug I found"
```

### Advanced Workflows

```bash
# Schedule a daily standup reminder
Schedule-Message-Tool --channel "#dev" --text "Daily standup in 15 minutes! 🏃‍♀️" --post_at 1609459200

# Search for specific discussions
Search-Messages-Tool --query "deployment pipeline" --count 10

# Pin important announcements
Pin-Message-Tool --channel "#general" --timestamp "1609459200.123456"

# Add reaction to show approval
React-Tool --channel "#dev" --timestamp "1609459200.123456" --name "thumbsup"
```

### SDLC Integration Examples

#### Meeting Notifications
```bash
# Notify team about standup
Send-Message-Tool --channel "#dev" --text "📅 Daily standup starting now! Join us in the main room."

# Share meeting summary
Upload-File-Tool --file_path "meeting_summary.md" --channels "#dev" --title "Sprint Planning Summary"
```

#### Deployment Announcements
```bash
# Deployment notification
Send-Message-Tool --channel "#releases" --text "🚀 Deploying v2.1.0 to production. ETA: 15 minutes"

# Post-deployment update
Send-Message-Tool --channel "#releases" --text "✅ Deployment successful! All systems operational."
```

#### Bug Reports
```bash
# Create bug report channel
Channel-Create-Tool --name "bug-urgent-auth" --is_private false

# Invite relevant team members
Invite-User-Tool --channel "#bug-urgent-auth" --user "@dev.lead"
Invite-User-Tool --channel "#bug-urgent-auth" --user "@qa.engineer"

# Upload bug details
Upload-File-Tool --file_path "bug_report.pdf" --channels "#bug-urgent-auth"
```

## Configuration Options

### Advanced Settings

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_USER_TOKEN=xoxp-your-user-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_WORKSPACE=your-workspace

# Default Settings
DEFAULT_CHANNEL=general
DEFAULT_MESSAGE_LIMIT=20
DEFAULT_SEARCH_COUNT=20

# File Upload Settings
MAX_FILE_SIZE_MB=100
UPLOAD_DIRECTORY=/tmp/slack_uploads
DOWNLOAD_DIRECTORY=/tmp/slack_downloads

# Feature Flags
ENABLE_FILE_OPERATIONS=true
ENABLE_ADMIN_FUNCTIONS=false
ENABLE_MESSAGE_DELETION=true
```

### Channel Types

When using `Channel-List-Tool`, you can filter by:
- `public_channel` - Public channels
- `private_channel` - Private channels
- `mpim` - Group direct messages
- `im` - Direct messages

### Message Formatting

Slack supports rich formatting:
```bash
# Bold and italics
Send-Message-Tool --channel "#dev" --text "*Bold text* and _italic text_"

# Code blocks
Send-Message-Tool --channel "#dev" --text "Here's the fix: \`\`\`python\nprint('Hello World')\n\`\`\`"

# Mentions and channels
Send-Message-Tool --channel "#dev" --text "Hey <@U123456> check out <#C789012>"
```

## Troubleshooting

### Common Issues

1. **Token Permission Errors**:
   ```bash
   # Verify token permissions
   Workspace-Info-Tool
   
   # Check if bot is in channel
   Channel-Join-Tool --channel "#your-channel"
   ```

2. **Channel Not Found**:
   ```bash
   # List all channels to find correct name
   Channel-List-Tool
   
   # Use channel ID instead of name
   Send-Message-Tool --channel "C1234567890" --text "Hello"
   ```

3. **File Upload Issues**:
   ```bash
   # Check file exists and permissions
   ls -la /path/to/file
   
   # Try uploading to workspace first
   Upload-File-Tool --file_path "/path/to/file"
   ```

4. **User Not Found**:
   ```bash
   # List users to find correct username
   User-List-Tool --limit 100
   
   # Use user ID instead
   Send-DM-Tool --user "U1234567890" --text "Hello"
   ```

### API Rate Limits

Slack enforces rate limits:
- **Tier 1**: 1+ requests per minute
- **Tier 2**: 20+ requests per minute  
- **Tier 3**: 50+ requests per minute
- **Tier 4**: 100+ requests per minute

The server automatically handles rate limiting with exponential backoff.

### Debug Mode

Enable debug logging:
```bash
SLACK_DEBUG=true uv run main.py
```

## Development

### Project Structure

```
mcp/slack/
├── README.md
├── pyproject.toml
├── main.py                 # MCP server entry point
├── src/
│   └── slack/
│       └── __init__.py     # Main SlackClient class
└── .venv/                  # Virtual environment
```

### Dependencies

- **mcp**: Model Context Protocol framework
- **slack-sdk**: Official Slack SDK for Python
- **requests**: HTTP requests for file downloads
- **python-dotenv**: Environment variable management
- **aiohttp**: Async HTTP client support

### Testing Your Changes

```bash
# Basic connection test
uv run python -c "
from src.slack import SlackClient
import os
client = SlackClient(bot_token=os.getenv('SLACK_BOT_TOKEN'))
print('Connection successful!')
print(client.get_workspace_info())
"

# Test MCP tools
uv run main.py
```

## Integration with SDLC Workflow

This Slack MCP server perfectly complements your existing SDLC automation platform:

1. **Meeting Transcription** → Share summaries in Slack channels
2. **PRD/TRD Generation** → Distribute documents via Slack  
3. **Figma MCP** → Share design updates in design channels
4. **Development MCPs** → Coordinate testing across Android/iOS/Chrome
5. **Slack MCP** → **🆕 Team communication and workflow coordination**
6. **Firebase Crashlytics MCP** → Alert teams about critical issues
7. **Docker/GCP MCP** → Notify deployment status

## Security Considerations

- **Token Security**: Store tokens in environment variables, never in code
- **Permission Scoping**: Use minimal required OAuth scopes
- **Channel Privacy**: Respect private channel access controls
- **User Privacy**: Handle user data according to privacy policies
- **File Security**: Validate file uploads and downloads

## Advanced Use Cases

### Automated Standup Bot

```bash
# Schedule daily standup reminders
Schedule-Message-Tool --channel "#dev" --text "🏃‍♀️ Daily standup in 10 minutes!" --post_at 1609459200

# Create standup thread
Send-Message-Tool --channel "#dev" --text "📝 Daily Standup Thread - Please share your updates below"
```

### Release Management

```bash
# Create release channel
Channel-Create-Tool --name "release-v2-1-0" --is_private false

# Invite stakeholders
Invite-User-Tool --channel "#release-v2-1-0" --user "@product.manager"
Invite-User-Tool --channel "#release-v2-1-0" --user "@qa.lead"

# Upload release notes
Upload-File-Tool --file_path "release_notes_v2.1.0.md" --channels "#release-v2-1-0"
```

### Incident Management

```bash
# Create incident channel
Channel-Create-Tool --name "incident-auth-down" --is_private false

# Alert team
Send-Message-Tool --channel "#incident-auth-down" --text "🚨 AUTH SERVICE DOWN - All hands on deck!"

# Pin incident details
Pin-Message-Tool --channel "#incident-auth-down" --timestamp "1609459200.123456"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Add appropriate documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Slack SDK for Python](https://github.com/slackapi/python-slack-sdk)
- Inspired by the need for seamless team communication in SDLC workflows
- Designed for integration with comprehensive development automation platforms

---

**Repository:** [https://github.com/tomdwipo/agent](https://github.com/tomdwipo/agent)