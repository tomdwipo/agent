#!/bin/bash

# Slack MCP Server Setup Script
# Automates the installation and configuration of the Slack MCP server

set -e

echo "💬 Slack MCP Server Setup"
echo "========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check for required tools
print_step "Checking prerequisites..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
print_success "Python $python_version found ✓"

# Check for uv
if ! command -v uv &> /dev/null; then
    print_warning "uv package manager not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    
    if command -v uv &> /dev/null; then
        print_success "uv installed successfully ✓"
    else
        print_error "Failed to install uv"
        exit 1
    fi
else
    print_success "uv package manager found ✓"
fi

# Install Python dependencies
print_step "Installing Python dependencies..."
uv sync

if [ $? -eq 0 ]; then
    print_success "Dependencies installed ✓"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Test Slack SDK import
print_step "Testing Slack SDK..."

if uv run python -c "import slack_sdk; print('Slack SDK version:', slack_sdk.__version__)" 2>/dev/null; then
    print_success "Slack SDK imported successfully ✓"
else
    print_error "Failed to import Slack SDK"
    exit 1
fi

# Test MCP server import
print_step "Testing Slack MCP server modules..."

if uv run python -c "from src.slack import SlackClient; print('Import successful')" 2>/dev/null; then
    print_success "Slack MCP server modules loaded successfully ✓"
else
    print_error "Failed to load Slack MCP server modules"
    exit 1
fi

# Check for existing .env file
if [ -f ".env" ]; then
    print_warning ".env file already exists"
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_step "Keeping existing .env file"
    else
        create_env=true
    fi
else
    create_env=true
fi

# Create example environment file
if [ "$create_env" = true ]; then
    print_step "Creating example .env file..."
    cat > .env << EOF
# Slack MCP Server Configuration

# Required: Slack Bot Token (get from https://api.slack.com/apps)
SLACK_BOT_TOKEN=xoxb-your-bot-token-here

# Optional: Enhanced features
SLACK_USER_TOKEN=xoxp-your-user-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Workspace settings
SLACK_WORKSPACE=your-workspace-name
DEFAULT_CHANNEL=general

# Feature settings
DEFAULT_MESSAGE_LIMIT=20
DEFAULT_SEARCH_COUNT=20
MAX_FILE_SIZE_MB=100

# File operation settings
UPLOAD_DIRECTORY=/tmp/slack_uploads
DOWNLOAD_DIRECTORY=/tmp/slack_downloads

# Feature flags
ENABLE_FILE_OPERATIONS=true
ENABLE_ADMIN_FUNCTIONS=false
ENABLE_MESSAGE_DELETION=true

# Debug settings
SLACK_DEBUG=false
EOF
    print_success "Created .env configuration file ✓"
fi

# Slack App setup instructions
print_step "Slack App Setup Instructions"
echo
echo "To use this MCP server, you need to create a Slack app:"
echo
echo "1. Go to https://api.slack.com/apps"
echo "2. Click 'Create New App' → 'From scratch'"
echo "3. Enter app name and select your workspace"
echo "4. Go to 'OAuth & Permissions' and add these Bot Token Scopes:"
echo "   ${YELLOW}Required scopes:${NC}"
echo "   • chat:write         (Send messages)"
echo "   • channels:read      (Read public channels)"
echo "   • groups:read        (Read private channels)"
echo "   • im:read           (Read DMs)"
echo "   • mpim:read         (Read group DMs)"
echo "   • users:read        (Read user info)"
echo "   • files:write       (Upload files)"
echo "   • files:read        (Read files)"
echo
echo "   ${YELLOW}Optional scopes for enhanced features:${NC}"
echo "   • users.profile:write (Set status)"
echo "   • search:read        (Search messages)"
echo "   • pins:write         (Pin messages)"
echo "   • reactions:write    (Add reactions)"
echo "   • reminders:write    (Create reminders)"
echo
echo "5. Install the app to your workspace"
echo "6. Copy the 'Bot User OAuth Token' (starts with xoxb-)"
echo "7. Update the SLACK_BOT_TOKEN in your .env file"
echo

