# Mac MCP Server

A comprehensive Model Context Protocol (MCP) server for macOS desktop automation and system control. This server provides native Mac application control, file operations, system management, and AppleScript automation capabilities, similar to the Android and iOS MCP servers in this project.

## 🚀 Features

### Core Automation
- **Desktop Control**: Click, type, drag, scroll operations with pixel-perfect precision
- **Element Interaction**: Access UI elements through accessibility properties
- **Keyboard Control**: Send complex key combinations and shortcuts
- **Mouse Operations**: Precise mouse movements, clicks, and drag operations

### Application Management
- **App Control**: Launch, quit, activate, hide applications
- **Window Management**: Resize, move, minimize, maximize, close windows
- **Menu Bar Interaction**: Navigate and click menu items
- **Dock Control**: Manage dock applications and settings

### System Features
- **File Operations**: Copy, move, delete, create files and directories with safety checks
- **Clipboard Management**: Read and write clipboard content (text, images, files)
- **Screenshot Capture**: Full screen, window, or region screenshots with annotation
- **System Monitoring**: Process management, system stats, network information

### Advanced Capabilities
- **AppleScript Execution**: Run custom AppleScript for complex automation
- **Shell Commands**: Execute terminal commands with safety restrictions
- **System Preferences**: Control system settings and preferences
- **Accessibility Features**: Support for accessibility tools and features

### Security & Safety
- **Safe Mode**: Restricted operations for secure environments
- **Permission Checks**: Verify accessibility and security permissions
- **Command Filtering**: Block dangerous shell commands in safe mode
- **File Protection**: Safe delete operations with trash support

## 📦 Installation

### Prerequisites

- macOS 10.15+ (Catalina or later)
- Python 3.10+
- Accessibility permissions (for advanced features)

### Quick Setup

1. **Clone and navigate to the Mac MCP directory:**
   ```bash
   cd mcp/mac
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure accessibility permissions (optional but recommended):**
   - Open System Preferences/Settings
   - Go to Security & Privacy > Privacy > Accessibility
   - Add Terminal and Python to the allowed applications

### Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install PyObjC frameworks:**
   ```bash
   pip install pyobjc-core pyobjc-framework-Cocoa pyobjc-framework-Quartz
   ```

3. **Create configuration file:**
   ```bash
   cp .env.example .env
   ```

## 🎯 Usage

### Basic Server

Start the Mac MCP server with default settings:

```bash
python3 main.py
```

### With Accessibility Features

Enable full automation capabilities:

```bash
python3 main.py --enable-accessibility
```

### Safe Mode

Run with restricted operations:

```bash
python3 main.py --safe-mode
```

### Custom Configuration

```bash
python3 main.py --device-name "My MacBook Pro" --enable-accessibility --log-level DEBUG
```

## 🛠️ Available Tools

### Desktop Control Tools

#### `Click-Tool`
Click on specific coordinates on the desktop.

```json
{
  "name": "Click-Tool",
  "parameters": {
    "x": 500,
    "y": 300,
    "click_type": "left",
    "double_click": false
  }
}
```

#### `Element-Click-Tool`
Click on UI elements by accessibility properties.

```json
{
  "name": "Element-Click-Tool",
  "parameters": {
    "element_type": "button",
    "identifier": "OK",
    "app_name": "Finder",
    "timeout": 10.0
  }
}
```

#### `Type-Tool`
Type text at current cursor position or coordinates.

```json
{
  "name": "Type-Tool",
  "parameters": {
    "text": "Hello, World!",
    "x": 400,
    "y": 200,
    "clear": true
  }
}
```

#### `Key-Press-Tool`
Send keyboard shortcuts and key combinations.

```json
{
  "name": "Key-Press-Tool",
  "parameters": {
    "keys": "c",
    "modifier_keys": "cmd"
  }
}
```

### Application Management Tools

#### `App-Control-Tool`
Control Mac applications.

```json
{
  "name": "App-Control-Tool",
  "parameters": {
    "action": "launch",
    "app_name": "Safari",
    "window_title": null
  }
}
```

#### `Window-Control-Tool`
Control application windows.

```json
{
  "name": "Window-Control-Tool",
  "parameters": {
    "action": "resize",
    "app_name": "Safari",
    "width": 1200,
    "height": 800
  }
}
```

#### `App-List-Tool`
List running applications and their windows.

```json
{
  "name": "App-List-Tool",
  "parameters": {
    "running_only": true
  }
}
```

### System Tools

#### `File-Operations-Tool`
Perform file and directory operations.

```json
{
  "name": "File-Operations-Tool",
  "parameters": {
    "action": "copy",
    "source_path": "~/Documents/file.txt",
    "destination_path": "~/Desktop/file_backup.txt",
    "recursive": false
  }
}
```

#### `Screenshot-Tool`
Take screenshots of desktop or specific areas.

```json
{
  "name": "Screenshot-Tool",
  "parameters": {
    "save_path": "~/Desktop/screenshot.png",
    "x": 0,
    "y": 0,
    "width": 1920,
    "height": 1080
  }
}
```

#### `System-Info-Tool`
Get comprehensive system information.

```json
{
  "name": "System-Info-Tool",
  "parameters": {}
}
```

### Advanced Tools

#### `AppleScript-Tool`
Execute AppleScript commands for advanced automation.

```json
{
  "name": "AppleScript-Tool",
  "parameters": {
    "script": "tell application \"Finder\" to open home",
    "timeout": 30.0
  }
}
```

#### `Shell-Command-Tool`
Execute shell commands with safety restrictions.

```json
{
  "name": "Shell-Command-Tool",
  "parameters": {
    "command": "ls -la ~/Desktop",
    "timeout": 30.0,
    "safe_mode": true
  }
}
```

#### `State-Tool`
Get the current state of the Mac desktop with optional screenshot.

```json
{
  "name": "State-Tool",
  "parameters": {
    "use_vision": true
  }
}
```

## ⚙️ Configuration

### Environment Variables

Configure the server behavior through `.env` file:

```env
# Device Configuration
MAC_DEVICE_NAME="Local Mac"
ENABLE_ACCESSIBILITY=false
SAFE_MODE=false
LOG_LEVEL=INFO

