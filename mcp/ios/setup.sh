#!/bin/bash
# iOS MCP Setup and Verification Script
# This script helps validate and setup WebDriverAgent for iOS automation

set -e  # Exit on any error

echo "🚀 iOS MCP Setup and Verification Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script requires macOS for iOS device automation"
    exit 1
fi

print_status "Running on macOS"

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    print_error "Xcode is not installed or command line tools are missing"
    print_info "Please install Xcode from the App Store and run:"
    print_info "xcode-select --install"
    exit 1
fi

print_status "Xcode is installed"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_status "Python $PYTHON_VERSION is available"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_warning "uv package manager not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    
    if ! command -v uv &> /dev/null; then
        print_error "Failed to install uv. Please install manually:"
        print_info "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

print_status "uv package manager is available"

# Install project dependencies
print_info "Installing project dependencies..."
uv sync

print_status "Dependencies installed"

# Check for iOS devices
print_info "Checking for connected iOS devices..."

# Check for physical devices
if command -v idevice_id &> /dev/null; then
    DEVICES=$(idevice_id -l)
    if [ -n "$DEVICES" ]; then
        print_status "Physical iOS devices found:"
        echo "$DEVICES" | while read -r device; do
            echo "  📱 $device"
        done
    else
        print_warning "No physical iOS devices found"
    fi
else
    # Try with tidevice
    if pip3 show tidevice &> /dev/null || uv run python -c "import tidevice" &> /dev/null; then
        DEVICES=$(uv run python -c "import tidevice; print('\n'.join(tidevice.Device.list()))" 2>/dev/null || echo "")
        if [ -n "$DEVICES" ]; then
            print_status "Physical iOS devices found (via tidevice):"
            echo "$DEVICES" | while read -r device; do
                echo "  📱 $device"
            done
        else
            print_warning "No physical iOS devices found"
        fi
    else
        print_warning "Neither libimobiledevice nor tidevice found for device detection"
    fi
fi

# Check for iOS Simulators
print_info "Checking for iOS Simulators..."
SIMULATORS=$(xcrun simctl list devices | grep -E "iPhone|iPad" | grep "Booted" || echo "")
if [ -n "$SIMULATORS" ]; then
    print_status "Running iOS Simulators found:"
    echo "$SIMULATORS" | while read -r sim; do
        echo "  📲 $sim"
    done
else
    print_warning "No running iOS Simulators found"
    print_info "You can start a simulator with:"
    print_info "open -a Simulator"
fi

# Check if tidevice is installed
print_info "Checking tidevice installation..."
if uv run python -c "import tidevice" &> /dev/null; then
    print_status "tidevice is installed"
else
    print_warning "tidevice not found. Installing..."
    uv add tidevice
    print_status "tidevice installed"
fi

# Function to check WebDriverAgent
check_wda() {
    local port=${1:-8100}
    local timeout=3
    
    print_info "Checking WebDriverAgent on port $port..."
    
    if curl -s --connect-timeout $timeout "http://localhost:$port/status" > /dev/null 2>&1; then
        print_status "WebDriverAgent is running on port $port"
        return 0
    else
        return 1
    fi
}

# Check if WebDriverAgent is running
if ! check_wda 8100; then
    print_warning "WebDriverAgent is not running on default port 8100"
    
    # Check common alternative ports
    for port in 4723 8200 9100; do
        if check_wda $port; then
            print_info "Found WebDriverAgent on port $port"
            break
        fi
    done
    
    print_info "To start WebDriverAgent:"
    echo ""
    echo "For physical devices:"
    echo "  uv run python -c \"import tidevice; tidevice.Device().wdaproxy()\""
    echo ""
    echo "For simulators:"
    echo "  1. Install Appium: npm install -g appium"
    echo "  2. Install driver: appium driver install xcuitest"
    echo "  3. Start server: appium --port 4723"
    echo ""
    echo "Alternative manual setup:"
    echo "  1. git clone https://github.com/appium/WebDriverAgent.git"
    echo "  2. cd WebDriverAgent"
    echo "  3. Open WebDriverAgent.xcodeproj in Xcode"
    echo "  4. Set development team in project settings"
    echo "  5. Build and run WebDriverAgentRunner target"
fi

# Test iOS MCP connection
print_info "Testing iOS MCP connection..."

# Try to initialize the iOS device
TEST_OUTPUT=$(uv run python -c "
try:
    import sys
    sys.path.append('src')
    from ios import IOSDevice
    
    # Try different connection methods
    methods = [
        ('simulator', {'simulator': True}),
        ('usb', {'usb': True}),
        ('localhost', {}),
    ]
    
    for method_name, kwargs in methods:
        try:
            print(f'Trying {method_name} connection...')
            device = IOSDevice(auto_setup=False, **kwargs)
            info = device.get_device_info()
            if info.get('connected'):
                print(f'✅ SUCCESS: Connected via {method_name}')
                print(f'Device info: {info}')
                break
        except Exception as e:
            print(f'❌ {method_name} failed: {e}')
    else:
        print('❌ All connection methods failed')
        
except Exception as e:
    print(f'❌ Import or initialization error: {e}')
" 2>&1)

echo "$TEST_OUTPUT"

if echo "$TEST_OUTPUT" | grep -q "SUCCESS"; then
    print_status "iOS MCP connection test passed!"
else
    print_warning "iOS MCP connection test failed"
    print_info "This may be normal if WebDriverAgent is not running"
fi

# Final recommendations
echo ""
echo "📋 Setup Verification Complete"
echo "=============================="
echo ""

print_info "To start the iOS MCP server:"
echo "  # For iOS Simulator:"
echo "  uv run main.py --simulator"
echo ""
echo "  # For physical device via USB:"
echo "  uv run main.py --usb"
echo ""
echo "  # For physical device via network:"
echo "  uv run main.py --device 192.168.1.100:8100"
echo ""

print_info "For more help, see README.md or run:"
echo "  uv run main.py --help"

echo ""
print_status "Setup verification complete! 🎉"