#!/usr/bin/env python3
"""
Chrome MCP Server

A Model Context Protocol server for Chrome browser automation and web testing.
Provides tools to interact directly with Chrome browser, enabling automated web testing,
scraping, and browser control similar to Android/iOS MCP servers.
"""

from mcp.server.fastmcp import FastMCP, Image
from contextlib import asynccontextmanager
from argparse import ArgumentParser
from src.chrome import ChromeBrowser
from textwrap import dedent
import asyncio


parser = ArgumentParser()
parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
parser.add_argument('--user-data-dir', type=str, help='Chrome user data directory path')
parser.add_argument('--profile', type=str, help='Chrome profile name to use')
parser.add_argument('--window-size', type=str, default='1920,1080', help='Browser window size (width,height)')
parser.add_argument('--incognito', action='store_true', help='Run in incognito mode')
parser.add_argument('--disable-extensions', action='store_true', help='Disable Chrome extensions')
parser.add_argument('--port', type=int, default=9222, help='Chrome debugging port (default: 9222)')
args = parser.parse_args()

instructions = dedent('''
Chrome MCP server provides tools to interact directly with Chrome browser,
enabling automated web testing, scraping, and browser control.
Supports both headless and GUI modes with comprehensive element interaction capabilities.
''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    await asyncio.sleep(1)  # Simulate startup latency
    yield

mcp = FastMCP(name="Chrome-MCP", instructions=instructions)

# Initialize Chrome browser
chrome_browser = ChromeBrowser(
    headless=args.headless,
    user_data_dir=args.user_data_dir,
    profile=args.profile,
    window_size=args.window_size,
    incognito=args.incognito,
    disable_extensions=args.disable_extensions,
    debug_port=args.port
)

@mcp.tool(name='Navigate-Tool', description='Navigate to a specific URL')
def navigate_tool(url: str):
    """Navigate to a specific URL in the browser."""
    chrome_browser.navigate(url)
    return f'Navigated to {url}'

@mcp.tool('State-Tool', description='Get the current state of the browser. Optionally includes visual screenshot when use_vision=True.')
def state_tool(use_vision: bool = False):
    """Get the current state of the browser with optional screenshot."""
    browser_state = chrome_browser.get_state(use_vision=use_vision)
    result = [browser_state.page_state.to_string()]
    if use_vision and browser_state.screenshot:
        result.append(Image(data=browser_state.screenshot, format='PNG'))
    return result

@mcp.tool(name='Click-Tool', description='Click on specific coordinates')
def click_tool(x: int, y: int):
    """Click on specific coordinates on the webpage."""
    chrome_browser.click(x, y)
    return f'Clicked on ({x},{y})'

@mcp.tool(name='Element-Click-Tool', description='Click on element by various selectors')
def element_click_tool(selector: str, value: str, timeout: float = 10.0):
    """
    Click on element using various selectors.
    Selector types: id, name, class, tag, xpath, css, link_text, partial_link_text
    """
    result = chrome_browser.click_element(selector, value, timeout=timeout)
    return result

@mcp.tool(name='Type-Tool', description='Type text in active element or by coordinates')
def type_tool(text: str, x: int = None, y: int = None, clear: bool = False):
    """Type text in active element or click coordinates first."""
    chrome_browser.type_text(text, x, y, clear=clear)
    return f'Typed "{text}"'

@mcp.tool(name='Element-Type-Tool', description='Type text in element by various selectors')
def element_type_tool(selector: str, value: str, text: str, clear: bool = True, timeout: float = 10.0):
    """
    Type text in element using various selectors.
    Selector types: id, name, class, tag, xpath, css, link_text, partial_link_text
    """
    result = chrome_browser.type_in_element(selector, value, text, clear=clear, timeout=timeout)
    return result

@mcp.tool(name='Scroll-Tool', description='Scroll the page in specified direction')
def scroll_tool(direction: str, amount: int = 300):
    """
    Scroll the page in specified direction.
    Directions: up, down, left, right, top, bottom
    Amount: pixels to scroll (ignored for top/bottom)
    """
    chrome_browser.scroll(direction, amount)
    return f'Scrolled {direction} by {amount}px'

@mcp.tool(name='Wait-Tool', description='Wait for specified duration')
def wait_tool(duration: float):
    """Wait for specified duration in seconds."""
    chrome_browser.wait(duration)
    return f'Waited for {duration} seconds'

@mcp.tool(name='Element-Wait-Tool', description='Wait for element to appear')
def element_wait_tool(selector: str, value: str, timeout: float = 10.0):
    """
    Wait for element to appear using various selectors.
    Returns True if element appears, False if timeout.
    """
    result = chrome_browser.wait_for_element(selector, value, timeout=timeout)
    return f'Element {"found" if result else "not found"} within {timeout}s'

@mcp.tool(name='Back-Tool', description='Navigate back in browser history')
def back_tool():
    """Navigate back in browser history."""
    chrome_browser.back()
    return 'Navigated back'

@mcp.tool(name='Forward-Tool', description='Navigate forward in browser history')
def forward_tool():
    """Navigate forward in browser history."""
    chrome_browser.forward()
    return 'Navigated forward'

@mcp.tool(name='Refresh-Tool', description='Refresh the current page')
def refresh_tool():
    """Refresh the current page."""
    chrome_browser.refresh()
    return 'Page refreshed'

@mcp.tool(name='Tab-Control-Tool', description='Control browser tabs')
def tab_control_tool(action: str, tab_index: int = None, url: str = None):
    """
    Control browser tabs.
    Actions: new, close, switch, list
    """
    result = chrome_browser.tab_control(action, tab_index, url)
    return result

@mcp.tool(name='Window-Control-Tool', description='Control browser window')
def window_control_tool(action: str, width: int = None, height: int = None):
    """
    Control browser window.
    Actions: maximize, minimize, fullscreen, resize, position
    """
    result = chrome_browser.window_control(action, width, height)
    return result

@mcp.tool(name='Execute-Script-Tool', description='Execute JavaScript code')
def execute_script_tool(script: str, *args):
    """Execute JavaScript code in the browser."""
    result = chrome_browser.execute_script(script, *args)
    return f'Script executed, result: {result}'

@mcp.tool(name='Get-Attribute-Tool', description='Get element attribute value')
def get_attribute_tool(selector: str, value: str, attribute: str, timeout: float = 10.0):
    """Get attribute value from element using various selectors."""
    result = chrome_browser.get_element_attribute(selector, value, attribute, timeout=timeout)
    return result

@mcp.tool(name='Get-Text-Tool', description='Get element text content')
def get_text_tool(selector: str, value: str, timeout: float = 10.0):
    """Get text content from element using various selectors."""
    result = chrome_browser.get_element_text(selector, value, timeout=timeout)
    return result

@mcp.tool(name='Cookie-Tool', description='Manage browser cookies')
def cookie_tool(action: str, name: str = None, value: str = None, domain: str = None):
    """
    Manage browser cookies.
    Actions: get, set, delete, clear, list
    """
    result = chrome_browser.cookie_management(action, name, value, domain)
    return result

@mcp.tool(name='Download-Tool', description='Handle file downloads')
def download_tool(action: str, url: str = None, path: str = None):
    """
    Handle file downloads.
    Actions: download, list, clear
    """
    result = chrome_browser.download_management(action, url, path)
    return result

@mcp.tool(name='Alert-Tool', description='Handle browser alerts/dialogs')
def alert_tool(action: str, text: str = None):
    """
    Handle browser alerts and dialogs.
    Actions: accept, dismiss, get_text, send_text
    """
    result = chrome_browser.handle_alert(action, text)
    return result

@mcp.tool(name='Form-Tool', description='Interact with web forms')
def form_tool(action: str, selector: str = None, value: str = None, form_data: dict = None):
    """
    Interact with web forms.
    Actions: submit, reset, fill, get_data
    """
    result = chrome_browser.form_interaction(action, selector, value, form_data)
    return result

@mcp.tool(name='Screenshot-Tool', description='Take screenshot of current page or element')
def screenshot_tool(selector: str = None, value: str = None, save_path: str = None):
    """Take screenshot of current page or specific element."""
    result = chrome_browser.take_screenshot(selector, value, save_path)
    return result

if __name__ == '__main__':
    mcp.run()