# Test connection if token is provided
if [ -f ".env" ]; then
    source .env
    if [ ! -z "$SLACK_BOT_TOKEN" ] && [ "$SLACK_BOT_TOKEN" != "xoxb-your-bot-token-here" ]; then
        print_step "Testing Slack connection..."
        
        if uv run python -c "
import os
from src.slack import SlackClient
try:
    client = SlackClient(bot_token=os.getenv('SLACK_BOT_TOKEN'))
    info = client.get_workspace_info()
    print('✓ Connection successful!')
    print(info)
except Exception as e:
    print(f'✗ Connection failed: {e}')
" 2>/dev/null; then
            print_success "Slack connection test passed ✓"
        else
            print_warning "Slack connection test failed (check your token)"
        fi
    else
        print_warning "No valid Slack token found in .env file"
    fi
fi

# Create downloads directory
print_step "Creating download directories..."
mkdir -p downloads
mkdir -p uploads
print_success "Created download/upload directories ✓"

# Final instructions
echo
echo "🎉 Slack MCP Server Setup Complete!"
echo "==================================="
echo
echo "Next steps:"
echo "1. Set up your Slack app (see instructions above)"
echo "2. Update SLACK_BOT_TOKEN in .env file"
echo "3. Test the server:"
echo "   ${BLUE}uv run main.py${NC}"
echo
echo "4. Test with specific tokens:"
echo "   ${BLUE}uv run main.py --bot-token xoxb-... --workspace myteam${NC}"
echo
echo "5. For MCP client integration, add this to your configuration:"
echo "${YELLOW}"
cat << 'EOF'
{
  "mcpServers": {
    "slack-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c", 
        "cd /path/to/agent/mcp/slack && uv run main.py"
      ],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here"
      }
    }
  }
}
EOF
echo "${NC}"
echo
echo "📖 For detailed usage instructions, see README.md"
echo "🐛 For troubleshooting, check the Common Issues section in README.md"

# Performance and security tips
echo
echo "💡 Tips:"
echo "• Use bot tokens for most operations (more secure)"
echo "• Add user tokens only if you need status/search features"
echo "• Start with minimal OAuth scopes and add more as needed"
echo "• Test with a development workspace first"
echo "• Keep tokens secure and never commit them to version control"

# Offer to run a quick demo
echo
read -p "Would you like to run a quick connection test? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -z "$SLACK_BOT_TOKEN" ] && [ "$SLACK_BOT_TOKEN" != "xoxb-your-bot-token-here" ]; then
        print_step "Running connection test..."
        
        if uv run python -c "
import os
from src.slack import SlackClient

token = os.getenv('SLACK_BOT_TOKEN')
if not token or token == 'xoxb-your-bot-token-here':
    print('❌ Please set a valid SLACK_BOT_TOKEN in .env file')
    exit(1)

try:
    client = SlackClient(bot_token=token)
    
    # Test workspace info
    print('Testing workspace connection...')
    workspace_info = client.get_workspace_info()
    print('✅ Workspace connection successful!')
    
    # Test channel listing
    print('Testing channel listing...')
    channels = client.list_channels()
    print('✅ Channel listing successful!')
    
    print('🎉 All tests passed! Slack MCP server is ready to use.')
    
except Exception as e:
    print(f'❌ Connection test failed: {e}')
    print('💡 Please check your SLACK_BOT_TOKEN and app permissions')
" 2>/dev/null; then
            print_success "Connection test completed successfully!"
        else
            print_warning "Connection test failed - check your configuration"
        fi
    else
        print_warning "Please set SLACK_BOT_TOKEN in .env file first"
        echo "Then run: ${BLUE}uv run python -c \"from src.slack import SlackClient; SlackClient()\"${NC}"
    fi
fi

print_success "Setup completed successfully! 🚀"