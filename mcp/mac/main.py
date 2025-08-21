#!/usr/bin/env python3
"""
Mac MCP Server

A Model Context Protocol server for macOS automation and system control.
Provides tools for native Mac application control, system management, file operations,
and AppleScript automation similar to Android/iOS MCP servers.
"""

from mcp.server.fastmcp import FastMCP, Image
from contextlib import asynccontextmanager
from argparse import ArgumentParser
from src.mac import MacDevice
from textwrap import dedent
import asyncio


parser = ArgumentParser()
parser.add_argument('--device-name', type=str, help='Mac device name for identification')
parser.add_argument('--enable-accessibility', action='store_true', help='Enable accessibility features for automation')
parser.add_argument('--safe-mode', action='store_true', help='Run in safe mode with restricted system operations')
parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
args = parser.parse_args()

instructions = dedent('''
Mac MCP server provides tools for comprehensive macOS automation and system control.
Enables native Mac application control, file operations, system management,
and AppleScript automation for complete desktop automation workflows.
''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    await asyncio.sleep(1)  # Simulate startup latency
    yield

mcp = FastMCP(name="Mac-MCP", instructions=instructions)

# Initialize Mac device
mac_device = MacDevice(
    device_name=args.device_name or "Local Mac",
    enable_accessibility=args.enable_accessibility,
    safe_mode=args.safe_mode,
    log_level=args.log_level
)

@mcp.tool(name='System-Info-Tool', description='Get comprehensive system information')
def system_info_tool():
    """Get comprehensive Mac system information."""
    info = mac_device.get_system_info()
    return info

@mcp.tool('State-Tool', description='Get the current state of the Mac desktop. Optionally includes visual screenshot when use_vision=True.')
def state_tool(use_vision: bool = False):
    """Get the current state of the Mac desktop with optional screenshot."""
    mac_state = mac_device.get_state(use_vision=use_vision)
    result = [mac_state.desktop_state.to_string()]
    if use_vision and mac_state.screenshot:
        result.append(Image(data=mac_state.screenshot, format='PNG'))
    return result

@mcp.tool(name='Click-Tool', description='Click on specific coordinates on the desktop')
def click_tool(x: int, y: int, click_type: str = 'left', double_click: bool = False):
    """
    Click on specific coordinates on the Mac desktop.
    Click types: left, right, middle
    """
    result = mac_device.click(x, y, click_type=click_type, double_click=double_click)
    return result

@mcp.tool(name='Element-Click-Tool', description='Click on UI elements by accessibility properties')
def element_click_tool(element_type: str, identifier: str, app_name: str = None, timeout: float = 10.0):
    """
    Click on UI elements using accessibility properties.
    Element types: button, menu, menuitem, checkbox, radiobutton, textfield, link, etc.
    """
    result = mac_device.click_element(element_type, identifier, app_name=app_name, timeout=timeout)
    return result

@mcp.tool(name='Type-Tool', description='Type text at current cursor position or coordinates')
def type_tool(text: str, x: int = None, y: int = None, clear: bool = False):
    """Type text at current cursor position or click coordinates first."""
    result = mac_device.type_text(text, x=x, y=y, clear=clear)
    return result

@mcp.tool(name='Element-Type-Tool', description='Type text in specific UI elements')
def element_type_tool(element_type: str, identifier: str, text: str, app_name: str = None, clear: bool = True, timeout: float = 10.0):
    """Type text in specific UI elements using accessibility properties."""
    result = mac_device.type_in_element(element_type, identifier, text, app_name=app_name, clear=clear, timeout=timeout)
    return result

@mcp.tool(name='Key-Press-Tool', description='Send keyboard shortcuts and key combinations')
def key_press_tool(keys: str, modifier_keys: str = None):
    """
    Send keyboard shortcuts and key combinations.
    Keys: any keyboard key (a-z, 0-9, space, return, tab, escape, etc.)
    Modifier keys: cmd, shift, ctrl, alt, fn (comma-separated)
    """
    result = mac_device.send_keys(keys, modifier_keys=modifier_keys)
    return result

@mcp.tool(name='Mouse-Drag-Tool', description='Perform mouse drag operations')
def mouse_drag_tool(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0):
    """Perform mouse drag from start coordinates to end coordinates."""
    result = mac_device.drag(start_x, start_y, end_x, end_y, duration=duration)
    return result

@mcp.tool(name='Scroll-Tool', description='Scroll in specified direction')
def scroll_tool(direction: str, amount: int = 5, x: int = None, y: int = None):
    """
    Scroll in specified direction.
    Directions: up, down, left, right
    Amount: number of scroll units
    """
    result = mac_device.scroll(direction, amount=amount, x=x, y=y)
    return result

@mcp.tool(name='App-Control-Tool', description='Control Mac applications')
def app_control_tool(action: str, app_name: str, window_title: str = None):
    """
    Control Mac applications.
    Actions: launch, quit, activate, hide, minimize, maximize, close
    """
    result = mac_device.app_control(action, app_name, window_title=window_title)
    return result

@mcp.tool(name='App-List-Tool', description='List running applications and their windows')
def app_list_tool(running_only: bool = True):
    """List running applications and their windows."""
    result = mac_device.list_applications(running_only=running_only)
    return result

@mcp.tool(name='Window-Control-Tool', description='Control application windows')
def window_control_tool(action: str, window_title: str = None, app_name: str = None, x: int = None, y: int = None, width: int = None, height: int = None):
    """
    Control application windows.
    Actions: activate, minimize, maximize, close, resize, move, fullscreen
    """
    result = mac_device.window_control(action, window_title=window_title, app_name=app_name, x=x, y=y, width=width, height=height)
    return result

@mcp.tool(name='AppleScript-Tool', description='Execute AppleScript commands')
def applescript_tool(script: str, timeout: float = 30.0):
    """Execute AppleScript commands for advanced Mac automation."""
    result = mac_device.execute_applescript(script, timeout=timeout)
    return result

@mcp.tool(name='Shell-Command-Tool', description='Execute shell commands with safety restrictions')
def shell_command_tool(command: str, timeout: float = 30.0, safe_mode: bool = True):
    """Execute shell commands with optional safety restrictions."""
    result = mac_device.execute_shell_command(command, timeout=timeout, safe_mode=safe_mode)
    return result

@mcp.tool(name='File-Operations-Tool', description='Perform file and directory operations')
def file_operations_tool(action: str, source_path: str, destination_path: str = None, recursive: bool = False):
    """
    Perform file and directory operations.
    Actions: copy, move, delete, create_dir, list, exists, info
    """
    result = mac_device.file_operations(action, source_path, destination_path=destination_path, recursive=recursive)
    return result

@mcp.tool(name='Finder-Tool', description='Control Finder application and file browser')
def finder_tool(action: str, path: str = None, view_style: str = None):
    """
    Control Finder application and file browser.
    Actions: open, new_window, go_to, set_view, get_selection, refresh
    View styles: icon, list, column, gallery
    """
    result = mac_device.finder_control(action, path=path, view_style=view_style)
    return result

@mcp.tool(name='Clipboard-Tool', description='Manage system clipboard')
def clipboard_tool(action: str, content: str = None, content_type: str = 'text'):
    """
    Manage system clipboard.
    Actions: get, set, clear
    Content types: text, image, file
    """
    result = mac_device.clipboard_management(action, content=content, content_type=content_type)
    return result

@mcp.tool(name='Notification-Tool', description='Send and manage Mac notifications')
def notification_tool(action: str, title: str = None, message: str = None, app_name: str = None):
    """
    Send and manage Mac notifications.
    Actions: send, clear, list
    """
    result = mac_device.notification_management(action, title=title, message=message, app_name=app_name)
    return result

@mcp.tool(name='System-Preferences-Tool', description='Control System Preferences/Settings')
def system_preferences_tool(action: str, pane: str = None, setting: str = None, value: str = None):
    """
    Control System Preferences/Settings.
    Actions: open, get_setting, set_setting, list_panes
    """
    result = mac_device.system_preferences_control(action, pane=pane, setting=setting, value=value)
    return result

@mcp.tool(name='Dock-Tool', description='Control Mac Dock')
def dock_tool(action: str, app_name: str = None, position: str = None):
    """
    Control Mac Dock.
    Actions: add_app, remove_app, set_position, set_autohide, get_apps
    Positions: bottom, left, right
    """
    result = mac_device.dock_control(action, app_name=app_name, position=position)
    return result

@mcp.tool(name='Menu-Bar-Tool', description='Interact with menu bar and menu items')
def menu_bar_tool(action: str, menu_name: str = None, item_name: str = None, app_name: str = None):
    """
    Interact with menu bar and menu items.
    Actions: click_menu, get_menus, get_menu_items
    """
    result = mac_device.menu_bar_interaction(action, menu_name=menu_name, item_name=item_name, app_name=app_name)
    return result

@mcp.tool(name='Screenshot-Tool', description='Take screenshots of desktop or specific areas')
def screenshot_tool(save_path: str = None, x: int = None, y: int = None, width: int = None, height: int = None, window_id: str = None):
    """
    Take screenshots of desktop or specific areas.
    Coordinates define capture region, window_id captures specific window.
    """
    result = mac_device.take_screenshot(save_path=save_path, x=x, y=y, width=width, height=height, window_id=window_id)
    return result

@mcp.tool(name='Process-Tool', description='Manage system processes')
def process_tool(action: str, process_name: str = None, pid: int = None):
    """
    Manage system processes.
    Actions: list, kill, info, cpu_usage, memory_usage
    """
    result = mac_device.process_management(action, process_name=process_name, pid=pid)
    return result

@mcp.tool(name='Network-Tool', description='Get network information and control network settings')
def network_tool(action: str, interface: str = None, setting: str = None, value: str = None):
    """
    Get network information and control network settings.
    Actions: list_interfaces, get_info, wifi_scan, connect_wifi, disconnect_wifi
    """
    result = mac_device.network_management(action, interface=interface, setting=setting, value=value)
    return result

@mcp.tool(name='Volume-Tool', description='Control system volume and audio')
def volume_tool(action: str, level: int = None, device: str = None):
    """
    Control system volume and audio.
    Actions: get_volume, set_volume, mute, unmute, list_devices
    Level: 0-100 for volume level
    """
    result = mac_device.volume_control(action, level=level, device=device)
    return result

@mcp.tool(name='Display-Tool', description='Control display settings and resolution')
def display_tool(action: str, display_id: int = None, resolution: str = None, brightness: int = None):
    """
    Control display settings and resolution.
    Actions: list_displays, get_resolution, set_resolution, get_brightness, set_brightness
    Resolution format: WIDTHxHEIGHT (e.g., 1920x1080)
    Brightness: 0-100
    """
    result = mac_device.display_control(action, display_id=display_id, resolution=resolution, brightness=brightness)
    return result

@mcp.tool(name='Accessibility-Tool', description='Control accessibility features and settings')
def accessibility_tool(action: str, feature: str = None, enabled: bool = None):
    """
    Control accessibility features and settings.
    Actions: list_features, get_feature, set_feature, check_permissions
    Features: voice_over, zoom, switch_control, etc.
    """
    result = mac_device.accessibility_control(action, feature=feature, enabled=enabled)
    return result

@mcp.tool(name='Wait-Tool', description='Wait for specified duration or conditions')
def wait_tool(duration: float = None, condition: str = None, element_type: str = None, identifier: str = None, timeout: float = 30.0):
    """
    Wait for specified duration or conditions.
    Conditions: element_appears, element_disappears, app_launches, app_quits
    """
    result = mac_device.wait(duration=duration, condition=condition, element_type=element_type, identifier=identifier, timeout=timeout)
    return result

if __name__ == '__main__':
    mcp.run()