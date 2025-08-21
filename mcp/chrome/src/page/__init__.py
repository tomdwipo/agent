"""
Page Module

Handles web page element hierarchy parsing and state management
for Chrome browser automation using Selenium WebDriver.
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


@dataclass
class WebElement:
    """Represents a web page element."""
    
    id: str
    tag_name: str
    text: str
    attributes: Dict[str, str]
    location: Dict[str, int]
    size: Dict[str, int]
    visible: bool
    enabled: bool
    interactive: bool = False
    
    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Get element bounds as (x, y, width, height)."""
        x = self.location.get('x', 0)
        y = self.location.get('y', 0)
        width = self.size.get('width', 0)
        height = self.size.get('height', 0)
        return (x, y, width, height)
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get element center coordinates."""
        x, y, width, height = self.bounds
        return (x + width // 2, y + height // 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert element to dictionary representation."""
        return {
            'id': self.id,
            'tag_name': self.tag_name,
            'text': self.text,
            'attributes': self.attributes,
            'location': self.location,
            'size': self.size,
            'visible': self.visible,
            'enabled': self.enabled,
            'interactive': self.interactive,
            'bounds': self.bounds,
            'center': self.center
        }


@dataclass
class PageState:
    """Represents the state of a web page."""
    
    elements: List[WebElement]
    interactive_elements: List[WebElement]
    page_info: Dict[str, Any]
    timestamp: float
    
    def to_string(self) -> str:
        """Convert page state to string representation."""
        result = f"Web Page State:\n"
        result += f"Title: {self.page_info.get('title', 'Unknown')}\n"
        result += f"URL: {self.page_info.get('url', 'Unknown')}\n"
        result += f"Total Elements: {len(self.elements)}\n"
        result += f"Interactive Elements: {len(self.interactive_elements)}\n\n"
        
        result += "Interactive Elements:\n"
        for i, element in enumerate(self.interactive_elements):
            bounds = element.bounds
            result += f"{i+1}. {element.tag_name.upper()}"
            if element.attributes.get('id'):
                result += f" #{element.attributes['id']}"
            if element.attributes.get('class'):
                result += f" .{element.attributes['class']}"
            if element.text:
                text = element.text[:50] + "..." if len(element.text) > 50 else element.text
                result += f" '{text}'"
            result += f" at ({bounds[0]}, {bounds[1]}, {bounds[2]}, {bounds[3]})\n"
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert page state to dictionary representation."""
        return {
            'elements': [elem.to_dict() for elem in self.elements],
            'interactive_elements': [elem.to_dict() for elem in self.interactive_elements],
            'page_info': self.page_info,
            'timestamp': self.timestamp
        }


class PageTree:
    """Web page element tree parser and manager."""
    
    def __init__(self, chrome_browser):
        """Initialize with Chrome browser instance."""
        self.chrome_browser = chrome_browser
        self.interactive_tags = {
            'a', 'button', 'input', 'textarea', 'select', 'option',
            'label', 'form', 'fieldset', 'legend', 'details', 'summary',
            'menuitem', 'area', 'canvas', 'audio', 'video', 'iframe',
            'embed', 'object'
        }
        self.interactive_types = {
            'button', 'submit', 'reset', 'image', 'checkbox', 'radio',
            'text', 'password', 'email', 'number', 'tel', 'url',
            'search', 'date', 'time', 'datetime-local', 'month', 'week',
            'color', 'file', 'range'
        }
    
    def get_state(self) -> PageState:
        """Get current page state."""
        try:
            driver = self.chrome_browser.get_driver()
            
            # Get page information
            page_info = self.chrome_browser.get_page_info()
            
            # Get all elements
            elements = self._parse_elements()
            interactive_elements = [elem for elem in elements if elem.interactive]
            
            return PageState(
                elements=elements,
                interactive_elements=interactive_elements,
                page_info=page_info,
                timestamp=time.time()
            )
            
        except Exception as e:
            # Fallback to minimal state
            return PageState(
                elements=[],
                interactive_elements=[],
                page_info={'title': 'Error', 'url': 'about:blank'},
                timestamp=time.time()
            )
    
    def _parse_elements(self) -> List[WebElement]:
        """Parse web page elements."""
        elements = []
        driver = self.chrome_browser.get_driver()
        
        try:
            # Get all elements
            web_elements = driver.find_elements(By.XPATH, "//*")
            
            for i, elem in enumerate(web_elements):
                try:
                    # Get element properties
                    tag_name = elem.tag_name
                    text = elem.text.strip()
                    
                    # Get attributes
                    attributes = {}
                    for attr in ['id', 'class', 'name', 'type', 'href', 'src', 'alt', 'title', 'placeholder']:
                        value = elem.get_attribute(attr)
                        if value:
                            attributes[attr] = value
                    
                    # Get location and size
                    location = elem.location
                    size = elem.size
                    
                    # Check visibility and interaction
                    visible = elem.is_displayed()
                    enabled = elem.is_enabled()
                    
                    # Determine if element is interactive
                    interactive = self._is_interactive_element(tag_name, attributes, visible, enabled, size)
                    
                    element = WebElement(
                        id=attributes.get('id', f'element_{i}'),
                        tag_name=tag_name,
                        text=text,
                        attributes=attributes,
                        location=location,
                        size=size,
                        visible=visible,
                        enabled=enabled,
                        interactive=interactive
                    )
                    
                    elements.append(element)
                    
                except Exception as e:
                    # Skip problematic elements
                    continue
            
            return elements
            
        except Exception as e:
            return []
    
    def _is_interactive_element(
        self,
        tag_name: str,
        attributes: Dict[str, str],
        visible: bool,
        enabled: bool,
        size: Dict[str, int]
    ) -> bool:
        """Check if an element is interactive."""
        if not visible or not enabled:
            return False
        
        # Check minimum size
        width = size.get('width', 0)
        height = size.get('height', 0)
        if width < 5 or height < 5:
            return False
        
        # Check tag name
        if tag_name.lower() in self.interactive_tags:
            return True
        
        # Check input type
        input_type = attributes.get('type', '').lower()
        if input_type in self.interactive_types:
            return True
        
        # Check for click handlers
        onclick = attributes.get('onclick')
        if onclick:
            return True
        
        # Check for role
        role = attributes.get('role', '').lower()
        if role in ['button', 'link', 'menuitem', 'tab', 'option']:
            return True
        
        return False
    
    def annotated_screenshot(self, elements: List[WebElement], scale: float = 1.0) -> Image.Image:
        """Create annotated screenshot with element highlights."""
        try:
            # Take screenshot
            screenshot = self.chrome_browser.get_screenshot(scale=scale)
            
            # Create drawing context
            draw = ImageDraw.Draw(screenshot)
            
            # Try to load a font, fallback to default
            try:
                # Try common font paths
                font_paths = [
                    "/System/Library/Fonts/Arial.ttf",  # macOS
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                    "C:/Windows/Fonts/arial.ttf"  # Windows
                ]
                font = None
                for path in font_paths:
                    try:
                        font = ImageFont.truetype(path, 16)
                        break
                    except:
                        continue
                
                if not font:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Annotate interactive elements
            for i, element in enumerate(elements):
                if not element.interactive:
                    continue
                
                # Scale bounds according to screenshot scale
                x, y, width, height = element.bounds
                x = int(x * scale)
                y = int(y * scale)
                width = int(width * scale)
                height = int(height * scale)
                
                # Skip if element is outside screenshot bounds
                if x < 0 or y < 0 or x + width > screenshot.width or y + height > screenshot.height:
                    continue
                
                # Draw rectangle around element
                draw.rectangle(
                    [x, y, x + width, y + height],
                    outline='red',
                    width=2
                )
                
                # Draw element number
                text = str(i + 1)
                
                # Get text dimensions
                try:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except:
                    text_width = len(text) * 8
                    text_height = 16
                
                # Position text
                text_x = x + 2
                text_y = y + 2
                
                # Ensure text is within bounds
                if text_x + text_width > screenshot.width:
                    text_x = screenshot.width - text_width - 2
                if text_y + text_height > screenshot.height:
                    text_y = screenshot.height - text_height - 2
                
                # Draw background for text
                draw.rectangle(
                    [text_x - 1, text_y - 1, text_x + text_width + 1, text_y + text_height + 1],
                    fill='red'
                )
                
                # Draw text
                draw.text((text_x, text_y), text, fill='white', font=font)
            
            return screenshot
            
        except Exception as e:
            # Return plain screenshot if annotation fails
            return self.chrome_browser.get_screenshot(scale=scale)