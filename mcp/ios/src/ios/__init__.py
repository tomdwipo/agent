"""
iOS Device Management Module

Handles iOS device connections, automation operations, and state management
using WebDriverAgent and tidevice for iOS automation.
"""

import time
import wda
import tidevice
from typing import Optional, Union, Dict, Any, Tuple
from io import BytesIO
from PIL import Image
from src.ios.views import IOSState
from src.tree import IOSTree


class IOSDevice:
    """Main iOS device management class."""
    
    def __init__(
        self,
        device: Optional[str] = None,
        simulator: bool = False,
        usb: bool = False,
        port: int = 8100
    ):
        """
        Initialize iOS device connection.
        
        Args:
            device: Device UDID or IP address (e.g., '192.168.1.100:8100')
            simulator: Whether to use iOS Simulator
            usb: Whether to connect via USB using tidevice
            port: WebDriverAgent port (default: 8100)
        """
        self.device = device
        self.simulator = simulator
        self.usb = usb
        self.port = port
        self.client = None
        self.session = None
        
        self._connect()
    
    def _connect(self):
        """Establish connection to iOS device."""
        try:
            if self.usb:
                # Use USB connection via tidevice
                if self.device:
                    self.client = wda.USBClient(self.device, port=self.port)
                else:
                    # Auto-detect first connected device
                    self.client = wda.USBClient(port=self.port)
            else:
                # Use network connection
                if self.device:
                    url = f"http://{self.device}"
                    if ':' not in self.device:
                        url = f"http://{self.device}:{self.port}"
                elif self.simulator:
                    url = f"http://localhost:{self.port}"
                else:
                    url = f"http://localhost:{self.port}"
                
                self.client = wda.Client(url)
            
            # Test connection
            status = self.client.status()
            print(f"Connected to iOS device: {status}")
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to iOS device: {e}")
    
    def get_device(self):
        """Get the underlying device client."""
        return self.client
    
    def get_session(self, bundle_id: Optional[str] = None):
        """Get or create a session for app control."""
        if not self.session or bundle_id:
            if bundle_id:
                self.session = self.client.session(bundle_id)
            else:
                self.session = self.client.session()
        return self.session
    
    def get_state(self, use_vision: bool = False) -> 'IOSState':
        """
        Get current device state with optional screenshot.
        
        Args:
            use_vision: Whether to include annotated screenshot
            
        Returns:
            IOSState object containing tree state and optional screenshot
        """
        try:
            tree = IOSTree(self)
            tree_state = tree.get_state()
            
            if use_vision:
                nodes = tree_state.interactive_elements
                annotated_screenshot = tree.annotated_screenshot(nodes=nodes, scale=1.0)
                screenshot = self.screenshot_in_bytes(annotated_screenshot)
            else:
                screenshot = None
                
            return IOSState(tree_state=tree_state, screenshot=screenshot)
            
        except Exception as e:
            raise RuntimeError(f"Failed to get device state: {e}")
    
    def get_screenshot(self, scale: float = 0.7) -> Image.Image:
        """
        Take screenshot of the device.
        
        Args:
            scale: Scale factor for the image (default: 0.7)
            
        Returns:
            PIL Image object
        """
        try:
            session = self.get_session()
            screenshot = session.screenshot()
            
            if screenshot is None:
                raise ValueError("Screenshot capture returned None")
            
            # Scale image if needed
            if scale != 1.0:
                size = (int(screenshot.width * scale), int(screenshot.height * scale))
                screenshot.thumbnail(size, Image.Resampling.LANCZOS)
            
            return screenshot
            
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
    
    def tap(self, x: int, y: int):
        """Tap on specific coordinates."""
        session = self.get_session()
        session.tap(x, y)
    
    def long_press(self, x: int, y: int, duration: float = 1.0):
        """Long press on specific coordinates."""
        session = self.get_session()
        session.tap_hold(x, y, duration)
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.5):
        """Swipe from one coordinate to another."""
        session = self.get_session()
        session.swipe(x1, y1, x2, y2, duration)
    
    def type_text(self, text: str, clear: bool = False):
        """Type text on the device."""
        session = self.get_session()
        if clear:
            # Clear current text if needed
            session.send_keys("\b" * 50)  # Delete existing text
        session.send_keys(text)
    
    def tap_element(self, selector: str, value: str, timeout: float = 10.0) -> str:
        """
        Tap on element using various selectors.
        
        Args:
            selector: Selector type (id, name, label, className, xpath, predicate)
            value: Selector value
            timeout: Timeout for element search
            
        Returns:
            Success message or error
        """
        try:
            session = self.get_session()
            
            # Build selector based on type
            if selector == 'id':
                element = session(id=value)
            elif selector == 'name':
                element = session(name=value)
            elif selector == 'label':
                element = session(label=value)
            elif selector == 'className':
                element = session(className=value)
            elif selector == 'xpath':
                element = session(xpath=value)
            elif selector == 'predicate':
                element = session(predicate=value)
            else:
                return f"Unsupported selector type: {selector}"
            
            # Wait for element and tap
            if element.wait(timeout=timeout):
                element.tap()
                return f"Tapped element: {selector}={value}"
            else:
                return f"Element not found: {selector}={value}"
                
        except Exception as e:
            return f"Error tapping element: {e}"
    
    def type_in_element(
        self,
        selector: str,
        value: str,
        text: str,
        clear: bool = True,
        timeout: float = 10.0
    ) -> str:
        """Type text in specific element."""
        try:
            session = self.get_session()
            
            # Build selector
            if selector == 'id':
                element = session(id=value)
            elif selector == 'name':
                element = session(name=value)
            elif selector == 'label':
                element = session(label=value)
            elif selector == 'className':
                element = session(className=value)
            elif selector == 'xpath':
                element = session(xpath=value)
            elif selector == 'predicate':
                element = session(predicate=value)
            else:
                return f"Unsupported selector type: {selector}"
            
            # Wait for element and type
            if element.wait(timeout=timeout):
                if clear:
                    element.clear_text()
                element.type(text)
                return f"Typed '{text}' in element: {selector}={value}"
            else:
                return f"Element not found: {selector}={value}"
                
        except Exception as e:
            return f"Error typing in element: {e}"
    
    def home(self):
        """Press home button."""
        self.client.home()
    
    def volume(self, direction: str):
        """Press volume buttons."""
        session = self.get_session()
        if direction.lower() == 'up':
            session.press("volumeUp")
        elif direction.lower() == 'down':
            session.press("volumeDown")
        else:
            raise ValueError("Direction must be 'up' or 'down'")
    
    def lock(self):
        """Lock the device."""
        session = self.get_session()
        session.lock()
    
    def unlock(self):
        """Unlock the device."""
        session = self.get_session()
        session.unlock()
    
    def is_locked(self) -> bool:
        """Check if device is locked."""
        session = self.get_session()
        return session.locked()
    
    def app_control(self, action: str, bundle_id: str) -> str:
        """Control app lifecycle."""
        try:
            session = self.get_session()
            
            if action == 'launch':
                session.app_activate(bundle_id)
                return f"Launched app: {bundle_id}"
            elif action == 'terminate':
                session.app_terminate(bundle_id)
                return f"Terminated app: {bundle_id}"
            elif action == 'activate':
                session.app_activate(bundle_id)
                return f"Activated app: {bundle_id}"
            elif action == 'state':
                state = session.app_state(bundle_id)
                state_map = {1: 'not_installed', 2: 'background', 4: 'running'}
                state_name = state_map.get(state.get('value', 0), 'unknown')
                return f"App {bundle_id} state: {state_name}"
            else:
                return f"Unsupported action: {action}"
                
        except Exception as e:
            return f"Error controlling app: {e}"
    
    def wait(self, duration: float):
        """Wait for specified duration."""
        time.sleep(duration)
    
    def get_orientation(self) -> str:
        """Get current device orientation."""
        session = self.get_session()
        return session.orientation
    
    def set_orientation(self, orientation: str):
        """Set device orientation."""
        session = self.get_session()
        orientation_map = {
            'portrait': wda.PORTRAIT,
            'landscape': wda.LANDSCAPE,
            'landscape_left': wda.LANDSCAPE_LEFT,
            'landscape_right': wda.LANDSCAPE_RIGHT
        }
        
        if orientation.lower() in orientation_map:
            session.orientation = orientation_map[orientation.lower()]
        else:
            raise ValueError(f"Invalid orientation: {orientation}")
    
    def handle_alert(self, action: str, text: str = None) -> str:
        """Handle iOS alerts and dialogs."""
        try:
            session = self.get_session()
            
            if action == 'accept':
                session.alert.accept()
                return "Accepted alert"
            elif action == 'dismiss':
                session.alert.dismiss()
                return "Dismissed alert"
            elif action == 'get_text':
                alert_text = session.alert.text
                return f"Alert text: {alert_text}"
            elif action == 'type_text' and text:
                session.alert.type(text)
                return f"Typed '{text}' in alert"
            else:
                return f"Unsupported alert action: {action}"
                
        except Exception as e:
            return f"Error handling alert: {e}"
    
    def scroll(self, direction: str, distance: float = 0.5):
        """Scroll in specified direction."""
        session = self.get_session()
        
        if direction.lower() == 'up':
            session.swipe_up()
        elif direction.lower() == 'down':
            session.swipe_down()
        elif direction.lower() == 'left':
            session.swipe_left()
        elif direction.lower() == 'right':
            session.swipe_right()
        else:
            # Custom scroll with distance
            width, height = session.window_size()
            center_x, center_y = width // 2, height // 2
            
            if direction.lower() == 'up':
                end_y = center_y - int(height * distance)
                session.swipe(center_x, center_y, center_x, end_y)
            elif direction.lower() == 'down':
                end_y = center_y + int(height * distance)
                session.swipe(center_x, center_y, center_x, end_y)
            elif direction.lower() == 'left':
                end_x = center_x - int(width * distance)
                session.swipe(center_x, center_y, end_x, center_y)
            elif direction.lower() == 'right':
                end_x = center_x + int(width * distance)
                session.swipe(center_x, center_y, end_x, center_y)
    
    def wait_for_element(self, selector: str, value: str, timeout: float = 10.0) -> bool:
        """Wait for element to appear."""
        try:
            session = self.get_session()
            
            # Build selector
            if selector == 'id':
                element = session(id=value)
            elif selector == 'name':
                element = session(name=value)
            elif selector == 'label':
                element = session(label=value)
            elif selector == 'className':
                element = session(className=value)
            elif selector == 'xpath':
                element = session(xpath=value)
            elif selector == 'predicate':
                element = session(predicate=value)
            else:
                return False
            
            return element.wait(timeout=timeout)
            
        except Exception as e:
            return False
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information."""
        try:
            session = self.get_session()
            return {
                'window_size': session.window_size(),
                'orientation': session.orientation,
                'battery': session.battery_info(),
                'device_info': session.device_info(),
                'locked': session.locked(),
                'scale': session.scale
            }
        except Exception as e:
            return {'error': str(e)}