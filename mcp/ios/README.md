# iOS MCP Server

A Model Context Protocol (MCP) server for iOS device automation and testing. This server provides comprehensive iOS device control capabilities similar to the Android MCP server, enabling automated testing, app interaction, and device control through WebDriverAgent.

## 🚀 Quick Start

**New to iOS MCP? Start here for fastest setup:**

### **Option A: iOS Simulator (Easiest)**

```bash
# 1. Navigate to iOS MCP directory
cd mcp/ios

# 2. Run setup verification (checks dependencies and provides guidance)
./setup.sh

# 3. For iOS Simulator (easiest option):
# Install Appium in another terminal:
npm install -g appium
appium driver install xcuitest
appium --port 4723

# 4. Start iOS MCP server:
uv run main.py --simulator --port 4723
```

### **Option B: Real iPhone via USB (More Powerful)**

```bash
# 1. Connect iPhone via USB and trust computer
# 2. Enable Developer Mode (iOS 16+): Settings → Privacy & Security → Developer Mode → On

# 3. Automated setup:
cd mcp/ios
./setup_real_iphone_auto.py

# 4. Or manual setup:
./setup_real_iphone.sh

# 5. Start iOS MCP server:
uv run main.py --usb
```

### **Option C: Real iPhone via WiFi (Most Convenient)**

```bash
# 1. First, set up WebDriverAgent via USB (one-time setup)
cd mcp/ios
cd WebDriverAgent
xcodebuild test-without-building -project WebDriverAgent.xcodeproj \
  -scheme WebDriverAgentRunner -destination 'id=YOUR_DEVICE_UDID' \
  -allowProvisioningUpdates

# 2. Find your iPhone's IP address:
# Method A: iPhone Settings → Wi-Fi → (i) icon → Note IP Address
# Method B: Automated discovery
python3 find_iphone_ip.py

# 3. Start iOS MCP server via WiFi:
uv run main.py --device YOUR_IPHONE_IP:8100
# Example: uv run main.py --device 192.168.1.2:8100
```

**That's it!** The server will guide you through any missing setup steps.

---

## Features

- 📱 **iOS Device Control** - Tap, swipe, type, and interact with iOS devices and simulators
- 🔍 **Element Detection** - Advanced UI element detection and interaction using various selectors
- 📸 **Visual Screenshots** - Capture and annotate screenshots with interactive elements
- 🎮 **App Lifecycle Management** - Launch, terminate, and control iOS applications
- 🔄 **Multiple Connection Methods** - WiFi, USB, and iOS Simulator support
- 🎯 **Precise Element Targeting** - XPath, predicate, and accessibility-based element selection
- 🔒 **Device Management** - Lock/unlock, volume control, orientation changes
- ⚡ **Alert Handling** - Automatic handling of iOS alerts and dialogs

## WiFi Connection Setup

### Prerequisites for WiFi Connection
- iPhone and Mac must be on the **same WiFi network**
- WebDriverAgent must be **built and trusted** on the iPhone first
- iPhone must have **Developer Mode enabled** (iOS 16+)

### Step-by-Step WiFi Setup

#### 1. Initial USB Setup (Required Once)
```bash
# Connect iPhone via USB first
cd mcp/ios

# Check if iPhone is detected
uv run tidevice list
# Should show: 00008101-000429600AD8001E ... Tommy iPhone ... usb

# Build and start WebDriverAgent
cd WebDriverAgent
xcodebuild test-without-building -project WebDriverAgent.xcodeproj \
  -scheme WebDriverAgentRunner -destination 'id=00008101-000429600AD8001E' \
  -allowProvisioningUpdates
```

#### 2. Find iPhone IP Address
```bash
# Method 1: iPhone Settings
# Settings → Wi-Fi → (i) next to network → IP Address

# Method 2: Automated discovery
cd mcp/ios
python3 find_iphone_ip.py

# Method 3: Quick network scan
./quick_find_ip.sh

# Method 4: Manual network scan
arp -a | grep "192.168.1"
nmap -sn 192.168.1.0/24
```

