#!/usr/bin/env python3
"""
iOS MCP Server

A Model Context Protocol server for iOS device automation and testing.
Provides tools to interact directly with iOS devices, enabling automated testing, 
app interaction, and device control similar to Android MCP.
"""

from mcp.server.fastmcp import FastMCP, Image
from contextlib import asynccontextmanager
from argparse import ArgumentParser
from src.ios import IOSDevice
from textwrap import dedent
import asyncio
import sys
import traceback


parser = ArgumentParser()
parser.add_argument('--device', type=str, help='Device UDID or IP address (e.g., 192.168.1.100:8100)')
parser.add_argument('--simulator', action='store_true', help='Use iOS Simulator')
parser.add_argument('--usb', action='store_true', help='Connect via USB using tidevice')
parser.add_argument('--port', type=int, default=8100, help='WebDriverAgent port (default: 8100)')
args = parser.parse_args()

instructions = dedent('''
iOS MCP server provides tools to interact directly with iOS devices and simulators,
enabling automated testing and device control similar to Android MCP.
Supports both physical devices and iOS Simulator through WebDriverAgent.

IMPORTANT: Requires WebDriverAgent to be running on the target device.
''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    await asyncio.sleep(1)  # Simulate startup latency
    yield

mcp = FastMCP(name="iOS-MCP", instructions=instructions)

# Global iOS device instance
ios_device = None

def initialize_device():
    """Initialize iOS device with proper error handling."""
    global ios_device
    
    try:
        print("🚀 Initializing iOS MCP Server...")
        print(f"🔌 Connection mode: {'USB' if args.usb else 'Network'}")
        if args.device:
            print(f"🎯 Target device: {args.device}")
        elif args.simulator:
            print("📱 Target: iOS Simulator")
        else:
            print("📱 Target: Auto-detect device")
        
        ios_device = IOSDevice(
            device=args.device,
            simulator=args.simulator,
            usb=args.usb,
            port=args.port,
            auto_setup=True
        )
        
        # Print device info
        device_info = ios_device.get_device_info()
        if device_info.get('connected'):
            print("✅ iOS MCP Server ready!")
            return True
        else:
            print("❌ Device initialization failed")
            return False
            
    except ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("\n💡 Quick fixes to try:")
        print("1. Ensure your iOS device/simulator is connected")
        print("2. Check that WebDriverAgent is installed and running")
        print("3. Verify device is trusted and unlocked")
        print("4. See README.md for detailed setup instructions")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error during initialization: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def safe_device_operation(operation_name: str, operation_func, *args, **kwargs):
    """Safely execute device operations with error handling."""
    try:
        if not ios_device:
            return f"❌ Device not initialized. Please restart the server."
        
        return operation_func(*args, **kwargs)
        
    except ConnectionError as e:
        return f"❌ Connection lost during {operation_name}: {e}. Please check device connection."
    except Exception as e:
        return f"❌ Error during {operation_name}: {e}"

@mcp.tool(name='Click-Tool', description='Tap on specific coordinates')
def click_tool(x: int, y: int):
    """Tap on specific coordinates on the iOS device screen."""
    def perform_tap():
        try:
            ios_device.tap(x, y)
            return f'✅ Successfully tapped on coordinates ({x}, {y})'
        except Exception as e:
            return f'❌ Failed to tap on coordinates ({x}, {y}): {str(e)}'
    
    return safe_device_operation("tap", perform_tap)

@mcp.tool('State-Tool', description='Get the state of the iOS device. Optionally includes visual screenshot when use_vision=True.')
def state_tool(use_vision: bool = False):
    """Get the current state of the iOS device with optional screenshot."""
    def get_state():
        device_state = ios_device.get_state(use_vision=use_vision)
        result = [device_state.tree_state.to_string()]
        if use_vision and device_state.screenshot:
            result.append(Image(data=device_state.screenshot, format='PNG'))
        return result
    
    return safe_device_operation("get_state", get_state)

@mcp.tool(name='Long-Press-Tool', description='Long press on specific coordinates')
def long_press_tool(x: int, y: int, duration: float = 1.0):
    """Long press on specific coordinates for given duration."""
    return safe_device_operation(
        "long_press",
        lambda: (ios_device.long_press(x, y, duration=duration), f'Long pressed on ({x},{y}) for {duration}s')[1]
    )

@mcp.tool(name='Swipe-Tool', description='Swipe between coordinates')
def swipe_tool(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5):
    """Swipe from one coordinate to another."""
    ios_device.swipe(x1, y1, x2, y2, duration=duration)
    return f'Swiped from ({x1},{y1}) to ({x2},{y2})'

@mcp.tool(name='Type-Tool', description='Type text on the device')
def type_tool(text: str, clear: bool = False):
    """Type text on the iOS device. Optionally clear existing text first."""
    ios_device.type_text(text, clear=clear)
    return f'Typed "{text}"'

@mcp.tool(name='Element-Tap-Tool', description='Tap on element by various selectors')
def element_tap_tool(selector: str, value: str, timeout: float = 10.0):
    """
    Tap on element using various selectors.
    Selector types: id, name, label, className, xpath, predicate
    """
    result = ios_device.tap_element(selector, value, timeout=timeout)
    return result

@mcp.tool(name='Element-Type-Tool', description='Type text in element by various selectors')
def element_type_tool(selector: str, value: str, text: str, clear: bool = True, timeout: float = 10.0):
    """
    Type text in element using various selectors.
    Selector types: id, name, label, className, xpath, predicate
    """
    result = ios_device.type_in_element(selector, value, text, clear=clear, timeout=timeout)
    return result

@mcp.tool(name='Home-Tool', description='Press home button')
def home_tool():
    """Press the home button to return to home screen."""
    ios_device.home()
    return 'Pressed home button'

@mcp.tool(name='Volume-Tool', description='Press volume buttons')
def volume_tool(direction: str):
    """
    Press volume buttons.
    Direction: up, down
    """
    ios_device.volume(direction)
    return f'Pressed volume {direction}'

@mcp.tool(name='Lock-Tool', description='Lock or unlock the device')
def lock_tool(action: str):
    """
    Lock or unlock the device.
    Action: lock, unlock
    """
    if action == 'lock':
        ios_device.lock()
        return 'Device locked'
    elif action == 'unlock':
        ios_device.unlock()
        return 'Device unlocked'
    else:
        return 'Invalid action. Use "lock" or "unlock"'

@mcp.tool(name='App-Control-Tool', description='Control app lifecycle')
def app_control_tool(action: str, bundle_id: str):
    """
    Control app lifecycle.
    Actions: launch, terminate, activate, state
    """
    result = ios_device.app_control(action, bundle_id)
    return result

@mcp.tool(name='Wait-Tool', description='Wait for specified duration')
def wait_tool(duration: float):
    """Wait for specified duration in seconds."""
    ios_device.wait(duration)
    return f'Waited for {duration} seconds'

@mcp.tool(name='Orientation-Tool', description='Get or set device orientation')
def orientation_tool(orientation: str = None):
    """
    Get current orientation or set new orientation.
    Orientations: portrait, landscape, landscape_left, landscape_right
    """
    if orientation:
        ios_device.set_orientation(orientation)
        return f'Set orientation to {orientation}'
    else:
        current = ios_device.get_orientation()
        return f'Current orientation: {current}'

@mcp.tool(name='Alert-Tool', description='Handle iOS alerts/dialogs')
def alert_tool(action: str, text: str = None):
    """
    Handle iOS alerts and dialogs.
    Actions: accept, dismiss, get_text, type_text
    """
    result = ios_device.handle_alert(action, text)
    return result

@mcp.tool(name='Scroll-Tool', description='Scroll in specified direction')
def scroll_tool(direction: str, distance: float = 0.5):
    """
    Scroll in specified direction.
    Directions: up, down, left, right
    Distance: 0.1 to 1.0 (percentage of screen)
    """
    ios_device.scroll(direction, distance)
    return f'Scrolled {direction} with distance {distance}'

@mcp.tool(name='Element-Wait-Tool', description='Wait for element to appear')
def element_wait_tool(selector: str, value: str, timeout: float = 10.0):
    """
    Wait for element to appear using various selectors.
    Returns True if element appears, False if timeout.
    """
    result = ios_device.wait_for_element(selector, value, timeout=timeout)
    return f'Element {"found" if result else "not found"} within {timeout}s'

if __name__ == '__main__':
    # Initialize device before starting server
    if not initialize_device():
        print("\n❌ Failed to initialize iOS device. Exiting...")
        sys.exit(1)
    
    print("\n🎯 Starting MCP server...")
    mcp.run()