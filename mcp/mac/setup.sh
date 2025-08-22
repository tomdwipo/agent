#!/bin/bash

# Mac MCP Server Setup Script
# Installs dependencies and configures the Mac MCP server for automation

set -e

echo "🍎 Setting up Mac MCP Server..."

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ Error: Mac MCP server can only be installed on macOS"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ Error: Python 3.10+ required. Found: $python_version"
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

echo "✅ uv package manager ready"

# Install dependencies
echo "📦 Installing Mac MCP dependencies..."
uv pip install -r <(grep -E "^[^#]" <<EOF
mcp>=1.9.3
pillow>=10.0.0
pyobjc-core>=10.0
pyobjc-framework-Cocoa>=10.0
pyobjc-framework-Quartz>=10.0
pyobjc-framework-ApplicationServices>=10.0
pyobjc-framework-CoreGraphics>=10.0
psutil>=5.9.0
typing-extensions>=4.8.0
asyncio>=3.4.3
python-dateutil>=2.8.0
EOF
)

echo "✅ Dependencies installed successfully"

# Check accessibility permissions
echo "🔐 Checking accessibility permissions..."

# Test if System Events is accessible
accessibility_test=$(osascript -e 'tell application "System Events" to get exists of process "Finder"' 2>&1 || echo "false")

if [[ "$accessibility_test" == "false" ]]; then
    echo "⚠️  Accessibility permissions not granted."
    echo "📋 To enable full automation features:"
    echo "   1. Open System Preferences/Settings"
    echo "   2. Go to Security & Privacy > Privacy > Accessibility"
    echo "   3. Add Terminal (or your terminal app) to the list"
    echo "   4. Add Python to the list if prompted"
    echo "   5. Restart this script"
    echo ""
    echo "🔄 You can still use the Mac MCP server with limited functionality"
else
    echo "✅ Accessibility permissions verified"
fi

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    echo "📄 Creating .env configuration file..."
    cp .env.example .env
    echo "✅ .env file created from template"
    echo "📝 Please edit .env file to configure your preferences"
else
    echo "✅ .env file already exists"
fi

# Make main.py executable
chmod +x main.py

echo ""
echo "🎉 Mac MCP Server setup completed!"
echo ""
echo "📚 Next steps:"
echo "   1. Edit .env file to configure settings"
echo "   2. Run the server: python3 main.py"
echo "   3. For accessibility features: python3 main.py --enable-accessibility"
echo ""
echo "🔧 Usage examples:"
echo "   # Basic mode"
echo "   python3 main.py"
echo ""
echo "   # With accessibility features"
echo "   python3 main.py --enable-accessibility"
echo ""
echo "   # Safe mode (restricted operations)"
echo "   python3 main.py --safe-mode"
echo ""
echo "   # Custom device name"
echo "   python3 main.py --device-name 'My MacBook Pro'"
echo ""
echo "📖 See README.md for complete documentation"