#### 3. Connect via WiFi
```bash
# Once WebDriverAgent is running and IP is known:
cd mcp/ios

# Test WebDriverAgent accessibility
curl http://YOUR_IPHONE_IP:8100/status

# Start iOS MCP server via WiFi
uv run main.py --device YOUR_IPHONE_IP:8100

# Example with actual IP:
uv run main.py --device 192.168.1.2:8100
```

### WiFi Connection Commands Reference

#### Using tidevice via WiFi
```bash
# Note: Use the correct bundle ID (com.tommy.WebDriverAgentRunner.xctrunner)
uv run tidevice -u YOUR_IPHONE_IP wdaproxy -B com.tommy.WebDriverAgentRunner.xctrunner

# Example:
uv run tidevice -u 192.168.1.2 wdaproxy -B com.tommy.WebDriverAgentRunner.xctrunner
```

#### Direct iOS MCP Connection
```bash
# WiFi connection (recommended)
uv run main.py --device 192.168.1.2:8100

# USB connection (fallback)
uv run main.py --usb

# Auto-detect connection
uv run main.py
```

### WiFi Troubleshooting

#### Connection Issues
```bash
# 1. Verify iPhone is on same network
ping YOUR_IPHONE_IP

# 2. Check WebDriverAgent is running
curl http://YOUR_IPHONE_IP:8100/status

# 3. Check for connection errors
uv run main.py --device YOUR_IPHONE_IP:8100 --verbose
```

#### Common WiFi Issues

| Issue | Solution |
|-------|----------|
| **"Connection refused"** | WebDriverAgent not running → Start via USB first |
| **"No route to host"** | Different WiFi networks → Connect to same network |
| **"Device not found"** | Wrong IP address → Use `find_iphone_ip.py` |
| **"Bundle ID not found"** | Use `com.tommy.WebDriverAgentRunner.xctrunner` |
| **"Pairing failed"** | Dependencies missing → `uv sync` |

#### Automated WiFi Setup
```bash
# Use automated WiFi setup script
cd mcp/ios
python3 setup_wifi_debugging.py

# This script will:
# 1. Check USB connection
# 2. Enable WiFi debugging
# 3. Find iPhone IP
# 4. Test WiFi connection
# 5. Start WebDriverAgent via WiFi
```

## Prerequisites

- **Python** >= 3.10
- **macOS** (required for iOS device interaction)
- **Xcode** and **Xcode Command Line Tools**
- **WebDriverAgent** setup (see Setup section)
- **uv** package manager (recommended)

### iOS Device Requirements
- iOS device with **iOS 9.3+** or iOS Simulator
- **Developer Mode** enabled (iOS 16+)
- **USB debugging** enabled for physical devices

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: using pip
pip install uv
```

### 2. Set up the project

```bash
# Navigate to the iOS MCP directory
cd mcp/ios

# Install dependencies
uv sync

# Activate virtual environment (optional)
source .venv/bin/activate
```

### 3. WebDriverAgent Setup

#### Option A: Using Appium WebDriverAgent (Recommended)

```bash
# Install Appium
npm install -g appium
npm install -g @appium/doctor

# Install XCUITest driver
appium driver install xcuitest

# Check setup
appium doctor --ios
```

#### Option B: Manual WebDriverAgent Setup

```bash
# Clone WebDriverAgent
git clone https://github.com/appium/WebDriverAgent.git
cd WebDriverAgent

# Open in Xcode and configure signing
open WebDriverAgent.xcodeproj

# Build and run WebDriverAgentRunner target
# Set your development team in Build Settings
```

### 4. Device Setup

#### For Physical Devices:
1. Enable **Developer Mode** in Settings > Privacy & Security > Developer Mode
2. Trust your Mac in Settings > General > Device Management
3. Ensure device is connected via USB or on same WiFi network

#### For iOS Simulator:
1. Install Xcode and iOS Simulator
2. Launch desired simulator
3. WebDriverAgent will connect automatically

## Usage

### Running the Server

#### For iOS Simulator:
```bash
uv run main.py --simulator
```

#### For Physical Device (WiFi) - Recommended:
```bash
# Find iPhone IP first
python3 find_iphone_ip.py