# Security Settings
ALLOW_SHELL_COMMANDS=true
ALLOW_FILE_OPERATIONS=true
ALLOW_SYSTEM_CHANGES=false

# Performance Settings
ELEMENT_DISCOVERY_TIMEOUT=10.0
APPLESCRIPT_TIMEOUT=30.0
SCREENSHOT_SCALE=1.0
```

### Command Line Options

- `--device-name`: Set custom device name for identification
- `--enable-accessibility`: Enable accessibility features for UI automation
- `--safe-mode`: Run with restricted system operations
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## 🔒 Security & Permissions

### Accessibility Permissions

For full automation capabilities, grant accessibility permissions:

1. Open **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
2. Click the lock to make changes
3. Add **Terminal** (or your terminal application)
4. Add **Python** if prompted during first run

### Safe Mode

When `--safe-mode` is enabled, the following restrictions apply:

- No dangerous shell commands (rm, sudo, shutdown, etc.)
- No system preference modifications
- No process killing capabilities
- File operations use safe delete (move to trash)

### File Operations Safety

- Automatic backup options for destructive operations
- Safe delete moves files to trash instead of permanent deletion
- Path validation and expansion for security
- Size limits for file operations

## 📱 Integration Examples

### Basic Automation Workflow

```python
# Launch Safari and navigate to a website
await mcp_client.call_tool("App-Control-Tool", {
    "action": "launch",
    "app_name": "Safari"
})

await mcp_client.call_tool("Key-Press-Tool", {
    "keys": "l",
    "modifier_keys": "cmd"
})

await mcp_client.call_tool("Type-Tool", {
    "text": "https://example.com"
})

await mcp_client.call_tool("Key-Press-Tool", {
    "keys": "return"
})
```

### File Management

```python
# Create a new directory and copy files
await mcp_client.call_tool("File-Operations-Tool", {
    "action": "create_dir",
    "source_path": "~/Desktop/MyProject"
})

await mcp_client.call_tool("File-Operations-Tool", {
    "action": "copy",
    "source_path": "~/Documents/source.txt",
    "destination_path": "~/Desktop/MyProject/source.txt"
})
```

### Screenshot and Visual Analysis

```python
# Take annotated screenshot for visual analysis
result = await mcp_client.call_tool("State-Tool", {
    "use_vision": True
})

# Take specific region screenshot
await mcp_client.call_tool("Screenshot-Tool", {
    "save_path": "~/Desktop/region.png",
    "x": 100,
    "y": 100,
    "width": 800,
    "height": 600
})
```

## 🧪 Testing

### Run Basic Tests

```bash
# Test system information
python3 -c "
from src.mac import MacDevice
mac = MacDevice()
print(mac.get_system_info())
"

# Test screenshot capability
python3 -c "
from src.mac import MacDevice
mac = MacDevice()
result = mac.take_screenshot('~/Desktop/test.png')
print(result)
"
```

### Test Accessibility Features

```bash
# Test with accessibility enabled
python3 main.py --enable-accessibility --log-level DEBUG
```

## 🤝 Integration with Other MCP Servers

The Mac MCP server integrates seamlessly with other MCP servers in this project:

- **Android MCP**: Cross-platform mobile automation
- **iOS MCP**: Complete Apple ecosystem control
- **Chrome MCP**: Web automation and testing
- **Slack MCP**: Team communication and workflow

### Example Multi-Platform Workflow

1. Use Mac MCP to capture requirements from desktop applications
2. Use Chrome MCP to research and gather information
3. Use iOS MCP to test mobile implementations
4. Use Slack MCP to coordinate with team members

## 📚 API Reference

### Error Handling

All tools return structured responses with error information:

```json
{
  "success": true,
  "result": "Operation completed successfully",
  "error": null
}
```

### Response Formats

- **String responses**: Simple operation results
- **JSON responses**: Complex data structures
- **Binary responses**: Screenshots and file data
- **Error responses**: Detailed error information with suggestions

## 🔧 Troubleshooting

### Common Issues

1. **Accessibility Permission Denied**
   - Solution: Grant accessibility permissions in System Preferences

2. **PyObjC Import Errors**
   - Solution: Reinstall PyObjC frameworks with `pip install --upgrade pyobjc`

3. **AppleScript Timeout**
   - Solution: Increase timeout values in configuration

4. **File Operation Permissions**
   - Solution: Check file permissions and disable safe mode if needed

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
python3 main.py --log-level DEBUG
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤖 About SDLC Agent Workflow

This Mac MCP server is part of the SDLC Agent Workflow project, an AI-powered software development lifecycle automation platform. The project aims to streamline development processes through intelligent automation and cross-platform integration.

For more information about the complete SDLC Agent Workflow platform, visit the main project repository.

---

**Note**: This server requires macOS and appropriate system permissions for full functionality. Some features may be limited without accessibility permissions.