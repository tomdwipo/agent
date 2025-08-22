"""
Chrome Browser Management Module

Handles Chrome browser connections, automation operations, and state management
using Selenium WebDriver with undetected-chromedriver for enhanced compatibility.
"""

import time
import os
import json
from typing import Optional, Union, Dict, Any, List, Tuple
from io import BytesIO
from PIL import Image

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException
)

from src.chrome.views import ChromeState
from src.page import PageTree


class ChromeBrowser:
    """Main Chrome browser management class."""
    
    def __init__(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None,
        profile: Optional[str] = None,
        window_size: str = "1920,1080",
        incognito: bool = False,
        disable_extensions: bool = False,
        debug_port: int = 9222
    ):
        """
        Initialize Chrome browser connection.
        
        Args:
            headless: Whether to run in headless mode
            user_data_dir: Chrome user data directory path
            profile: Chrome profile name to use
            window_size: Browser window size (width,height)
            incognito: Whether to run in incognito mode
            disable_extensions: Whether to disable Chrome extensions
            debug_port: Chrome debugging port
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.profile = profile
        self.window_size = window_size
        self.incognito = incognito
        self.disable_extensions = disable_extensions
        self.debug_port = debug_port
        self.driver = None
        
        self._initialize_browser()
    
    def _initialize_browser(self):
        """Initialize Chrome browser with specified options."""
        try:
            # Configure Chrome options for undetected-chromedriver
            options = uc.ChromeOptions()
            
            if self.headless:
                options.add_argument('--headless=new')
            
            if self.user_data_dir:
                options.add_argument(f'--user-data-dir={self.user_data_dir}')
            
            if self.profile:
                options.add_argument(f'--profile-directory={self.profile}')
            
            if self.incognito:
                options.add_argument('--incognito')
            
            if self.disable_extensions:
                options.add_argument('--disable-extensions')
            
            # Set window size
            options.add_argument(f'--window-size={self.window_size}')
            
            # Additional options for stability and compatibility
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument(f'--remote-debugging-port={self.debug_port}')
            
            # Set download preferences
            prefs = {
                'download.default_directory': os.path.expanduser('~/Downloads'),
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            }
            options.add_experimental_option('prefs', prefs)
            
            # Initialize undetected Chrome driver
            self.driver = uc.Chrome(options=options)
            
            try:
                # Check if we have a valid window before executing script
                current_window = self.driver.current_window_handle
                
                # Execute script to remove webdriver property
                self.driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                )
                
                print(f"Chrome browser initialized successfully")
                
            except Exception as script_error:
                print(f"Warning: Could not execute initialization script: {script_error}")
                # Try to recover by ensuring we have a valid window
                try:
                    windows = self.driver.window_handles
                    if not windows:
                        # No windows available, create a new one
                        self.driver.execute_script("window.open('about:blank', '_blank');")
                        windows = self.driver.window_handles
                    
                    if windows:
                        self.driver.switch_to.window(windows[0])
                        # Try the initialization script again
                        self.driver.execute_script(
                            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                        )
                        print(f"Chrome browser recovered and initialized successfully")
                    else:
                        print("Warning: Browser initialized but no valid windows available")
                        
                except Exception as recovery_error:
                    print(f"Warning: Browser initialized but recovery failed: {recovery_error}")
                    # Browser is still usable, just without the webdriver property removal
            
        except Exception as e:
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            raise ConnectionError(f"Failed to initialize Chrome browser: {e}")
    
    def _ensure_valid_window(self):
        """Ensure we have a valid browser window, create one if needed"""
        try:
            # Check if we have a valid window handle
            current_window = self.driver.current_window_handle
            # Try to interact with the window
            self.driver.execute_script("return document.readyState;")
            return True
        except Exception as e:
            print(f"Current window is invalid: {e}")
            try:
                # Check if there are other windows available
                windows = self.driver.window_handles
                if windows:
                    # Switch to the first available window
                    self.driver.switch_to.window(windows[0])
                    print("Switched to available window")
                    return True
                else:
                    # No windows available, open a new one
                    self.driver.execute_script("window.open('about:blank', '_blank');")
                    windows = self.driver.window_handles
                    if windows:
                        self.driver.switch_to.window(windows[-1])
                        print("Created and switched to new window")
                        return True
            except Exception as recovery_error:
                print(f"Failed to recover window: {recovery_error}")
                # Last resort: try full browser recovery
                return self._recover_browser()
        return False

    def _recover_browser(self) -> bool:
        """Attempt to recover from browser failure"""
        try:
            print("Attempting browser recovery...")
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            # Reinitialize the browser
            self._initialize_browser()
            print("Browser recovery successful")
            return True
        except Exception as e:
            print(f"Browser recovery failed: {e}")
            return False

    def get_driver(self):
        """Get the underlying WebDriver instance."""
        return self.driver
    
    def get_state(self, use_vision: bool = False) -> 'ChromeState':
        """
        Get current browser state with optional screenshot.
        
        Args:
            use_vision: Whether to include annotated screenshot
            
        Returns:
            ChromeState object containing page state and optional screenshot
        """
        try:
            # Ensure we have a valid window
            if not self._ensure_valid_window():
                raise Exception("No valid browser window available")
                
            page_tree = PageTree(self)
            page_state = page_tree.get_state()
            
            if use_vision:
                elements = page_state.interactive_elements
                annotated_screenshot = page_tree.annotated_screenshot(elements=elements, scale=1.0)
                screenshot = self.screenshot_in_bytes(annotated_screenshot)
            else:
                screenshot = None
                
            return ChromeState(page_state=page_state, screenshot=screenshot)
            
        except Exception as e:
            raise RuntimeError(f"Failed to get browser state: {e}")
    
    def get_screenshot(self, scale: float = 1.0) -> Image.Image:
        """
        Take screenshot of the current page.
        
        Args:
            scale: Scale factor for the image (default: 1.0)
            
        Returns:
            PIL Image object
        """
        try:
            # Take screenshot as PNG bytes
            screenshot_bytes = self.driver.get_screenshot_as_png()
            screenshot = Image.open(BytesIO(screenshot_bytes))
            
            # Scale image if needed
            if scale != 1.0:
                size = (int(screenshot.width * scale), int(screenshot.height * scale))
                screenshot = screenshot.resize(size, Image.Resampling.LANCZOS)
            
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
    
    def navigate(self, url: str):
        """Navigate to a specific URL."""
        try:
            # Ensure we have a valid window before navigation
            if not self._ensure_valid_window():
                raise Exception("No valid browser window available")
                
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            self.driver.get(url)
        except Exception as e:
            print(f"Failed to navigate to {url}: {e}")
            raise
    
    def click(self, x: int, y: int):
        """Click on specific coordinates."""
        try:
            # Ensure we have a valid window
            if not self._ensure_valid_window():
                raise Exception("No valid browser window available")
                
            ActionChains(self.driver).move_by_offset(x, y).click().perform()
            # Reset mouse position
            ActionChains(self.driver).move_by_offset(-x, -y).perform()
        except Exception as e:
            print(f"Failed to click at ({x}, {y}): {e}")
            raise
    
    def click_element(self, selector: str, value: str, timeout: float = 10.0) -> str:
        """
        Click on element using various selectors.
        
        Args:
            selector: Selector type (id, name, class, tag, xpath, css, link_text, partial_link_text)
            value: Selector value
            timeout: Timeout for element search
            
        Returns:
            Success message or error
        """
        try:
            # Ensure we have a valid window
            if not self._ensure_valid_window():
                return "Error: No valid browser window available"
                
            element = self._find_element(selector, value, timeout)
            if element:
                # Scroll element into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)  # Wait for scroll to complete
                
                # Click element
                element.click()
                return f"Clicked element: {selector}={value}"
            else:
                return f"Element not found: {selector}={value}"
                
        except Exception as e:
            return f"Error clicking element: {e}"
    
    def type_text(self, text: str, x: int = None, y: int = None, clear: bool = False):
        """Type text in active element or click coordinates first."""
        if x is not None and y is not None:
            self.click(x, y)
            time.sleep(0.2)
        
        if clear:
            # Clear existing text
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
        
        ActionChains(self.driver).send_keys(text).perform()
    
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
            element = self._find_element(selector, value, timeout)
            if element:
                # Scroll element into view and focus
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                element.click()
                
                if clear:
                    element.clear()
                
                element.send_keys(text)
                return f"Typed '{text}' in element: {selector}={value}"
            else:
                return f"Element not found: {selector}={value}"
                
        except Exception as e:
            return f"Error typing in element: {e}"
    
    def scroll(self, direction: str, amount: int = 300):
        """Scroll the page in specified direction."""
        if direction.lower() == 'up':
            self.driver.execute_script(f"window.scrollBy(0, -{amount});")
        elif direction.lower() == 'down':
            self.driver.execute_script(f"window.scrollBy(0, {amount});")
        elif direction.lower() == 'left':
            self.driver.execute_script(f"window.scrollBy(-{amount}, 0);")
        elif direction.lower() == 'right':
            self.driver.execute_script(f"window.scrollBy({amount}, 0);")
        elif direction.lower() == 'top':
            self.driver.execute_script("window.scrollTo(0, 0);")
        elif direction.lower() == 'bottom':
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def wait(self, duration: float):
        """Wait for specified duration."""
        time.sleep(duration)
    
    def wait_for_element(self, selector: str, value: str, timeout: float = 10.0) -> bool:
        """Wait for element to appear."""
        try:
            element = self._find_element(selector, value, timeout)
            return element is not None
        except Exception:
            return False
    
    def back(self):
        """Navigate back in browser history."""
        self.driver.back()
    
    def forward(self):
        """Navigate forward in browser history."""
        self.driver.forward()
    
    def refresh(self):
        """Refresh the current page."""
        self.driver.refresh()
    
    def tab_control(self, action: str, tab_index: int = None, url: str = None) -> str:
        """Control browser tabs."""
        try:
            if action == 'new':
                if url:
                    self.driver.execute_script(f"window.open('{url}', '_blank');")
                else:
                    self.driver.execute_script("window.open('', '_blank');")
                # Switch to new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])
                return "Opened new tab"
            
            elif action == 'close':
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    # Switch to remaining tab
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    return "Closed current tab"
                else:
                    return "Cannot close the last tab"
            
            elif action == 'switch':
                if tab_index is not None and 0 <= tab_index < len(self.driver.window_handles):
                    self.driver.switch_to.window(self.driver.window_handles[tab_index])
                    return f"Switched to tab {tab_index}"
                else:
                    return f"Invalid tab index: {tab_index}"
            
            elif action == 'list':
                tabs = []
                for i, handle in enumerate(self.driver.window_handles):
                    self.driver.switch_to.window(handle)
                    tabs.append(f"Tab {i}: {self.driver.title} - {self.driver.current_url}")
                return f"Tabs: {'; '.join(tabs)}"
            
            else:
                return f"Unsupported tab action: {action}"
                
        except Exception as e:
            return f"Error controlling tabs: {e}"
    
    def window_control(self, action: str, width: int = None, height: int = None) -> str:
        """Control browser window."""
        try:
            if action == 'maximize':
                self.driver.maximize_window()
                return "Window maximized"
            
            elif action == 'minimize':
                self.driver.minimize_window()
                return "Window minimized"
            
            elif action == 'fullscreen':
                self.driver.fullscreen_window()
                return "Window set to fullscreen"
            
            elif action == 'resize':
                if width and height:
                    self.driver.set_window_size(width, height)
                    return f"Window resized to {width}x{height}"
                else:
                    return "Width and height required for resize"
            
            elif action == 'position':
                if width is not None and height is not None:  # Using as x, y coordinates
                    self.driver.set_window_position(width, height)
                    return f"Window positioned at ({width}, {height})"
                else:
                    return "X and Y coordinates required for position"
            
            else:
                return f"Unsupported window action: {action}"
                
        except Exception as e:
            return f"Error controlling window: {e}"
    
    def execute_script(self, script: str, *args):
        """Execute JavaScript code in the browser."""
        try:
            result = self.driver.execute_script(script, *args)
            return result
        except Exception as e:
            return f"Script execution error: {e}"
    
    def get_element_attribute(self, selector: str, value: str, attribute: str, timeout: float = 10.0) -> str:
        """Get attribute value from element."""
        try:
            element = self._find_element(selector, value, timeout)
            if element:
                attr_value = element.get_attribute(attribute)
                return f"Attribute '{attribute}': {attr_value}"
            else:
                return f"Element not found: {selector}={value}"
        except Exception as e:
            return f"Error getting attribute: {e}"
    
    def get_element_text(self, selector: str, value: str, timeout: float = 10.0) -> str:
        """Get text content from element."""
        try:
            element = self._find_element(selector, value, timeout)
            if element:
                text = element.text
                return f"Element text: {text}"
            else:
                return f"Element not found: {selector}={value}"
        except Exception as e:
            return f"Error getting text: {e}"
    
    def cookie_management(self, action: str, name: str = None, value: str = None, domain: str = None) -> str:
        """Manage browser cookies."""
        try:
            if action == 'get':
                if name:
                    cookie = self.driver.get_cookie(name)
                    return f"Cookie '{name}': {cookie}"
                else:
                    return "Cookie name required for get action"
            
            elif action == 'set':
                if name and value:
                    cookie_dict = {'name': name, 'value': value}
                    if domain:
                        cookie_dict['domain'] = domain
                    self.driver.add_cookie(cookie_dict)
                    return f"Cookie '{name}' set to '{value}'"
                else:
                    return "Name and value required for set action"
            
            elif action == 'delete':
                if name:
                    self.driver.delete_cookie(name)
                    return f"Cookie '{name}' deleted"
                else:
                    return "Cookie name required for delete action"
            
            elif action == 'clear':
                self.driver.delete_all_cookies()
                return "All cookies cleared"
            
            elif action == 'list':
                cookies = self.driver.get_cookies()
                return f"Cookies: {json.dumps(cookies, indent=2)}"
            
            else:
                return f"Unsupported cookie action: {action}"
                
        except Exception as e:
            return f"Error managing cookies: {e}"
    
    def download_management(self, action: str, url: str = None, path: str = None) -> str:
        """Handle file downloads."""
        try:
            if action == 'download':
                if url:
                    self.navigate(url)
                    return f"Initiated download from {url}"
                else:
                    return "URL required for download action"
            
            elif action == 'list':
                # Get Chrome downloads page
                self.navigate('chrome://downloads/')
                return "Navigated to downloads page"
            
            elif action == 'clear':
                # Clear downloads history
                self.navigate('chrome://downloads/')
                self.execute_script("downloads.Manager.clearAll();")
                return "Downloads cleared"
            
            else:
                return f"Unsupported download action: {action}"
                
        except Exception as e:
            return f"Error managing downloads: {e}"
    
    def handle_alert(self, action: str, text: str = None) -> str:
        """Handle browser alerts and dialogs."""
        try:
            alert = self.driver.switch_to.alert
            
            if action == 'accept':
                alert.accept()
                return "Alert accepted"
            
            elif action == 'dismiss':
                alert.dismiss()
                return "Alert dismissed"
            
            elif action == 'get_text':
                alert_text = alert.text
                return f"Alert text: {alert_text}"
            
            elif action == 'send_text':
                if text:
                    alert.send_keys(text)
                    return f"Sent text to alert: {text}"
                else:
                    return "Text required for send_text action"
            
            else:
                return f"Unsupported alert action: {action}"
                
        except Exception as e:
            return f"No alert present or error: {e}"
    
    def form_interaction(self, action: str, selector: str = None, value: str = None, form_data: dict = None) -> str:
        """Interact with web forms."""
        try:
            if action == 'submit':
                if selector and value:
                    form = self._find_element(selector, value)
                    if form:
                        form.submit()
                        return "Form submitted"
                    else:
                        return f"Form not found: {selector}={value}"
                else:
                    # Submit active form
                    self.driver.execute_script("document.forms[0].submit();")
                    return "Active form submitted"
            
            elif action == 'reset':
                if selector and value:
                    form = self._find_element(selector, value)
                    if form:
                        form.reset()
                        return "Form reset"
                    else:
                        return f"Form not found: {selector}={value}"
                else:
                    self.driver.execute_script("document.forms[0].reset();")
                    return "Active form reset"
            
            elif action == 'fill':
                if form_data:
                    filled_fields = []
                    for field_selector, field_value in form_data.items():
                        # Try to find and fill field
                        try:
                            element = self.driver.find_element(By.NAME, field_selector)
                            element.clear()
                            element.send_keys(field_value)
                            filled_fields.append(field_selector)
                        except:
                            try:
                                element = self.driver.find_element(By.ID, field_selector)
                                element.clear()
                                element.send_keys(field_value)
                                filled_fields.append(field_selector)
                            except:
                                continue
                    return f"Filled fields: {', '.join(filled_fields)}"
                else:
                    return "Form data required for fill action"
            
            else:
                return f"Unsupported form action: {action}"
                
        except Exception as e:
            return f"Error interacting with form: {e}"
    
    def take_screenshot(self, selector: str = None, value: str = None, save_path: str = None) -> str:
        """Take screenshot of current page or specific element."""
        try:
            if selector and value:
                # Screenshot of specific element
                element = self._find_element(selector, value)
                if element:
                    screenshot_bytes = element.screenshot_as_png
                    if save_path:
                        with open(save_path, 'wb') as f:
                            f.write(screenshot_bytes)
                        return f"Element screenshot saved to {save_path}"
                    else:
                        return "Element screenshot taken (not saved)"
                else:
                    return f"Element not found: {selector}={value}"
            else:
                # Full page screenshot
                if save_path:
                    self.driver.save_screenshot(save_path)
                    return f"Page screenshot saved to {save_path}"
                else:
                    screenshot_bytes = self.driver.get_screenshot_as_png()
                    return "Page screenshot taken (not saved)"
                    
        except Exception as e:
            return f"Error taking screenshot: {e}"
    
    def _find_element(self, selector: str, value: str, timeout: float = 10.0):
        """Find element using various selectors."""
        by_map = {
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }
        
        if selector not in by_map:
            return None
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by_map[selector], value)))
            return element
        except TimeoutException:
            return None
    
    def get_page_info(self) -> Dict[str, Any]:
        """Get current page information."""
        try:
            return {
                'title': self.driver.title,
                'url': self.driver.current_url,
                'window_size': self.driver.get_window_size(),
                'cookies_count': len(self.driver.get_cookies()),
                'window_handles': len(self.driver.window_handles)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()