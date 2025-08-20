# Android MCP Server

A lightweight MCP (Model Context Protocol) server for Android operating system automation. This server provides tools to interact directly with Android devices, enabling automated testing, app interaction, and device control.

## Features

- **Device Control**: Click, long click, swipe, drag, and type on Android devices
- **State Management**: Get device state with optional visual screenshots
- **Navigation**: Press hardware buttons and access notifications
- **Automation**: Wait functionality for timing control
- **Emulator Support**: Works with both physical devices and Android emulators

## Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Android device or emulator with USB debugging enabled
- ADB (Android Debug Bridge) installed and accessible

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: using pip
pip install uv
```

### 2. Set up the project

```bash
# Navigate to the android MCP directory
cd mcp/android

# Install dependencies
uv sync

# Activate the virtual environment (optional, uv run handles this automatically)
source .venv/bin/activate
```

### 3. Verify installation

```bash
# Test the server
uv run main.py --help
```

## Usage

### Running the server

#### For physical devices:
```bash
uv run main.py
```

#### For Android emulator:
```bash
uv run main.py --emulator
```

### Device Setup

1. **Enable Developer Options** on your Android device:
   - Go to Settings > About phone
   - Tap "Build number" 7 times

2. **Enable USB Debugging**:
   - Go to Settings > Developer options
   - Enable "USB debugging"

3. **Connect device** and verify ADB connection:
   ```bash
   adb devices
   ```

## MCP Server Configuration

Add the following configuration to your MCP client settings (e.g., Claude Desktop, Cline, etc.):

```json
{
  "android-mcp": {
    "type": "stdio",
    "command": "bash",
    "args": [
      "-c",
      "cd /Users/tommy-amarbank/Documents/startup/agent/mcp/android && source .venv/bin/activate && uv run main.py --emulator"
    ],
    "alwaysAllow": [
      "State-Tool",
      "Click-Tool",
      "Type-Tool"
    ]
  }
}
```

**Note**: Update the path in the configuration to match your actual project location.
change /Users/tommy-amarbank/Documents/startup/agent/mcp/android to your actual path 

### Configuration Options

- **For physical devices**: Remove the `--emulator` flag from the args
- **Custom device**: Add `--device <device_id>` to specify a particular device
- **alwaysAllow**: Pre-approve specific tools to avoid repeated permission prompts

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **Click-Tool** | Click on specific coordinates | `x: int, y: int` |
| **State-Tool** | Get device state with optional screenshot | `use_vision: bool = false` |
| **Long-Click-Tool** | Long press on coordinates | `x: int, y: int, duration: int` |
| **Swipe-Tool** | Swipe between coordinates | `x1: int, y1: int, x2: int, y2: int` |
| **Type-Tool** | Type text at coordinates | `text: str, x: int, y: int, clear: bool = false` |
| **Drag-Tool** | Drag and drop between coordinates | `x1: int, y1: int, x2: int, y2: int` |
| **Press-Tool** | Press hardware buttons | `button: str` |
| **Notification-Tool** | Access notification panel | None |
| **Wait-Tool** | Wait for specified duration | `duration: int` |

## Troubleshooting

### Common Issues

1. **Device not found**:
   - Ensure USB debugging is enabled
   - Check `adb devices` output
   - Try different USB cables/ports

2. **Permission denied**:
   - Allow USB debugging permission on device
   - Check device authorization in `adb devices`

3. **Connection timeout**:
   - Restart ADB: `adb kill-server && adb start-server`
   - Reconnect device

4. **Python version issues**:
   - Ensure Python 3.13+ is installed
   - Use `uv python install 3.13` if needed

### Emulator Setup

If using Android emulator:

1. Start Android emulator (usually accessible as `emulator-5554`)
2. Verify connection: `adb connect emulator-5554`
3. Use `--emulator` flag when running the server

## Development

### Project Structure

```
mcp/android/
├── README.md
├── pyproject.toml
├── main.py           # MCP server entry point
├── src/
│   ├── mobile/       # Device interaction logic
│   └── tree/         # UI tree parsing and state management
└── .venv/           # Virtual environment
```

### Dependencies

- **mcp**: Model Context Protocol framework
- **uiautomator2**: Android device automation
- **pillow**: Image processing for screenshots
- **ipykernel**: Jupyter kernel support

