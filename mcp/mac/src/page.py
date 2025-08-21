"""
Page Module for Mac Desktop

Handles Mac desktop UI tree structure, element discovery, and state management.
Provides a unified interface for accessing desktop elements and their properties.
"""

import time
import subprocess
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont


@dataclass
class InteractiveElement:
    """Represents an interactive element on the Mac desktop."""
    
    id: str
    type: str
    text: str
    bounds: Dict[str, int]
    properties: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'type': self.type,
            'text': self.text,
            'bounds': self.bounds,
            'properties': self.properties
        }


@dataclass
class PageState:
    """Represents the current state of the Mac desktop."""
    
    title: str
    url: str  # Current focused application
    interactive_elements: List[InteractiveElement]
    page_info: Dict[str, Any]
    
    def to_string(self) -> str:
        """Convert page state to string representation."""
        result = []
        result.append(f"Title: {self.title}")
        result.append(f"Focused App: {self.url}")
        result.append(f"Interactive Elements: {len(self.interactive_elements)}")
        
        for i, element in enumerate(self.interactive_elements[:10]):  # Limit to first 10
            result.append(f"  {i+1}. {element.type}: {element.text} at {element.bounds}")
        
        if len(self.interactive_elements) > 10:
            result.append(f"  ... and {len(self.interactive_elements) - 10} more elements")
        
        return "\n".join(result)