# Connect via WiFi
uv run main.py --device 192.168.1.2:8100
```

#### For Physical Device (USB):
```bash
uv run main.py --usb --device YOUR_DEVICE_UDID
```

#### Auto-detect Device:
```bash
uv run main.py
```

### Starting WebDriverAgent

#### Using Xcode (Recommended for initial setup):
```bash
# In WebDriverAgent directory
cd WebDriverAgent
xcodebuild test-without-building -project WebDriverAgent.xcodeproj \
           -scheme WebDriverAgentRunner \
           -destination 'id=YOUR_DEVICE_UDID' \
           -allowProvisioningUpdates

# Example with actual device ID:
xcodebuild test-without-building -project WebDriverAgent.xcodeproj \
           -scheme WebDriverAgentRunner \
           -destination 'id=UDID' \
           -allowProvisioningUpdates
```

# 1. Connect iPhone via USB cable
# 2. Unlock iPhone and tap "Trust This Computer"
# 3. Check if device is detected:
cd /Users/tommy-amarbank/Documents/startup/agent/mcp/ios
uv run tidevice list


# Once USB connected, enable WiFi debugging:
uv run tidevice -u YOUR_DEVICE_UDID pair


# Check iPhone Settings → Wi-Fi → (i) next to network → IP Address
# OR use our network scanner:
python3 find_iphone_ip.py


# Correct syntax (note -u position):
uv run tidevice -u 192.168.1.2 wdaproxy -B com.facebook.WebDriverAgentRunner.xctrunner

cd /Users/tommy-amarbank/Documents/startup/agent/mcp/ios
python3 setup_wifi_debugging.py

uv run tidevice list

cd /Users/tommy-amarbank/Documents/startup/agent/mcp/ios/WebDriverAgent && xcodebuild test-without-building -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination 'id=YOUR_DEVICE_UDID' -allowProvisioningUpdates

curl http://192.168.1.2:8100/status

#### Using tidevice (for USB connections):
```bash
# Install tidevice
pip install tidevice

# Start WebDriverAgent via USB
tidevice wdaproxy -B com.tommy.WebDriverAgentRunner.xctrunner
```

#### Using tidevice (for WiFi connections):
```bash
# Note: WebDriverAgent must be running first (via Xcode)
# Then use tidevice to proxy the connection
tidevice -u YOUR_IPHONE_IP wdaproxy -B com.tommy.WebDriverAgentRunner.xctrunner

# Example:
tidevice -u 192.168.1.2 wdaproxy -B com.tommy.WebDriverAgentRunner.xctrunner
```

## MCP Server Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "ios-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/agent/mcp/ios && source .venv/bin/activate && uv run main.py --device 192.168.1.2:8100"
      ],
      "alwaysAllow": [
        "State-Tool",
        "Click-Tool",
        "Element-Tap-Tool",
        "Type-Tool"
      ]
    }
  }
}
```

**Note**: Update the path and connection method according to your setup.

## Available Tools

### Basic Interaction Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **Click-Tool** | Tap on specific coordinates | `x: int, y: int` |
| **State-Tool** | Get device state with optional screenshot | `use_vision: bool = false` |
| **Long-Press-Tool** | Long press on coordinates | `x: int, y: int, duration: float = 1.0` |
| **Swipe-Tool** | Swipe between coordinates | `x1: int, y1: int, x2: int, y2: int, duration: float = 0.5` |
| **Type-Tool** | Type text on device | `text: str, clear: bool = false` |

### Advanced Element Interaction

| Tool | Description | Parameters |
|------|-------------|------------|
| **Element-Tap-Tool** | Tap element by selector | `selector: str, value: str, timeout: float = 10.0` |
| **Element-Type-Tool** | Type in element by selector | `selector: str, value: str, text: str, clear: bool = true` |
| **Element-Wait-Tool** | Wait for element to appear | `selector: str, value: str, timeout: float = 10.0` |

#### Supported Selectors:
- `id` - Accessibility identifier
- `name` - Element name
- `label` - Accessibility label  
- `className` - XCUIElement class name
- `xpath` - XPath expression
- `predicate` - NSPredicate string

