#!/bin/bash

# iOS MCP Server Setup Script
# Automates the installation and configuration of the iOS MCP server

set -e

echo "🍎 iOS MCP Server Setup"
echo "======================="

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

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "iOS MCP server requires macOS. Current OS: $OSTYPE"
    exit 1
fi

print_success "Running on macOS ✓"

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

# Check for Xcode
if ! command -v xcodebuild &> /dev/null; then
    print_warning "Xcode is required for iOS automation"
    print_warning "Please install Xcode from the App Store"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "Xcode found ✓"
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

# Check for iOS devices/simulators
print_step "Checking for iOS devices and simulators..."

# Check for simulators
if command -v xcrun &> /dev/null; then
    simulators=$(xcrun simctl list devices | grep "iPhone" | grep "Booted\|Shutdown" | wc -l)
    if [ $simulators -gt 0 ]; then
        print_success "Found $simulators iOS simulators ✓"
    else
        print_warning "No iOS simulators found"
    fi
fi

# Check for physical devices
if command -v idevice_id &> /dev/null; then
    devices=$(idevice_id -l | wc -l)
    if [ $devices -gt 0 ]; then
        print_success "Found $devices connected iOS devices ✓"
    else
        print_warning "No physical iOS devices found"
    fi
else
    print_warning "libimobiledevice not installed (optional for physical devices)"
    print_warning "Install with: brew install libimobiledevice"
fi

# Setup WebDriverAgent (optional)
print_step "WebDriverAgent setup..."

read -p "Do you want to set up WebDriverAgent automatically? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Setting up WebDriverAgent via Appium..."
    
    # Check for Node.js
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is required for Appium"
        print_warning "Install Node.js from https://nodejs.org"
        read -p "Continue without Appium setup? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        # Install Appium
        if ! command -v appium &> /dev/null; then
            print_step "Installing Appium..."
            npm install -g appium
            npm install -g @appium/doctor
        fi
        
        # Install XCUITest driver
        print_step "Installing XCUITest driver..."
        appium driver install xcuitest
        
        # Run Appium doctor
        print_step "Running Appium doctor check..."
        appium doctor --ios
        
        print_success "Appium setup completed ✓"
    fi
else
    print_warning "Skipping WebDriverAgent automatic setup"
    echo "Please follow manual setup instructions in README.md"
fi

# Test installation
print_step "Testing iOS MCP server..."

# Test basic import
if uv run python -c "from src.ios import IOSDevice; print('Import successful')" 2>/dev/null; then
    print_success "iOS MCP server modules loaded successfully ✓"
else
    print_error "Failed to load iOS MCP server modules"
    exit 1
fi

# Create example environment file
if [ ! -f ".env" ]; then
    print_step "Creating example .env file..."
    cat > .env << EOF
# iOS MCP Server Configuration

# Device connection settings
DEFAULT_DEVICE_TYPE=simulator
DEFAULT_PORT=8100
CONNECTION_TIMEOUT=30

# WebDriverAgent settings
WDA_BUNDLE_ID=com.facebook.WebDriverAgentRunner.xctrunner

# Debug settings
DEBUG_MODE=false
VERBOSE_LOGGING=false

# Element detection settings
ELEMENT_WAIT_TIMEOUT=10.0
SCREENSHOT_SCALE=0.7
EOF
    print_success "Created .env configuration file ✓"
fi

# Final instructions
echo
echo "🎉 iOS MCP Server Setup Complete!"
echo "================================="
echo
echo "Next steps:"
echo "1. Start an iOS Simulator or connect a physical device"
echo "2. Launch WebDriverAgent (see README.md for instructions)"
echo "3. Test the server:"
echo "   ${BLUE}uv run main.py --simulator${NC}"
echo
echo "For MCP client integration, add this to your configuration:"
echo "${YELLOW}"
cat << 'EOF'
{
  "mcpServers": {
    "ios-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c", 
        "cd /path/to/agent/mcp/ios && uv run main.py --simulator"
      ]
    }
  }
}
EOF
echo "${NC}"
echo
echo "📖 For detailed setup and usage instructions, see README.md"
echo "🐛 For troubleshooting, check the Common Issues section in README.md"

print_success "Setup completed successfully! 🚀"