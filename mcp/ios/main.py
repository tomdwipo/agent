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
''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    await asyncio.sleep(1)  # Simulate startup latency
    yield

mcp = FastMCP(name="iOS-MCP", instructions=instructions)

# Initialize iOS device
ios_device = IOSDevice(
    device=args.device,
    simulator=args.simulator,
    usb=args.usb,
    port=args.port
)

@mcp.tool(name='Click-Tool', description='Tap on specific coordinates')
def click_tool(x: int, y: int):
    """Tap on specific coordinates on the iOS device screen."""
    ios_device.tap(x, y)
    return f'Tapped on ({x},{y})'

@mcp.tool('State-Tool', description='Get the state of the iOS device. Optionally includes visual screenshot when use_vision=True.')
def state_tool(use_vision: bool = False):
    """Get the current state of the iOS device with optional screenshot."""
    device_state = ios_device.get_state(use_vision=use_vision)
    result = [device_state.tree_state.to_string()]
    if use_vision and device_state.screenshot:
        result.append(Image(data=device_state.screenshot, format='PNG'))
    return result

@mcp.tool(name='Long-Press-Tool', description='Long press on specific coordinates')
def long_press_tool(x: int, y: int, duration: float = 1.0):
    """Long press on specific coordinates for given duration."""
    ios_device.long_press(x, y, duration=duration)
    return f'Long pressed on ({x},{y}) for {duration}s'

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
    mcp.run()