### Device Control Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **Home-Tool** | Press home button | None |
| **Volume-Tool** | Press volume buttons | `direction: str` (up/down) |
| **Lock-Tool** | Lock/unlock device | `action: str` (lock/unlock) |
| **Orientation-Tool** | Get/set orientation | `orientation: str` (optional) |

### App Management Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **App-Control-Tool** | Control app lifecycle | `action: str, bundle_id: str` |

#### App Actions:
- `launch` - Launch application
- `terminate` - Terminate application  
- `activate` - Bring app to foreground
- `state` - Get app state

### Utility Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **Wait-Tool** | Wait for duration | `duration: float` |
| **Alert-Tool** | Handle iOS alerts | `action: str, text: str = None` |
| **Scroll-Tool** | Scroll in direction | `direction: str, distance: float = 0.5` |

## Usage Examples

### Basic Device Interaction

```bash
# Take screenshot and see interactive elements
State-Tool --use_vision true

# Tap on specific coordinates
Click-Tool --x 200 --y 300

# Type text
Type-Tool --text "Hello iOS!" --clear true
```

### Element-Based Interaction

```bash
# Tap on button by accessibility ID
Element-Tap-Tool --selector id --value "loginButton"

# Type in text field by name
Element-Type-Tool --selector name --value "Username" --text "testuser"

# Wait for element to appear
Element-Wait-Tool --selector label --value "Welcome" --timeout 15.0
```

### App Testing Workflow

```bash
# Launch app
App-Control-Tool --action launch --bundle_id com.example.MyApp

# Wait for app to load
Wait-Tool --duration 2.0

# Get app state and interact
State-Tool --use_vision true
Element-Tap-Tool --selector label --value "Get Started"

# Handle alerts if they appear
Alert-Tool --action accept
```

### Advanced Element Selection

```bash
# Using XPath
Element-Tap-Tool --selector xpath --value "//XCUIElementTypeButton[@name='Submit']"

# Using predicate
Element-Tap-Tool --selector predicate --value "name LIKE '*Login*'"

# Using class name
Element-Tap-Tool --selector className --value "XCUIElementTypeTextField"
```

## Troubleshooting

### 🔴 Connection Errors (FIXED!)

**Before our improvements, you might have seen:**
```
ConnectionRefusedError: [Errno 61] Connection refused
```

**Now you'll see helpful guidance instead:**
```
🛠️  iOS MCP SERVER SETUP REQUIRED
================================================================================
📱 iOS SIMULATOR SETUP:

1️⃣  Install Appium (Recommended):
   npm install -g appium
   appium driver install xcuitest
   appium --port 4723
```

The server now:
- ✅ **Detects missing WebDriverAgent automatically**
- ✅ **Provides step-by-step setup instructions** 
- ✅ **Attempts auto-setup when possible**
- ✅ **Retries connection with clear feedback**
- ✅ **Gracefully handles all error cases**

### WiFi Connection Issues

#### 1. **"Connection Refused" via WiFi**
```bash
# Check if WebDriverAgent is running
curl http://YOUR_IPHONE_IP:8100/status

# If not running, start via USB first:
cd WebDriverAgent
xcodebuild test-without-building -project WebDriverAgent.xcodeproj \
  -scheme WebDriverAgentRunner -destination 'id=YOUR_DEVICE_UDID' \
  -allowProvisioningUpdates
```

#### 2. **"Device Not Found" via WiFi**
```bash
# Find correct iPhone IP
python3 find_iphone_ip.py

# Or check iPhone manually:
# Settings → Wi-Fi → (i) → IP Address

# Test connectivity
ping YOUR_IPHONE_IP
```

#### 3. **"No app matches" Error**
```bash
# Use correct bundle ID:
com.tommy.WebDriverAgentRunner.xctrunner
# NOT: com.facebook.WebDriverAgentRunner.xctrunner

# Check installed apps:
uv run tidevice applist
```

#### 4. **"pkg_resources" Error**
```bash
# Fixed by adding setuptools and pyOpenSSL dependencies
uv sync
```

### Common Issues

