#!/bin/bash
# Automated WebDriverAgent Setup for Real iPhone

set -e

echo "📱 WebDriverAgent Setup for Real iPhone"
echo "======================================="

DEVICE_UDID="00008101-000429600AD8001E"  # Tommy iPhone from xctrace output
WDA_PORT=8100

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Check if device is connected
echo "🔍 Checking device connection..."
if xcrun devicectl list devices | grep -q "$DEVICE_UDID"; then
    print_status "Tommy iPhone is connected and ready"
else
    print_error "Tommy iPhone not found. Please:"
    echo "  1. Connect iPhone via USB"
    echo "  2. Unlock iPhone and trust this Mac"
    echo "  3. Enable Developer Mode (Settings → Privacy & Security → Developer Mode)"
    exit 1
fi

# Check if WebDriverAgent repository exists
if [ ! -d "WebDriverAgent" ]; then
    print_info "Cloning WebDriverAgent repository..."
    git clone https://github.com/appium/WebDriverAgent.git
    cd WebDriverAgent
else
    print_status "WebDriverAgent repository found"
    cd WebDriverAgent
    
    # Update to latest version
    print_info "Updating WebDriverAgent..."
    git pull origin master
fi

# Check if we have a valid development team
print_info "Checking for Apple Developer Team..."

# Try to get available teams
TEAMS=$(xcrun xcodebuild -showBuildSettings -project WebDriverAgent.xcodeproj -target WebDriverAgentRunner 2>/dev/null | grep DEVELOPMENT_TEAM | head -1 | awk '{print $3}')

if [ -z "$TEAMS" ] || [ "$TEAMS" = "" ]; then
    print_warning "No development team configured"
    print_info "Please follow these steps in Xcode:"
    echo ""
    echo "1. Open WebDriverAgent project:"
    echo "   open WebDriverAgent.xcodeproj"
    echo ""
    echo "2. Select WebDriverAgentRunner target"
    echo "3. Go to Signing & Capabilities tab"
    echo "4. Select your Apple Developer Team"
    echo "5. Change Bundle Identifier to: com.yourname.WebDriverAgentRunner"
    echo ""
    read -p "Press Enter after configuring signing in Xcode..."
fi

# Build WebDriverAgent for the device
print_info "Building WebDriverAgent for your iPhone..."

# First, clean any previous builds
xcodebuild clean -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner

# Build and install to device
print_info "Building and installing WebDriverAgentRunner..."
xcodebuild build-for-testing \
    -project WebDriverAgent.xcodeproj \
    -scheme WebDriverAgentRunner \
    -destination "id=$DEVICE_UDID" \
    -allowProvisioningUpdates

if [ $? -eq 0 ]; then
    print_status "WebDriverAgent built successfully!"
else
    print_error "Build failed. Common fixes:"
    echo "  1. Check Apple Developer Team is selected"
    echo "  2. Make sure Bundle ID is unique (com.yourname.WebDriverAgentRunner)"
    echo "  3. Trust developer certificate on iPhone:"
    echo "     Settings → General → VPN & Device Management → Trust"
    exit 1
fi

# Start WebDriverAgent on the device
print_info "Starting WebDriverAgent on your iPhone..."

# Kill any existing WebDriverAgent processes
pkill -f WebDriverAgent || true

# Start WebDriverAgent test runner (this will keep it running)
print_status "Launching WebDriverAgent on Tommy iPhone..."
print_warning "Keep this terminal window open!"

echo ""
print_info "WebDriverAgent will start on your iPhone"
print_info "You may need to trust the app on your iPhone:"
echo "  Settings → General → VPN & Device Management → Trust Developer"
echo ""
print_info "WebDriverAgent will be available at:"
echo "  http://localhost:$WDA_PORT"
echo ""
print_info "Once running, start iOS MCP with:"
echo "  uv run main.py --usb --device $DEVICE_UDID"
echo "  or"
echo "  uv run main.py --device IPHONE_IP:$WDA_PORT"
echo ""

# Run WebDriverAgent test to start the server
xcodebuild test-without-building \
    -project WebDriverAgent.xcodeproj \
    -scheme WebDriverAgentRunner \
    -destination "id=$DEVICE_UDID" \
    -allowProvisioningUpdates