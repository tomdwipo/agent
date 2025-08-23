#!/bin/bash
# Real iPhone WebDriverAgent Setup Script

echo "📱 iOS Real Device Setup for WebDriverAgent"
echo "=========================================="

# Check if iPhone is connected
echo "🔍 Checking for connected iPhone..."
CONNECTED_DEVICES=$(idevice_id -l 2>/dev/null || echo "")

if [ -z "$CONNECTED_DEVICES" ]; then
    echo "❌ No iPhone detected. Please:"
    echo "   1. Connect iPhone via USB cable"
    echo "   2. Unlock iPhone"  
    echo "   3. Tap 'Trust This Computer'"
    echo "   4. Enable Developer Mode (iOS 16+):"
    echo "      Settings → Privacy & Security → Developer Mode → On"
    exit 1
else
    echo "✅ iPhone connected:"
    echo "$CONNECTED_DEVICES" | while read device; do
        echo "   📱 $device"
    done
fi

# Clone WebDriverAgent if not exists
if [ ! -d "WebDriverAgent" ]; then
    echo "📥 Cloning WebDriverAgent..."
    git clone https://github.com/appium/WebDriverAgent.git
else
    echo "✅ WebDriverAgent already exists"
fi

cd WebDriverAgent

echo "🔧 Setting up WebDriverAgent..."
echo "================================"

echo "📝 Next steps (manual):"
echo "1. Open WebDriverAgent.xcodeproj in Xcode:"
echo "   open WebDriverAgent.xcodeproj"
echo ""
echo "2. In Xcode, select WebDriverAgentRunner target"
echo "3. Go to Signing & Capabilities tab"
echo "4. Select your Apple Developer Team"
echo "5. Change Bundle Identifier to something unique:"
echo "   com.yourname.WebDriverAgentRunner"
echo ""
echo "6. Connect your iPhone and select it as destination"
echo "7. Build and run WebDriverAgentRunner (Cmd+R)"
echo ""
echo "8. On your iPhone, trust the developer:"
echo "   Settings → General → VPN & Device Management"
echo "   → Trust your developer certificate"
echo ""
echo "9. WebDriverAgent should start and show local IP"
echo "   Note the IP address (e.g., 192.168.1.100:8100)"

echo ""
echo "🚀 Once WebDriverAgent is running, start iOS MCP:"
echo "cd ../mcp/ios"
echo "uv run main.py --device YOUR_IPHONE_IP:8100"
echo ""
echo "Example: uv run main.py --device 192.168.1.100:8100"