# iOS MCP Server

A Model Context Protocol (MCP) server for iOS device automation and testing. This server provides comprehensive iOS device control capabilities similar to the Android MCP server, enabling automated testing, app interaction, and device control through WebDriverAgent.

## Features

- 📱 **iOS Device Control** - Tap, swipe, type, and interact with iOS devices and simulators
- 🔍 **Element Detection** - Advanced UI element detection and interaction using various selectors
- 📸 **Visual Screenshots** - Capture and annotate screenshots with interactive elements
- 🎮 **App Lifecycle Management** - Launch, terminate, and control iOS applications
- 🔄 **Multiple Connection Methods** - WiFi, USB, and iOS Simulator support
- 🎯 **Precise Element Targeting** - XPath, predicate, and accessibility-based element selection
- 🔒 **Device Management** - Lock/unlock, volume control, orientation changes
- ⚡ **Alert Handling** - Automatic handling of iOS alerts and dialogs

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

#### For Physical Device (WiFi):
```bash
uv run main.py --device 192.168.1.100:8100
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

#### Using tidevice (Recommended for USB):
```bash
# Install tidevice
pip install tidevice

# Start WebDriverAgent
tidevice wdaproxy -B com.facebook.WebDriverAgentRunner.xctrunner
```

#### Using Xcode:
```bash
# In WebDriverAgent directory
xcodebuild -project WebDriverAgent.xcodeproj \
           -scheme WebDriverAgentRunner \
           -destination 'platform=iOS,name=YOUR_DEVICE_NAME' \
           test
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
        "cd /path/to/agent/mcp/ios && source .venv/bin/activate && uv run main.py --simulator"
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
# Reset WebDriverAgent
pkill -f WebDriverAgent
tidevice wdaproxy -B com.facebook.WebDriverAgentRunner.xctrunner

# Check WebDriverAgent status
curl http://localhost:8100/status

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