1. **WebDriverAgent Connection Failed**:
   - Ensure WebDriverAgent is built and running
   - Check device is connected and trusted
   - Verify port 8100 is accessible

2. **Device Not Found**:
   - Check device UDID: `xcrun simctl list devices`
   - For physical devices: `idevice_id -l`
   - Ensure device is unlocked and trusted

3. **Element Not Found**:
   - Use `State-Tool` with vision to see available elements
   - Try different selectors (name, label, className)
   - Increase timeout value

4. **Permission Denied**:
   - Enable Developer Mode on iOS 16+
   - Trust development certificates
   - Check Xcode project signing

### WebDriverAgent Issues

```bash
# Reset WebDriverAgent (USB)
pkill -f WebDriverAgent
tidevice wdaproxy -B com.tommy.WebDriverAgentRunner.xctrunner

# Reset WebDriverAgent (WiFi)
pkill -f WebDriverAgent
# Restart via Xcode method:
cd WebDriverAgent
xcodebuild test-without-building -project WebDriverAgent.xcodeproj \
  -scheme WebDriverAgentRunner -destination 'id=YOUR_DEVICE_UDID' \
  -allowProvisioningUpdates

# Check WebDriverAgent status (works for both USB/WiFi)
curl http://localhost:8100/status  # USB via tidevice proxy
curl http://YOUR_IPHONE_IP:8100/status  # Direct WiFi

# View WebDriverAgent logs
tidevice syslog | grep WebDriverAgent
```

### iOS Simulator Issues

```bash
# List available simulators
xcrun simctl list devices

# Boot specific simulator
xcrun simctl boot "iPhone 14 Pro"

# Reset simulator
xcrun simctl erase all
```

## Development

### Project Structure

```
mcp/ios/
├── README.md
├── pyproject.toml
├── main.py                 # MCP server entry point
├── src/
│   ├── ios/                # iOS device management
│   │   ├── __init__.py     # Main IOSDevice class
│   │   └── views.py        # State representation
│   └── tree/               # UI tree parsing
│       ├── __init__.py     # Tree parsing logic
│       ├── config.py       # Configuration
│       ├── utils.py        # Helper functions
│       └── views.py        # Tree visualization
└── .venv/                  # Virtual environment
```

### Dependencies

- **mcp**: Model Context Protocol framework
- **facebook-wda**: WebDriverAgent Python client
- **tidevice**: iOS device management tools
- **pillow**: Image processing for screenshots

### Testing Your Changes

```bash
# Run basic connection test
uv run python -c "
from src.ios import IOSDevice
device = IOSDevice(simulator=True)
print('Connection successful!')
print(device.get_device_info())
"

# Test MCP tools
uv run main.py --simulator
```

## Integration with SDLC Workflow

This iOS MCP server perfectly complements your existing SDLC automation platform:

1. **Meeting Transcription** → Requirements gathering for iOS features
2. **PRD/TRD Generation** → iOS-specific technical requirements
3. **Figma MCP** → Design extraction for iOS implementation
4. **iOS MCP** → **🆕 iOS device testing and automation**
5. **Firebase Crashlytics MCP** → iOS crash analysis and debugging
6. **Docker MCP** → iOS app building and CI/CD

## Advanced Configuration

### Custom WebDriverAgent Port

```bash
# Start WebDriverAgent on custom port
tidevice wdaproxy -B com.facebook.WebDriverAgentRunner.xctrunner --port 8200

# Connect MCP server to custom port
uv run main.py --port 8200
```

### Multiple Device Support

```bash
# List connected devices
tidevice list

# Connect to specific device
uv run main.py --usb --device YOUR_DEVICE_UDID
```

### Network Connection

```bash
# Find device IP
tidevice list -u

# Connect via WiFi
uv run main.py --device 192.168.1.100:8100
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

- Built with [facebook-wda](https://github.com/openatx/facebook-wda) for WebDriverAgent integration
- Powered by [tidevice](https://github.com/alibaba/tidevice) for device management
- Inspired by the need for comprehensive iOS automation in SDLC workflows

---

**Repository:** [https://github.com/tomdwipo/agent](https://github.com/tomdwipo/agent)