class PageTree:
    """Manages Mac desktop UI tree structure and element discovery."""
    
    def __init__(self, mac_device):
        """Initialize with Mac device reference."""
        self.mac_device = mac_device
    
    def get_state(self) -> PageState:
        """Get current desktop state with interactive elements."""
        try:
            # Get focused application
            focused_app = self._get_focused_app()
            
            # Get desktop title (computer name)
            title = self._get_desktop_title()
            
            # Discover interactive elements
            elements = self._discover_elements()
            
            # Get additional page info
            page_info = self._get_page_info()
            
            return PageState(
                title=title,
                url=focused_app,
                interactive_elements=elements,
                page_info=page_info
            )
            
        except Exception as e:
            # Return minimal state on error
            return PageState(
                title="Mac Desktop",
                url="Unknown",
                interactive_elements=[],
                page_info={"error": str(e)}
            )
    
    def _get_focused_app(self) -> str:
        """Get the currently focused application."""
        try:
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                return frontApp
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "Unknown"
                
        except Exception:
            return "Unknown"
    
    def _get_desktop_title(self) -> str:
        """Get desktop title (computer name)."""
        try:
            result = subprocess.run(['hostname'], capture_output=True, text=True)
            if result.returncode == 0:
                return f"Mac Desktop - {result.stdout.strip()}"
            else:
                return "Mac Desktop"
        except Exception:
            return "Mac Desktop"
    
    def _discover_elements(self) -> List[InteractiveElement]:
        """Discover interactive elements on the desktop."""
        elements = []
        
        try:
            # Get desktop items (files, folders)
            desktop_items = self._get_desktop_items()
            elements.extend(desktop_items)
            
            # Get dock items
            dock_items = self._get_dock_items()
            elements.extend(dock_items)
            
            # Get menu bar items
            menu_items = self._get_menu_bar_items()
            elements.extend(menu_items)
            
            # Get window elements from focused app
            window_elements = self._get_window_elements()
            elements.extend(window_elements)
            
        except Exception as e:
            # Add error element
            elements.append(InteractiveElement(
                id="error",
                type="error",
                text=f"Element discovery error: {e}",
                bounds={"x": 0, "y": 0, "width": 0, "height": 0},
                properties={"error": True}
            ))
        
        return elements
    
    def _get_desktop_items(self) -> List[InteractiveElement]:
        """Get desktop files and folders."""
        items = []
        
        try:
            script = '''
            tell application "Finder"
                set desktopItems to every item of desktop
                set itemList to {}
                repeat with anItem in desktopItems
                    set itemName to name of anItem
                    set itemList to itemList & itemName
                end repeat
                return itemList
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                item_names = result.stdout.strip().split(', ')
                
                for i, name in enumerate(item_names):
                    if name.strip():
                        items.append(InteractiveElement(
                            id=f"desktop_item_{i}",
                            type="file",
                            text=name.strip(),
                            bounds={"x": 50 + (i % 10) * 80, "y": 50 + (i // 10) * 80, "width": 64, "height": 64},
                            properties={"location": "desktop"}
                        ))
        except Exception:
            pass
        
        return items
    
    def _get_dock_items(self) -> List[InteractiveElement]:
        """Get dock applications."""
        items = []
        
        try:
            script = '''
            tell application "System Events"
                tell process "Dock"
                    set dockItems to name of every UI element of list 1
                    return dockItems
                end tell
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                item_names = result.stdout.strip().split(', ')
                
                for i, name in enumerate(item_names):
                    if name.strip() and name.strip() != "missing value":
                        items.append(InteractiveElement(
                            id=f"dock_item_{i}",
                            type="application",
                            text=name.strip(),
                            bounds={"x": 100 + i * 60, "y": 900, "width": 56, "height": 56},  # Approximate dock position
                            properties={"location": "dock"}
                        ))
        except Exception:
            pass
        
        return items
    
    def _get_menu_bar_items(self) -> List[InteractiveElement]:
        """Get menu bar items."""
        items = []
        
        try:
            focused_app = self._get_focused_app()
            
            if focused_app and focused_app != "Unknown":
                script = f'''
                tell application "{focused_app}"
                    activate
                    tell application "System Events"
                        tell process "{focused_app}"
                            set menuNames to name of every menu of menu bar 1
                            return menuNames
                        end tell
                    end tell
                end tell
                '''
                
                result = subprocess.run([
                    'osascript', '-e', script
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 and result.stdout.strip():
                    menu_names = result.stdout.strip().split(', ')
                    
                    for i, name in enumerate(menu_names):
                        if name.strip() and name.strip() != "missing value":
                            items.append(InteractiveElement(
                                id=f"menu_item_{i}",
                                type="menu",
                                text=name.strip(),
                                bounds={"x": 50 + i * 80, "y": 0, "width": 75, "height": 22},
                                properties={"location": "menu_bar", "app": focused_app}
                            ))
        except Exception:
            pass
        
        return items
    
    def _get_window_elements(self) -> List[InteractiveElement]:
        """Get UI elements from the focused application window."""
        items = []
        
        try:
            focused_app = self._get_focused_app()
            
            if focused_app and focused_app != "Unknown":
                script = f'''
                tell application "System Events"
                    tell process "{focused_app}"
                        try
                            set windowElements to every UI element of window 1
                            set elementInfo to {{}}
                            repeat with anElement in windowElements
                                try
                                    set elementName to name of anElement
                                    set elementRole to role of anElement
                                    set elementInfo to elementInfo & {{elementName, elementRole}}
                                end try
                            end repeat
                            return elementInfo
                        end try
                    end tell
                end tell
                '''
                
                result = subprocess.run([
                    'osascript', '-e', script
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 and result.stdout.strip():
                    # Parse the output (simplified)
                    elements_text = result.stdout.strip()
                    if elements_text and elements_text != "missing value":
                        # Create a generic window element
                        items.append(InteractiveElement(
                            id="focused_window",
                            type="window",
                            text=f"{focused_app} Window",
                            bounds={"x": 100, "y": 100, "width": 800, "height": 600},
                            properties={"app": focused_app, "elements_found": True}
                        ))
        except Exception:
            pass
        
        return items
    
    def _get_page_info(self) -> Dict[str, Any]:
        """Get additional page information."""
        try:
            import platform
            
            info = {
                'platform': platform.system(),
                'version': platform.mac_ver()[0],
                'machine': platform.machine(),
                'timestamp': time.time()
            }
            
            # Add screen resolution
            try:
                if hasattr(self.mac_device, 'get_system_info'):
                    sys_info = self.mac_device.get_system_info()
                    if 'displays' in sys_info:
                        info['displays'] = sys_info['displays']
            except Exception:
                pass
            
            return info
            
        except Exception as e:
            return {'error': str(e)}
    
    def annotated_screenshot(self, elements: List[InteractiveElement], scale: float = 1.0) -> Image.Image:
        """Create annotated screenshot with element highlights."""
        try:
            # Get base screenshot
            screenshot = self.mac_device.get_screenshot(scale=scale)
            
            if not screenshot:
                return None
            
            # Create drawing context
            draw = ImageDraw.Draw(screenshot)
            
            # Try to load a font, fallback to default
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            # Annotate elements
            for i, element in enumerate(elements[:20]):  # Limit annotations
                bounds = element.bounds
                x, y = bounds.get('x', 0), bounds.get('y', 0)
                width, height = bounds.get('width', 0), bounds.get('height', 0)
                
                # Scale coordinates
                x, y = int(x * scale), int(y * scale)
                width, height = int(width * scale), int(height * scale)
                
                # Draw bounding box
                if width > 0 and height > 0:
                    color = 'red' if element.type == 'button' else 'blue'
                    draw.rectangle(
                        [x, y, x + width, y + height],
                        outline=color,
                        width=2
                    )
                    
                    # Draw label
                    label = f"{i+1}. {element.text[:20]}"
                    text_bbox = draw.textbbox((0, 0), label, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    
                    # Background for text
                    draw.rectangle(
                        [x, y - text_height - 4, x + text_width + 4, y],
                        fill='white',
                        outline=color
                    )
                    
                    # Text
                    draw.text((x + 2, y - text_height - 2), label, fill='black', font=font)
            
            return screenshot
            
        except Exception as e:
            # Return original screenshot on error
            try:
                return self.mac_device.get_screenshot(scale=scale)
            except:
                return None