"""
iOS Tree Module

Handles iOS UI element hierarchy parsing and state management
similar to Android's UIAutomator but for iOS using WebDriverAgent.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
from PIL import Image, ImageDraw, ImageFont


@dataclass
class IOSElement:
    """Represents an iOS UI element."""
    
    id: str
    name: str
    label: str
    className: str
    frame: Dict[str, Any]
    enabled: bool
    visible: bool
    interactive: bool = False
    
    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Get element bounds as (x, y, width, height)."""
        frame = self.frame
        x = int(frame.get('x', 0))
        y = int(frame.get('y', 0))
        width = int(frame.get('width', 0))
        height = int(frame.get('height', 0))
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
            'name': self.name,
            'label': self.label,
            'className': self.className,
            'frame': self.frame,
            'enabled': self.enabled,
            'visible': self.visible,
            'interactive': self.interactive,
            'bounds': self.bounds,
            'center': self.center
        }


@dataclass
class TreeState:
    """Represents the UI tree state of an iOS device."""
    
    elements: List[IOSElement]
    interactive_elements: List[IOSElement]
    window_size: Tuple[int, int]
    orientation: str
    timestamp: float
    
    def to_string(self) -> str:
        """Convert tree state to string representation."""
        result = f"iOS UI Tree State:\n"
        result += f"Window Size: {self.window_size}\n"
        result += f"Orientation: {self.orientation}\n"
        result += f"Total Elements: {len(self.elements)}\n"
        result += f"Interactive Elements: {len(self.interactive_elements)}\n\n"
        
        # Show all elements with text content
        result += "All Elements with Text:\n"
        text_elements = []
        for i, element in enumerate(self.elements):
            if element.name or element.label:
                bounds = element.bounds
                text_info = f"{i+1}. {element.className}"
                if element.name:
                    text_info += f" name='{element.name}'"
                if element.label and element.label != element.name:
                    text_info += f" label='{element.label}'"
                text_info += f" at ({bounds[0]}, {bounds[1]}, {bounds[2]}, {bounds[3]})"
                if element.interactive:
                    text_info += " (interactive)"
                text_elements.append(text_info)
        
        if text_elements:
            result += "\n".join(text_elements) + "\n\n"
        else:
            result += "No elements with text found.\n\n"
        
        result += "Interactive Elements:\n"
        if self.interactive_elements:
            for i, element in enumerate(self.interactive_elements):
                bounds = element.bounds
                result += f"{i+1}. {element.className}"
                if element.name:
                    result += f" '{element.name}'"
                if element.label:
                    result += f" [{element.label}]"
                result += f" at ({bounds[0]}, {bounds[1]}, {bounds[2]}, {bounds[3]})\n"
        else:
            result += "No interactive elements found.\n"
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tree state to dictionary representation."""
        return {
            'elements': [elem.to_dict() for elem in self.elements],
            'interactive_elements': [elem.to_dict() for elem in self.interactive_elements],
            'window_size': self.window_size,
            'orientation': self.orientation,
            'timestamp': self.timestamp
        }


class IOSTree:
    """iOS UI tree parser and manager."""
    
    def __init__(self, ios_device):
        """Initialize with iOS device instance."""
        self.ios_device = ios_device
        self.interactive_types = {
            'XCUIElementTypeButton',
            'XCUIElementTypeTextField',
            'XCUIElementTypeSecureTextField', 
            'XCUIElementTypeTextView',
            'XCUIElementTypeSwitch',
            'XCUIElementTypeSlider',
            'XCUIElementTypeCell',
            'XCUIElementTypeLink',
            'XCUIElementTypeImage',
            'XCUIElementTypeTab',
            'XCUIElementTypeTabBar',
            'XCUIElementTypeNavigationBar',
            'XCUIElementTypeSearchField',
            'XCUIElementTypeSegmentedControl',
            'XCUIElementTypePicker',
            'XCUIElementTypePickerWheel'
        }
    
    def get_state(self) -> TreeState:
        """Get current UI tree state."""
        try:
            import time
            
            session = self.ios_device.get_session()
            
            # Get page source (UI hierarchy)
            source = session.source(accessible=True)  # Get JSON format
            
            # Parse elements
            elements = self._parse_elements(source)
            interactive_elements = [elem for elem in elements if elem.interactive]
            
            # Get additional device info
            window_size = session.window_size()
            orientation = session.orientation
            
            return TreeState(
                elements=elements,
                interactive_elements=interactive_elements,
                window_size=window_size,
                orientation=orientation,
                timestamp=time.time()
            )
            
        except Exception as e:
            # Fallback to minimal state
            import time
            return TreeState(
                elements=[],
                interactive_elements=[],
                window_size=(375, 667),  # Default iPhone size
                orientation='PORTRAIT',
                timestamp=time.time()
            )
    
    def _parse_elements(self, source: Dict[str, Any], parent_frame: Optional[Dict] = None) -> List[IOSElement]:
        """Parse UI elements from source hierarchy."""
        elements = []
        
        if not isinstance(source, dict):
            return elements
        
        # Create element from current node
        element = self._create_element(source, parent_frame)
        if element:
            elements.append(element)
        
        # Process children recursively
        children = source.get('children', [])
        if isinstance(children, list):
            for child in children:
                child_elements = self._parse_elements(child, source.get('frame'))
                elements.extend(child_elements)
        
        return elements
    
    def _create_element(self, node: Dict[str, Any], parent_frame: Optional[Dict] = None) -> Optional[IOSElement]:
        """Create IOSElement from node data."""
        try:
            # Extract basic properties
            element_id = node.get('identifier', '')
            name = node.get('name', '')
            label = node.get('label', '')
            class_name = node.get('type', '')
            frame = node.get('frame', {})
            enabled = node.get('enabled', True)
            visible = node.get('visible', True)
            
            # Calculate absolute frame if parent frame exists
            if parent_frame and frame:
                # Adjust frame relative to parent
                abs_frame = {
                    'x': frame.get('x', 0) + parent_frame.get('x', 0),
                    'y': frame.get('y', 0) + parent_frame.get('y', 0),
                    'width': frame.get('width', 0),
                    'height': frame.get('height', 0)
                }
            else:
                abs_frame = frame
            
            # Determine if element is interactive
            interactive = (
                enabled and 
                visible and
                class_name in self.interactive_types and
                abs_frame.get('width', 0) > 0 and
                abs_frame.get('height', 0) > 0
            )
            
            return IOSElement(
                id=element_id,
                name=name,
                label=label,
                className=class_name,
                frame=abs_frame,
                enabled=enabled,
                visible=visible,
                interactive=interactive
            )
            
        except Exception as e:
            return None
    
    def annotated_screenshot(self, nodes: List[IOSElement], scale: float = 1.0) -> Image.Image:
        """Create annotated screenshot with element highlights."""
        try:
            # Take screenshot
            screenshot = self.ios_device.get_screenshot(scale=scale)
            
            # Create drawing context
            draw = ImageDraw.Draw(screenshot)
            
            # Try to load a font, fallback to default
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Annotate interactive elements
            for i, element in enumerate(nodes):
                if not element.interactive:
                    continue
                
                # Scale bounds according to screenshot scale
                x, y, width, height = element.bounds
                x = int(x * scale)
                y = int(y * scale)
                width = int(width * scale)
                height = int(height * scale)
                
                # Draw rectangle around element
                draw.rectangle(
                    [x, y, x + width, y + height],
                    outline='red',
                    width=2
                )
                
                # Draw element number
                text = str(i + 1)
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Position text
                text_x = x + 2
                text_y = y + 2
                
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
            return self.ios_device.get_screenshot(scale=scale)