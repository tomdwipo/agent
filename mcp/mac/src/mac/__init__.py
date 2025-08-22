"""
Mac Device Management Module

Handles Mac system connections, automation operations, and state management
using PyObjC, AppleScript, and native macOS APIs for comprehensive control.
"""

import os
import sys
import time
import json
import subprocess
import logging
from typing import Optional, Union, Dict, Any, List, Tuple
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

try:
    # PyObjC imports for native Mac automation
    import Cocoa
    import Quartz
    import AppKit
    from AppKit import NSWorkspace, NSApplication, NSScreen, NSEvent
    from Cocoa import NSAutoreleasePool, NSPasteboard, NSStringPboardType
    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
    from ApplicationServices import AXUIElementCreateApplication, AXUIElementCreateSystemWide
    import CoreGraphics as CG
    PYOBJC_AVAILABLE = True
except ImportError:
    PYOBJC_AVAILABLE = False
    logging.warning("PyObjC not available. Some Mac automation features will be limited.")

from src.mac.views import MacState
from src.page import PageTree


class MacDevice:
    """Main Mac device management class."""
    
    def __init__(
        self,
        device_name: str = "Local Mac",
        enable_accessibility: bool = False,
        safe_mode: bool = False,
        log_level: str = "INFO"
    ):
        """
        Initialize Mac device connection.
        
        Args:
            device_name: Mac device name for identification
            enable_accessibility: Enable accessibility features for automation
            safe_mode: Run in safe mode with restricted system operations
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.device_name = device_name
        self.enable_accessibility = enable_accessibility
        self.safe_mode = safe_mode
        
        # Setup logging
        logging.basicConfig(level=getattr(logging, log_level.upper()))
        self.logger = logging.getLogger(__name__)
        
        # Initialize system connections
        self._initialize_system()
        
        # Check accessibility permissions
        if enable_accessibility:
            self._check_accessibility_permissions()
    
    def _initialize_system(self):
        """Initialize Mac system connections and check requirements."""
        try:
            if not PYOBJC_AVAILABLE:
                self.logger.warning("PyObjC not available. Using fallback methods.")
            
            # Check if running on macOS
            if sys.platform != 'darwin':
                raise RuntimeError("Mac MCP server can only run on macOS")
            
            # Initialize NSApplication for GUI interactions
            if PYOBJC_AVAILABLE:
                try:
                    self.app = NSApplication.sharedApplication()
                    self.workspace = NSWorkspace.sharedWorkspace()
                    self.pasteboard = NSPasteboard.generalPasteboard()
                except Exception as e:
                    self.logger.warning(f"Failed to initialize NSApplication: {e}")
                    self.app = None
                    self.workspace = None
                    self.pasteboard = None
            
            self.logger.info(f"Mac device '{self.device_name}' initialized successfully")
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Mac device: {e}")
    
    def _check_accessibility_permissions(self):
        """Check and request accessibility permissions."""
        try:
            # Check if accessibility is enabled
            import subprocess
            result = subprocess.run([
                'osascript', '-e',
                'tell application "System Events" to get exists of process "Finder"'
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.warning("Accessibility permissions not granted. Some features may not work.")
                return False
            
            self.logger.info("Accessibility permissions verified")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to check accessibility permissions: {e}")
            return False
    
    def get_state(self, use_vision: bool = False) -> 'MacState':
        """
        Get current Mac desktop state with optional screenshot.
        
        Args:
            use_vision: Whether to include annotated screenshot
            
        Returns:
            MacState object containing desktop state and optional screenshot
        """
        try:
            page_tree = PageTree(self)
            desktop_state = page_tree.get_state()
            
            if use_vision:
                elements = desktop_state.interactive_elements
                annotated_screenshot = page_tree.annotated_screenshot(elements=elements, scale=1.0)
                screenshot = self.screenshot_in_bytes(annotated_screenshot)
            else:
                screenshot = None
                
            return MacState(desktop_state=desktop_state, screenshot=screenshot)
            
        except Exception as e:
            raise RuntimeError(f"Failed to get Mac state: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive Mac system information."""
        try:
            import platform
            import psutil
            
            # Basic system info
            info = {
                'device_name': self.device_name,
                'system': platform.system(),
                'version': platform.mac_ver()[0],
                'machine': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
            }
            
            # Hardware info
            try:
                info.update({
                    'cpu_count': psutil.cpu_count(),
                    'cpu_usage': psutil.cpu_percent(interval=1),
                    'memory_total': psutil.virtual_memory().total,
                    'memory_available': psutil.virtual_memory().available,
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent,
                })
            except Exception as e:
                self.logger.warning(f"Failed to get hardware info: {e}")
            
            # Display info
            if PYOBJC_AVAILABLE:
                try:
                    screens = NSScreen.screens()
                    displays = []
                    for i, screen in enumerate(screens):
                        frame = screen.frame()
                        displays.append({
                            'id': i,
                            'width': int(frame.size.width),
                            'height': int(frame.size.height),
                            'scale': screen.backingScaleFactor()
                        })
                    info['displays'] = displays
                except Exception as e:
                    self.logger.warning(f"Failed to get display info: {e}")
            
            # Running applications
            try:
                apps = self.list_applications(running_only=True)
                info['running_apps'] = len(apps) if isinstance(apps, list) else 0
            except Exception:
                pass
            
            return info
            
        except Exception as e:
            return {'error': f"Failed to get system info: {e}"}
    
    def get_screenshot(self, scale: float = 1.0) -> Image.Image:
        """
        Take screenshot of the Mac desktop.
        
        Args:
            scale: Scale factor for the image (default: 1.0)
            
        Returns:
            PIL Image object
        """
        try:
            if PYOBJC_AVAILABLE:
                # Use Quartz for high-quality screenshots
                region = Quartz.CGRectInfinite
                image = Quartz.CGWindowListCreateImage(
                    region,
                    Quartz.kCGWindowListOptionOnScreenOnly,
                    Quartz.kCGNullWindowID,
                    Quartz.kCGWindowImageDefault
                )
                
                if image:
                    width = Quartz.CGImageGetWidth(image)
                    height = Quartz.CGImageGetHeight(image)
                    
                    # Convert to PIL Image
                    bytes_per_row = Quartz.CGImageGetBytesPerRow(image)
                    data_provider = Quartz.CGImageGetDataProvider(image)
                    data = Quartz.CGDataProviderCopyData(data_provider)
                    
                    # Create PIL Image from raw data
                    pil_image = Image.frombuffer(
                        "RGBA", (width, height), 
                        data, "raw", "BGRA", bytes_per_row, 1
                    )
                    
                    # Convert RGBA to RGB
                    pil_image = pil_image.convert('RGB')
                    
                    # Scale image if needed
                    if scale != 1.0:
                        size = (int(width * scale), int(height * scale))
                        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
                    
                    return pil_image
            
            # Fallback to screencapture command
            temp_file = "/tmp/mac_mcp_screenshot.png"
            result = subprocess.run([
                'screencapture', '-x', temp_file
            ], capture_output=True)
            
            if result.returncode == 0 and os.path.exists(temp_file):
                screenshot = Image.open(temp_file)
                os.remove(temp_file)  # Clean up
                
                # Scale image if needed
                if scale != 1.0:
                    size = (int(screenshot.width * scale), int(screenshot.height * scale))
                    screenshot = screenshot.resize(size, Image.Resampling.LANCZOS)
                
                return screenshot
            else:
                raise RuntimeError("Failed to capture screenshot")
                
        except Exception as e:
            raise RuntimeError(f"Failed to take screenshot: {e}")
    
    def screenshot_in_bytes(self, screenshot: Image.Image) -> bytes:
        """Convert PIL Image to bytes."""
        try:
            if screenshot is None:
                raise ValueError("Screenshot is None")
            
            io = BytesIO()
            screenshot.save(io, format='PNG')
            bytes_data = io.getvalue()
            
            if len(bytes_data) == 0:
                raise ValueError("Screenshot conversion resulted in empty bytes")
            
            return bytes_data
            
        except Exception as e:
            raise RuntimeError(f"Failed to convert screenshot to bytes: {e}")
    
    def click(self, x: int, y: int, click_type: str = 'left', double_click: bool = False) -> str:
        """Click on specific coordinates on the Mac desktop."""
        try:
            if PYOBJC_AVAILABLE:
                # Use Quartz for precise clicking
                if click_type == 'left':
                    if double_click:
                        # Double click
                        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                            None, CG.kCGEventLeftMouseDown, (x, y), CG.kCGMouseButtonLeft))
                        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                            None, CG.kCGEventLeftMouseUp, (x, y), CG.kCGMouseButtonLeft))
                        time.sleep(0.05)
                        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                            None, CG.kCGEventLeftMouseDown, (x, y), CG.kCGMouseButtonLeft))
                        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                            None, CG.kCGEventLeftMouseUp, (x, y), CG.kCGMouseButtonLeft))
                    else:
                        # Single click
                        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                            None, CG.kCGEventLeftMouseDown, (x, y), CG.kCGMouseButtonLeft))
                        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                            None, CG.kCGEventLeftMouseUp, (x, y), CG.kCGMouseButtonLeft))
                
                elif click_type == 'right':
                    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                        None, CG.kCGEventRightMouseDown, (x, y), CG.kCGMouseButtonRight))
                    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                        None, CG.kCGEventRightMouseUp, (x, y), CG.kCGMouseButtonRight))
                
                return f"{'Double-c' if double_click else 'C'}licked {click_type} at ({x}, {y})"
            
            # Fallback using AppleScript
            click_script = f'''
            tell application "System Events"
                set the screen_coordinates to {{{x}, {y}}}
                click at screen_coordinates
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', click_script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Clicked at ({x}, {y}) using AppleScript"
            else:
                return f"Failed to click: {result.stderr}"
                
        except Exception as e:
            return f"Error clicking: {e}"
    
    def click_element(self, element_type: str, identifier: str, app_name: str = None, timeout: float = 10.0) -> str:
        """Click on UI elements using accessibility properties."""
        try:
            if not self.enable_accessibility:
                return "Accessibility features not enabled. Use --enable-accessibility flag."
            
            # Use AppleScript for element clicking
            if app_name:
                script = f'''
                tell application "{app_name}"
                    activate
                    tell application "System Events"
                        tell process "{app_name}"
                            click {element_type} "{identifier}"
                        end tell
                    end tell
                end tell
                '''
            else:
                script = f'''
                tell application "System Events"
                    click {element_type} "{identifier}"
                end tell
                '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                return f"Clicked {element_type} '{identifier}'{f' in {app_name}' if app_name else ''}"
            else:
                return f"Failed to click element: {result.stderr}"
                
        except Exception as e:
            return f"Error clicking element: {e}"
    
    def type_text(self, text: str, x: int = None, y: int = None, clear: bool = False) -> str:
        """Type text at current cursor position or click coordinates first."""
        try:
            # Click at coordinates if provided
            if x is not None and y is not None:
                self.click(x, y)
                time.sleep(0.2)
            
            if clear:
                # Clear existing text with Cmd+A
                self.send_keys('a', modifier_keys='cmd')
                time.sleep(0.1)
            
            if PYOBJC_AVAILABLE:
                # Use CGEvent for typing
                for char in text:
                    if char == '\n':
                        # Handle newline
                        key_event = CG.CGEventCreateKeyboardEvent(None, 36, True)  # Return key
                        CG.CGEventPost(CG.kCGHIDEventTap, key_event)
                        key_event = CG.CGEventCreateKeyboardEvent(None, 36, False)
                        CG.CGEventPost(CG.kCGHIDEventTap, key_event)
                    else:
                        # Regular character
                        unicode_string = CG.CFStringCreateWithCharacters(None, [ord(char)], 1)
                        key_event = CG.CGEventCreateKeyboardEvent(None, 0, True)
                        CG.CGEventKeyboardSetUnicodeString(key_event, 1, unicode_string)
                        CG.CGEventPost(CG.kCGHIDEventTap, key_event)
                        
                        key_event = CG.CGEventCreateKeyboardEvent(None, 0, False)
                        CG.CGEventKeyboardSetUnicodeString(key_event, 1, unicode_string)
                        CG.CGEventPost(CG.kCGHIDEventTap, key_event)
                    
                    time.sleep(0.01)  # Small delay between characters
                
                return f"Typed '{text}'"
            
            # Fallback using AppleScript
            script = f'''
            tell application "System Events"
                keystroke "{text}"
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Typed '{text}' using AppleScript"
            else:
                return f"Failed to type text: {result.stderr}"
                
        except Exception as e:
            return f"Error typing text: {e}"
    
    def type_in_element(self, element_type: str, identifier: str, text: str, app_name: str = None, clear: bool = True, timeout: float = 10.0) -> str:
        """Type text in specific UI elements using accessibility properties."""
        try:
            if not self.enable_accessibility:
                return "Accessibility features not enabled. Use --enable-accessibility flag."
            
            # Click on element first
            click_result = self.click_element(element_type, identifier, app_name=app_name, timeout=timeout)
            if "Failed" in click_result or "Error" in click_result:
                return click_result
            
            time.sleep(0.2)
            
            # Clear if requested
            if clear:
                self.send_keys('a', modifier_keys='cmd')
                time.sleep(0.1)
            
            # Type the text
            type_result = self.type_text(text)
            
            return f"Typed '{text}' in {element_type} '{identifier}'{f' in {app_name}' if app_name else ''}"
            
        except Exception as e:
            return f"Error typing in element: {e}"
    
    def send_keys(self, keys: str, modifier_keys: str = None) -> str:
        """Send keyboard shortcuts and key combinations."""
        try:
            # Build AppleScript for key combinations
            modifiers = []
            if modifier_keys:
                for mod in modifier_keys.split(','):
                    mod = mod.strip().lower()
                    if mod in ['cmd', 'command']:
                        modifiers.append('command down')
                    elif mod in ['shift']:
                        modifiers.append('shift down')
                    elif mod in ['ctrl', 'control']:
                        modifiers.append('control down')
                    elif mod in ['alt', 'option']:
                        modifiers.append('option down')
                    elif mod in ['fn', 'function']:
                        modifiers.append('function down')
            
            # Special key mappings
            key_map = {
                'return': 'return',
                'enter': 'return',
                'tab': 'tab',
                'space': 'space',
                'escape': 'escape',
                'esc': 'escape',
                'delete': 'delete',
                'backspace': 'delete',
                'up': 'up arrow',
                'down': 'down arrow',
                'left': 'left arrow',
                'right': 'right arrow',
                'home': 'home',
                'end': 'end',
                'pageup': 'page up',
                'pagedown': 'page down',
                'f1': 'F1', 'f2': 'F2', 'f3': 'F3', 'f4': 'F4',
                'f5': 'F5', 'f6': 'F6', 'f7': 'F7', 'f8': 'F8',
                'f9': 'F9', 'f10': 'F10', 'f11': 'F11', 'f12': 'F12'
            }
            
            key = key_map.get(keys.lower(), keys)
            
            if modifiers:
                modifier_str = ' using {' + ', '.join(modifiers) + '}'
            else:
                modifier_str = ''
            
            script = f'''
            tell application "System Events"
                key code (key code of "{key}"){modifier_str}
            end tell
            '''
            
            # For simple keystroke without modifiers
            if not modifiers:
                script = f'''
                tell application "System Events"
                    keystroke "{key}"
                end tell
                '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                modifier_desc = f" with {modifier_keys}" if modifier_keys else ""
                return f"Sent key '{keys}'{modifier_desc}"
            else:
                return f"Failed to send keys: {result.stderr}"
                
        except Exception as e:
            return f"Error sending keys: {e}"
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> str:
        """Perform mouse drag from start coordinates to end coordinates."""
        try:
            if PYOBJC_AVAILABLE:
                # Calculate intermediate points for smooth drag
                steps = max(int(duration * 60), 10)  # 60 FPS
                dx = (end_x - start_x) / steps
                dy = (end_y - start_y) / steps
                
                # Start drag
                CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                    None, CG.kCGEventLeftMouseDown, (start_x, start_y), CG.kCGMouseButtonLeft))
                
                # Intermediate points
                for i in range(1, steps):
                    x = start_x + dx * i
                    y = start_y + dy * i
                    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                        None, CG.kCGEventLeftMouseDragged, (x, y), CG.kCGMouseButtonLeft))
                    time.sleep(duration / steps)
                
                # End drag
                CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                    None, CG.kCGEventLeftMouseUp, (end_x, end_y), CG.kCGMouseButtonLeft))
                
                return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
            
            # Fallback using AppleScript (less smooth)
            script = f'''
            tell application "System Events"
                set startPoint to {{{start_x}, {start_y}}}
                set endPoint to {{{end_x}, {end_y}}}
                
                -- Simulate drag
                tell me to do shell script "cliclick -r m:" & {start_x} & "," & {start_y}
                tell me to do shell script "cliclick -r dd:" & {start_x} & "," & {start_y}
                tell me to do shell script "cliclick -r m:" & {end_x} & "," & {end_y}
                tell me to do shell script "cliclick -r du:" & {end_x} & "," & {end_y}
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y}) using AppleScript"
            else:
                return f"Failed to drag: {result.stderr}"
                
        except Exception as e:
            return f"Error dragging: {e}"
    
    def scroll(self, direction: str, amount: int = 5, x: int = None, y: int = None) -> str:
        """Scroll in specified direction."""
        try:
            # Move mouse to position if specified
            if x is not None and y is not None:
                if PYOBJC_AVAILABLE:
                    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
                        None, CG.kCGEventMouseMoved, (x, y), 0))
            
            if PYOBJC_AVAILABLE:
                # Use CGEvent for scrolling
                if direction.lower() == 'up':
                    scroll_event = CG.CGEventCreateScrollWheelEvent(None, CG.kCGScrollEventUnitLine, 1, amount)
                elif direction.lower() == 'down':
                    scroll_event = CG.CGEventCreateScrollWheelEvent(None, CG.kCGScrollEventUnitLine, 1, -amount)
                elif direction.lower() == 'left':
                    scroll_event = CG.CGEventCreateScrollWheelEvent(None, CG.kCGScrollEventUnitLine, 2, 0, -amount)
                elif direction.lower() == 'right':
                    scroll_event = CG.CGEventCreateScrollWheelEvent(None, CG.kCGScrollEventUnitLine, 2, 0, amount)
                else:
                    return f"Unsupported scroll direction: {direction}"
                
                CG.CGEventPost(CG.kCGHIDEventTap, scroll_event)
                return f"Scrolled {direction} by {amount} units"
            
            # Fallback using AppleScript
            script = f'''
            tell application "System Events"
                scroll {direction} {amount}
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Scrolled {direction} by {amount} units using AppleScript"
            else:
                return f"Failed to scroll: {result.stderr}"
                
        except Exception as e:
            return f"Error scrolling: {e}"
    
    def app_control(self, action: str, app_name: str, window_title: str = None) -> str:
        """Control Mac applications."""
        try:
            if action == 'launch':
                script = f'''
                tell application "{app_name}"
                    activate
                end tell
                '''
            
            elif action == 'quit':
                script = f'''
                tell application "{app_name}"
                    quit
                end tell
                '''
            
            elif action == 'activate':
                script = f'''
                tell application "{app_name}"
                    activate
                end tell
                '''
            
            elif action == 'hide':
                script = f'''
                tell application "System Events"
                    set visible of application process "{app_name}" to false
                end tell
                '''
            
            elif action == 'minimize':
                if window_title:
                    script = f'''
                    tell application "{app_name}"
                        set miniaturized of window "{window_title}" to true
                    end tell
                    '''
                else:
                    script = f'''
                    tell application "{app_name}"
                        set miniaturized of window 1 to true
                    end tell
                    '''
            
            elif action == 'maximize':
                if window_title:
                    script = f'''
                    tell application "{app_name}"
                        set bounds of window "{window_title}" to bounds of window of desktop
                    end tell
                    '''
                else:
                    script = f'''
                    tell application "{app_name}"
                        set bounds of window 1 to bounds of window of desktop
                    end tell
                    '''
            
            elif action == 'close':
                if window_title:
                    script = f'''
                    tell application "{app_name}"
                        close window "{window_title}"
                    end tell
                    '''
                else:
                    script = f'''
                    tell application "{app_name}"
                        close window 1
                    end tell
                    '''
            
            else:
                return f"Unsupported app action: {action}"
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Successfully {action}ed {app_name}{f' window {window_title}' if window_title else ''}"
            else:
                return f"Failed to {action} {app_name}: {result.stderr}"
                
        except Exception as e:
            return f"Error controlling app: {e}"
    
    def list_applications(self, running_only: bool = True) -> List[Dict[str, Any]]:
        """List running applications and their windows."""
        try:
            apps = []
            
            if PYOBJC_AVAILABLE and self.workspace:
                running_apps = self.workspace.runningApplications()
                
                for app in running_apps:
                    if not running_only or not app.isHidden():
                        app_info = {
                            'name': app.localizedName(),
                            'bundle_id': app.bundleIdentifier(),
                            'pid': app.processIdentifier(),
                            'active': app.isActive(),
                            'hidden': app.isHidden(),
                            'windows': []
                        }
                        
                        # Get window information
                        try:
                            window_list = CGWindowListCopyWindowInfo(
                                kCGWindowListOptionOnScreenOnly, kCGNullWindowID
                            )
                            
                            for window in window_list:
                                if window.get('kCGWindowOwnerPID') == app.processIdentifier():
                                    window_info = {
                                        'title': window.get('kCGWindowName', ''),
                                        'id': window.get('kCGWindowNumber'),
                                        'bounds': window.get('kCGWindowBounds', {})
                                    }
                                    app_info['windows'].append(window_info)
                        except Exception:
                            pass
                        
                        apps.append(app_info)
            
            else:
                # Fallback using ps command
                result = subprocess.run([
                    'ps', 'aux'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    for line in lines:
                        parts = line.split()
                        if len(parts) >= 11:
                            command = ' '.join(parts[10:])
                            if '.app' in command or not running_only:
                                apps.append({
                                    'name': parts[10],
                                    'pid': int(parts[1]),
                                    'command': command
                                })
            
            return apps
            
        except Exception as e:
            return [{'error': f"Failed to list applications: {e}"}]
    
    def window_control(self, action: str, window_title: str = None, app_name: str = None, x: int = None, y: int = None, width: int = None, height: int = None) -> str:
        """Control application windows."""
        try:
            if not app_name and not window_title:
                return "Either app_name or window_title must be specified"
            
            if action == 'activate':
                if app_name and window_title:
                    script = f'''
                    tell application "{app_name}"
                        activate
                        set index of window "{window_title}" to 1
                    end tell
                    '''
                elif app_name:
                    script = f'''
                    tell application "{app_name}"
                        activate
                    end tell
                    '''
                else:
                    return "App name required for activate action"
            
            elif action == 'resize':
                if not (width and height):
                    return "Width and height required for resize action"
                
                if app_name and window_title:
                    script = f'''
                    tell application "{app_name}"
                        set bounds of window "{window_title}" to {{0, 0, {width}, {height}}}
                    end tell
                    '''
                elif app_name:
                    script = f'''
                    tell application "{app_name}"
                        set bounds of window 1 to {{0, 0, {width}, {height}}}
                    end tell
                    '''
                else:
                    return "App name required for resize action"
            
            elif action == 'move':
                if not (x is not None and y is not None):
                    return "X and Y coordinates required for move action"
                
                end_x = x + (width or 800)
                end_y = y + (height or 600)
                
                if app_name and window_title:
                    script = f'''
                    tell application "{app_name}"
                        set bounds of window "{window_title}" to {{{x}, {y}, {end_x}, {end_y}}}
                    end tell
                    '''
                elif app_name:
                    script = f'''
                    tell application "{app_name}"
                        set bounds of window 1 to {{{x}, {y}, {end_x}, {end_y}}}
                    end tell
                    '''
                else:
                    return "App name required for move action"
            
            elif action in ['minimize', 'maximize', 'close']:
                # Reuse app_control logic
                return self.app_control(action, app_name, window_title=window_title)
            
            elif action == 'fullscreen':
                if app_name:
                    script = f'''
                    tell application "{app_name}"
                        activate
                        tell application "System Events"
                            tell process "{app_name}"
                                set value of attribute "AXFullScreen" of window 1 to true
                            end tell
                        end tell
                    end tell
                    '''
                else:
                    return "App name required for fullscreen action"
            
            else:
                return f"Unsupported window action: {action}"
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Successfully {action}ed window{f' {window_title}' if window_title else ''}{f' in {app_name}' if app_name else ''}"
            else:
                return f"Failed to {action} window: {result.stderr}"
                
        except Exception as e:
            return f"Error controlling window: {e}"
    
    def execute_applescript(self, script: str, timeout: float = 30.0) -> str:
        """Execute AppleScript commands for advanced Mac automation."""
        try:
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                return f"AppleScript executed successfully. Output: {result.stdout.strip()}"
            else:
                return f"AppleScript failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return f"AppleScript timed out after {timeout} seconds"
        except Exception as e:
            return f"Error executing AppleScript: {e}"
    
    def execute_shell_command(self, command: str, timeout: float = 30.0, safe_mode: bool = True) -> str:
        """Execute shell commands with optional safety restrictions."""
        try:
            if safe_mode or self.safe_mode:
                # List of dangerous commands to block in safe mode
                dangerous_commands = [
                    'rm', 'rmdir', 'del', 'format', 'fdisk',
                    'dd', 'mkfs', 'shutdown', 'reboot', 'halt',
                    'sudo', 'su', 'chmod 777', 'chown root'
                ]
                
                command_lower = command.lower()
                for dangerous in dangerous_commands:
                    if dangerous in command_lower:
                        return f"Command blocked in safe mode: {dangerous}"
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = []
            if result.stdout:
                output.append(f"STDOUT: {result.stdout.strip()}")
            if result.stderr:
                output.append(f"STDERR: {result.stderr.strip()}")
            
            status = "Success" if result.returncode == 0 else "Failed"
            output.append(f"Exit code: {result.returncode} ({status})")
            
            return "\n".join(output)
            
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout} seconds"
        except Exception as e:
            return f"Error executing command: {e}"
    
    def file_operations(self, action: str, source_path: str, destination_path: str = None, recursive: bool = False) -> str:
        """Perform file and directory operations."""
        try:
            import shutil
            
            source_path = os.path.expanduser(source_path)
            
            if action == 'copy':
                if not destination_path:
                    return "Destination path required for copy action"
                
                destination_path = os.path.expanduser(destination_path)
                
                if os.path.isdir(source_path):
                    if recursive:
                        shutil.copytree(source_path, destination_path)
                        return f"Directory copied from {source_path} to {destination_path}"
                    else:
                        return "Use recursive=True to copy directories"
                else:
                    shutil.copy2(source_path, destination_path)
                    return f"File copied from {source_path} to {destination_path}"
            
            elif action == 'move':
                if not destination_path:
                    return "Destination path required for move action"
                
                destination_path = os.path.expanduser(destination_path)
                shutil.move(source_path, destination_path)
                return f"Moved from {source_path} to {destination_path}"
            
            elif action == 'delete':
                if self.safe_mode:
                    return "Delete operations disabled in safe mode"
                
                if os.path.isdir(source_path):
                    if recursive:
                        shutil.rmtree(source_path)
                        return f"Directory deleted: {source_path}"
                    else:
                        os.rmdir(source_path)
                        return f"Empty directory deleted: {source_path}"
                else:
                    os.remove(source_path)
                    return f"File deleted: {source_path}"
            
            elif action == 'create_dir':
                os.makedirs(source_path, exist_ok=True)
                return f"Directory created: {source_path}"
            
            elif action == 'list':
                if os.path.isdir(source_path):
                    items = os.listdir(source_path)
                    return f"Contents of {source_path}: {', '.join(items)}"
                else:
                    return f"Path is not a directory: {source_path}"
            
            elif action == 'exists':
                exists = os.path.exists(source_path)
                return f"Path exists: {exists}"
            
            elif action == 'info':
                if os.path.exists(source_path):
                    stat = os.stat(source_path)
                    import time
                    info = {
                        'path': source_path,
                        'size': stat.st_size,
                        'modified': time.ctime(stat.st_mtime),
                        'created': time.ctime(stat.st_ctime),
                        'is_file': os.path.isfile(source_path),
                        'is_dir': os.path.isdir(source_path),
                        'permissions': oct(stat.st_mode)[-3:]
                    }
                    return json.dumps(info, indent=2)
                else:
                    return f"Path does not exist: {source_path}"
            
            else:
                return f"Unsupported file operation: {action}"
                
        except Exception as e:
            return f"Error performing file operation: {e}"
    
    def finder_control(self, action: str, path: str = None, view_style: str = None) -> str:
        """Control Finder application and file browser."""
        try:
            if action == 'open':
                if path:
                    path = os.path.expanduser(path)
                    script = f'''
                    tell application "Finder"
                        activate
                        open folder POSIX file "{path}"
                    end tell
                    '''
                else:
                    script = '''
                    tell application "Finder"
                        activate
                    end tell
                    '''
            
            elif action == 'new_window':
                script = '''
                tell application "Finder"
                    activate
                    make new Finder window
                end tell
                '''
            
            elif action == 'go_to':
                if not path:
                    return "Path required for go_to action"
                
                path = os.path.expanduser(path)
                script = f'''
                tell application "Finder"
                    activate
                    set target of front window to folder POSIX file "{path}"
                end tell
                '''
            
            elif action == 'set_view':
                if not view_style:
                    return "View style required for set_view action"
                
                view_map = {
                    'icon': 'icon view',
                    'list': 'list view',
                    'column': 'column view',
                    'gallery': 'gallery view'
                }
                
                if view_style not in view_map:
                    return f"Unsupported view style: {view_style}. Use: {', '.join(view_map.keys())}"
                
                script = f'''
                tell application "Finder"
                    set current view of front window to {view_map[view_style]}
                end tell
                '''
            
            elif action == 'get_selection':
                script = '''
                tell application "Finder"
                    set selectedItems to selection
                    set itemPaths to {}
                    repeat with anItem in selectedItems
                        set end of itemPaths to POSIX path of (anItem as alias)
                    end repeat
                    return itemPaths as string
                end tell
                '''
            
            elif action == 'refresh':
                script = '''
                tell application "Finder"
                    tell front window to update
                end tell
                '''
            
            else:
                return f"Unsupported Finder action: {action}"
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                return f"Finder {action} completed{f': {output}' if output else ''}"
            else:
                return f"Failed to {action} in Finder: {result.stderr}"
                
        except Exception as e:
            return f"Error controlling Finder: {e}"
    
    def clipboard_management(self, action: str, content: str = None, content_type: str = 'text') -> str:
        """Manage system clipboard."""
        try:
            if action == 'get':
                if PYOBJC_AVAILABLE and self.pasteboard:
                    if content_type == 'text':
                        clipboard_content = self.pasteboard.stringForType_(NSStringPboardType)
                        return f"Clipboard content: {clipboard_content or 'Empty'}"
                    else:
                        return f"Content type '{content_type}' not supported with PyObjC"
                
                # Fallback using pbpaste
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Clipboard content: {result.stdout}"
                else:
                    return "Failed to get clipboard content"
            
            elif action == 'set':
                if not content:
                    return "Content required for set action"
                
                if PYOBJC_AVAILABLE and self.pasteboard:
                    if content_type == 'text':
                        self.pasteboard.clearContents()
                        self.pasteboard.setString_forType_(content, NSStringPboardType)
                        return f"Clipboard set to: {content}"
                    else:
                        return f"Content type '{content_type}' not supported with PyObjC"
                
                # Fallback using pbcopy
                result = subprocess.run(['pbcopy'], input=content, text=True)
                if result.returncode == 0:
                    return f"Clipboard set to: {content}"
                else:
                    return "Failed to set clipboard content"
            
            elif action == 'clear':
                if PYOBJC_AVAILABLE and self.pasteboard:
                    self.pasteboard.clearContents()
                    return "Clipboard cleared"
                
                # Fallback using pbcopy with empty content
                result = subprocess.run(['pbcopy'], input='', text=True)
                if result.returncode == 0:
                    return "Clipboard cleared"
                else:
                    return "Failed to clear clipboard"
            
            else:
                return f"Unsupported clipboard action: {action}"
                
        except Exception as e:
            return f"Error managing clipboard: {e}"
    
    def notification_management(self, action: str, title: str = None, message: str = None, app_name: str = None) -> str:
        """Send and manage Mac notifications."""
        try:
            if action == 'send':
                if not title:
                    return "Title required for send action"
                
                script = f'''
                display notification "{message or ''}" with title "{title}"
                '''
                
                if app_name:
                    script = f'''
                    tell application "{app_name}"
                        display notification "{message or ''}" with title "{title}"
                    end tell
                    '''
            
            elif action == 'clear':
                # Clear all notifications (limited capability)
                script = '''
                tell application "System Events"
                    tell process "NotificationCenter"
                        try
                            click button "Clear All" of group 1 of UI element 1 of scroll area 1 of group 1 of group 1 of window "Notification Center"
                        end try
                    end tell
                end tell
                '''
            
            elif action == 'list':
                # Limited capability to list notifications
                return "Listing notifications is not supported through AppleScript"
            
            else:
                return f"Unsupported notification action: {action}"
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Notification {action} completed"
            else:
                return f"Failed to {action} notification: {result.stderr}"
                
        except Exception as e:
            return f"Error managing notifications: {e}"
    
    def system_preferences_control(self, action: str, pane: str = None, setting: str = None, value: str = None) -> str:
        """Control System Preferences/Settings."""
        try:
            if action == 'open':
                if pane:
                    script = f'''
                    tell application "System Preferences"
                        activate
                        set current pane to pane "{pane}"
                    end tell
                    '''
                else:
                    script = '''
                    tell application "System Preferences"
                        activate
                    end tell
                    '''
            
            elif action == 'list_panes':
                script = '''
                tell application "System Preferences"
                    get name of every pane
                end tell
                '''
            
            elif action == 'get_setting':
                if not (pane and setting):
                    return "Pane and setting required for get_setting action"
                
                # Use defaults command for getting preferences
                result = subprocess.run([
                    'defaults', 'read', pane, setting
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    return f"Setting {pane}.{setting}: {result.stdout.strip()}"
                else:
                    return f"Failed to get setting: {result.stderr}"
            
            elif action == 'set_setting':
                if not (pane and setting and value):
                    return "Pane, setting, and value required for set_setting action"
                
                if self.safe_mode:
                    return "Setting system preferences disabled in safe mode"
                
                # Use defaults command for setting preferences
                result = subprocess.run([
                    'defaults', 'write', pane, setting, value
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    return f"Setting {pane}.{setting} set to: {value}"
                else:
                    return f"Failed to set setting: {result.stderr}"
            
            else:
                return f"Unsupported system preferences action: {action}"
            
            if action in ['open', 'list_panes']:
                result = subprocess.run([
                    'osascript', '-e', script
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    return f"System Preferences {action} completed{f': {output}' if output else ''}"
                else:
                    return f"Failed to {action} System Preferences: {result.stderr}"
            
        except Exception as e:
            return f"Error controlling System Preferences: {e}"
    
    def dock_control(self, action: str, app_name: str = None, position: str = None) -> str:
        """Control Mac Dock."""
        try:
            if action == 'add_app':
                if not app_name:
                    return "App name required for add_app action"
                
                script = f'''
                tell application "Dock"
                    make new item at end with properties {{name:"{app_name}"}}
                end tell
                '''
            
            elif action == 'remove_app':
                if not app_name:
                    return "App name required for remove_app action"
                
                script = f'''
                tell application "System Events"
                    tell process "Dock"
                        try
                            right click UI element "{app_name}" of list 1
                            click menu item "Remove from Dock" of menu 1
                        end try
                    end tell
                end tell
                '''
            
            elif action == 'set_position':
                if not position:
                    return "Position required for set_position action"
                
                if position not in ['bottom', 'left', 'right']:
                    return "Position must be 'bottom', 'left', or 'right'"
                
                result = subprocess.run([
                    'defaults', 'write', 'com.apple.dock', 'orientation', position
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Restart Dock to apply changes
                    subprocess.run(['killall', 'Dock'])
                    return f"Dock position set to: {position}"
                else:
                    return f"Failed to set dock position: {result.stderr}"
            
            elif action == 'set_autohide':
                enabled = position == 'true' if position else True
                
                result = subprocess.run([
                    'defaults', 'write', 'com.apple.dock', 'autohide', 'true' if enabled else 'false'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    subprocess.run(['killall', 'Dock'])
                    return f"Dock autohide {'enabled' if enabled else 'disabled'}"
                else:
                    return f"Failed to set dock autohide: {result.stderr}"
            
            elif action == 'get_apps':
                script = '''
                tell application "System Events"
                    tell process "Dock"
                        get name of every UI element of list 1
                    end tell
                end tell
                '''
            
            else:
                return f"Unsupported dock action: {action}"
            
            if action in ['add_app', 'remove_app', 'get_apps']:
                result = subprocess.run([
                    'osascript', '-e', script
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    return f"Dock {action} completed{f': {output}' if output else ''}"
                else:
                    return f"Failed to {action} dock: {result.stderr}"
                    
        except Exception as e:
            return f"Error controlling dock: {e}"
    
    def menu_bar_interaction(self, action: str, menu_name: str = None, item_name: str = None, app_name: str = None) -> str:
        """Interact with menu bar and menu items."""
        try:
            if action == 'click_menu':
                if not (menu_name and item_name):
                    return "Menu name and item name required for click_menu action"
                
                if app_name:
                    script = f'''
                    tell application "{app_name}"
                        activate
                        tell application "System Events"
                            tell process "{app_name}"
                                click menu item "{item_name}" of menu "{menu_name}" of menu bar 1
                            end tell
                        end tell
                    end tell
                    '''
                else:
                    script = f'''
                    tell application "System Events"
                        click menu item "{item_name}" of menu "{menu_name}" of menu bar 1
                    end tell
                    '''
            
            elif action == 'get_menus':
                if app_name:
                    script = f'''
                    tell application "{app_name}"
                        activate
                        tell application "System Events"
                            tell process "{app_name}"
                                get name of every menu of menu bar 1
                            end tell
                        end tell
                    end tell
                    '''
                else:
                    script = '''
                    tell application "System Events"
                        get name of every menu of menu bar 1
                    end tell
                    '''
            
            elif action == 'get_menu_items':
                if not menu_name:
                    return "Menu name required for get_menu_items action"
                
                if app_name:
                    script = f'''
                    tell application "{app_name}"
                        activate
                        tell application "System Events"
                            tell process "{app_name}"
                                get name of every menu item of menu "{menu_name}" of menu bar 1
                            end tell
                        end tell
                    end tell
                    '''
                else:
                    script = f'''
                    tell application "System Events"
                        get name of every menu item of menu "{menu_name}" of menu bar 1
                    end tell
                    '''
            
            else:
                return f"Unsupported menu bar action: {action}"
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                return f"Menu bar {action} completed{f': {output}' if output else ''}"
            else:
                return f"Failed to {action} menu bar: {result.stderr}"
                
        except Exception as e:
            return f"Error interacting with menu bar: {e}"
    
    def take_screenshot(self, save_path: str = None, x: int = None, y: int = None, width: int = None, height: int = None, window_id: str = None) -> str:
        """Take screenshots of desktop or specific areas."""
        try:
            if not save_path:
                save_path = f"/tmp/mac_mcp_screenshot_{int(time.time())}.png"
            
            save_path = os.path.expanduser(save_path)
            
            command = ['screencapture']
            
            # Add region if specified
            if x is not None and y is not None and width is not None and height is not None:
                command.extend(['-R', f'{x},{y},{width},{height}'])
            
            # Add window ID if specified
            if window_id:
                command.extend(['-l', window_id])
            
            # Add silent flag
            command.append('-x')
            
            # Add output path
            command.append(save_path)
            
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                if os.path.exists(save_path):
                    file_size = os.path.getsize(save_path)
                    return f"Screenshot saved to {save_path} ({file_size} bytes)"
                else:
                    return f"Screenshot command succeeded but file not found: {save_path}"
            else:
                return f"Failed to take screenshot: {result.stderr}"
                
        except Exception as e:
            return f"Error taking screenshot: {e}"
    
    def process_management(self, action: str, process_name: str = None, pid: int = None) -> str:
        """Manage system processes."""
        try:
            if action == 'list':
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    return f"Running processes ({len(lines)-1} total):\n" + '\n'.join(lines[:20])  # Limit output
                else:
                    return f"Failed to list processes: {result.stderr}"
            
            elif action == 'kill':
                if self.safe_mode:
                    return "Process killing disabled in safe mode"
                
                if pid:
                    result = subprocess.run(['kill', str(pid)], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"Process {pid} killed"
                    else:
                        return f"Failed to kill process {pid}: {result.stderr}"
                elif process_name:
                    result = subprocess.run(['pkill', process_name], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"Processes matching '{process_name}' killed"
                    else:
                        return f"Failed to kill processes: {result.stderr}"
                else:
                    return "Either PID or process name required for kill action"
            
            elif action == 'info':
                if pid:
                    result = subprocess.run(['ps', '-p', str(pid), '-o', 'pid,ppid,user,%cpu,%mem,command'], capture_output=True, text=True)
                elif process_name:
                    result = subprocess.run(['pgrep', '-l', process_name], capture_output=True, text=True)
                else:
                    return "Either PID or process name required for info action"
                
                if result.returncode == 0:
                    return f"Process info:\n{result.stdout}"
                else:
                    return f"Process not found or error: {result.stderr}"
            
            elif action in ['cpu_usage', 'memory_usage']:
                try:
                    import psutil
                    if action == 'cpu_usage':
                        usage = psutil.cpu_percent(interval=1)
                        return f"CPU usage: {usage}%"
                    else:
                        memory = psutil.virtual_memory()
                        return f"Memory usage: {memory.percent}% ({memory.used}/{memory.total} bytes)"
                except ImportError:
                    return "psutil not available for detailed system monitoring"
            
            else:
                return f"Unsupported process action: {action}"
                
        except Exception as e:
            return f"Error managing processes: {e}"
    
    def wait(self, duration: float = None, condition: str = None, element_type: str = None, identifier: str = None, timeout: float = 30.0) -> str:
        """Wait for specified duration or conditions."""
        try:
            if duration is not None:
                time.sleep(duration)
                return f"Waited for {duration} seconds"
            
            elif condition:
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    if condition == 'element_appears':
                        if element_type and identifier:
                            # Check if element exists
                            result = self.click_element(element_type, identifier, timeout=1.0)
                            if "Failed" not in result and "Error" not in result:
                                return f"Element {element_type} '{identifier}' appeared"
                    
                    elif condition == 'app_launches':
                        if identifier:  # App name
                            apps = self.list_applications(running_only=True)
                            for app in apps:
                                if isinstance(app, dict) and app.get('name', '').lower() == identifier.lower():
                                    return f"App '{identifier}' launched"
                    
                    time.sleep(0.5)  # Check every 500ms
                
                return f"Condition '{condition}' not met within {timeout} seconds"
            
            else:
                return "Either duration or condition must be specified"
                
        except Exception as e:
            return f"Error waiting: {e}"
    
    # Additional helper methods for system monitoring and control
    def network_management(self, action: str, interface: str = None, setting: str = None, value: str = None) -> str:
        """Get network information and control network settings."""
        try:
            if action == 'list_interfaces':
                result = subprocess.run(['ifconfig', '-l'], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Network interfaces: {result.stdout.strip()}"
                else:
                    return f"Failed to list interfaces: {result.stderr}"
            
            elif action == 'get_info':
                interface = interface or 'en0'  # Default to en0
                result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Interface {interface} info:\n{result.stdout}"
                else:
                    return f"Failed to get interface info: {result.stderr}"
            
            elif action == 'wifi_scan':
                result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"WiFi networks:\n{result.stdout}"
                else:
                    return f"Failed to scan WiFi: {result.stderr}"
            
            else:
                return f"Unsupported network action: {action}"
                
        except Exception as e:
            return f"Error managing network: {e}"
    
    def volume_control(self, action: str, level: int = None, device: str = None) -> str:
        """Control system volume and audio."""
        try:
            if action == 'get_volume':
                result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Current volume: {result.stdout.strip()}%"
                else:
                    return f"Failed to get volume: {result.stderr}"
            
            elif action == 'set_volume':
                if level is None:
                    return "Volume level required for set_volume action"
                
                level = max(0, min(100, level))  # Clamp to 0-100
                result = subprocess.run(['osascript', '-e', f'set volume output volume {level}'], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Volume set to {level}%"
                else:
                    return f"Failed to set volume: {result.stderr}"
            
            elif action == 'mute':
                result = subprocess.run(['osascript', '-e', 'set volume with output muted'], capture_output=True, text=True)
                if result.returncode == 0:
                    return "Audio muted"
                else:
                    return f"Failed to mute: {result.stderr}"
            
            elif action == 'unmute':
                result = subprocess.run(['osascript', '-e', 'set volume without output muted'], capture_output=True, text=True)
                if result.returncode == 0:
                    return "Audio unmuted"
                else:
                    return f"Failed to unmute: {result.stderr}"
            
            else:
                return f"Unsupported volume action: {action}"
                
        except Exception as e:
            return f"Error controlling volume: {e}"
    
    def display_control(self, action: str, display_id: int = None, resolution: str = None, brightness: int = None) -> str:
        """Control display settings and resolution."""
        try:
            if action == 'list_displays':
                if PYOBJC_AVAILABLE:
                    screens = NSScreen.screens()
                    displays = []
                    for i, screen in enumerate(screens):
                        frame = screen.frame()
                        displays.append(f"Display {i}: {int(frame.size.width)}x{int(frame.size.height)}")
                    return f"Displays: {', '.join(displays)}"
                else:
                    return "Display listing requires PyObjC"
            
            elif action == 'get_brightness':
                try:
                    result = subprocess.run(['brightness', '-l'], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"Brightness info:\n{result.stdout}"
                    else:
                        return "Brightness command not available (install 'brightness' tool)"
                except FileNotFoundError:
                    return "Brightness control not available (install 'brightness' tool)"
            
            elif action == 'set_brightness':
                if brightness is None:
                    return "Brightness level required for set_brightness action"
                
                brightness = max(0, min(100, brightness))  # Clamp to 0-100
                brightness_decimal = brightness / 100.0
                
                try:
                    result = subprocess.run(['brightness', str(brightness_decimal)], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"Brightness set to {brightness}%"
                    else:
                        return f"Failed to set brightness: {result.stderr}"
                except FileNotFoundError:
                    return "Brightness control not available (install 'brightness' tool)"
            
            else:
                return f"Unsupported display action: {action}"
                
        except Exception as e:
            return f"Error controlling display: {e}"
    
    def accessibility_control(self, action: str, feature: str = None, enabled: bool = None) -> str:
        """Control accessibility features and settings."""
        try:
            if action == 'check_permissions':
                return "Accessibility permissions: " + ("Enabled" if self._check_accessibility_permissions() else "Disabled")
            
            elif action == 'list_features':
                features = [
                    'VoiceOver', 'Zoom', 'Switch Control', 'Sticky Keys',
                    'Slow Keys', 'Mouse Keys', 'Display Accommodations'
                ]
                return f"Accessibility features: {', '.join(features)}"
            
            elif action in ['get_feature', 'set_feature']:
                if not feature:
                    return "Feature name required"
                
                # Map feature names to system preferences
                feature_map = {
                    'voice_over': 'com.apple.universalaccess voiceOverOnOffKey',
                    'zoom': 'com.apple.universalaccess closeViewScrollWheelToggle',
                    'sticky_keys': 'com.apple.universalaccess stickyKey'
                }
                
                pref_key = feature_map.get(feature.lower())
                if not pref_key:
                    return f"Unknown accessibility feature: {feature}"
                
                domain, key = pref_key.split(' ', 1)
                
                if action == 'get_feature':
                    result = subprocess.run(['defaults', 'read', domain, key], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"Feature {feature}: {result.stdout.strip()}"
                    else:
                        return f"Failed to get feature: {result.stderr}"
                
                else:  # set_feature
                    if enabled is None:
                        return "Enabled value required for set_feature action"
                    
                    if self.safe_mode:
                        return "Accessibility feature changes disabled in safe mode"
                    
                    value = 'true' if enabled else 'false'
                    result = subprocess.run(['defaults', 'write', domain, key, value], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"Feature {feature} {'enabled' if enabled else 'disabled'}"
                    else:
                        return f"Failed to set feature: {result.stderr}"
            
            else:
                return f"Unsupported accessibility action: {action}"
                
        except Exception as e:
            return f"Error controlling accessibility: {e}"