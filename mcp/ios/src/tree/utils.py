"""
iOS Tree Utilities

Helper functions for iOS UI tree manipulation and processing.
"""

from typing import List, Dict, Any, Optional, Tuple
from .config import INTERACTIVE_ELEMENT_TYPES, MIN_INTERACTIVE_SIZE


def is_interactive_element(element_type: str, frame: Dict[str, Any], enabled: bool = True, visible: bool = True) -> bool:
    """
    Check if an element is interactive based on type, size, and properties.
    
    Args:
        element_type: XCUIElement type
        frame: Element frame dictionary
        enabled: Whether element is enabled
        visible: Whether element is visible
        
    Returns:
        True if element is interactive, False otherwise
    """
    if not enabled or not visible:
        return False
    
    if element_type not in INTERACTIVE_ELEMENT_TYPES:
        return False
    
    width = frame.get('width', 0)
    height = frame.get('height', 0)
    
    if width < MIN_INTERACTIVE_SIZE['width'] or height < MIN_INTERACTIVE_SIZE['height']:
        return False
    
    return True


def calculate_element_center(frame: Dict[str, Any]) -> Tuple[int, int]:
    """
    Calculate center coordinates of an element.
    
    Args:
        frame: Element frame dictionary
        
    Returns:
        Tuple of (center_x, center_y)
    """
    x = int(frame.get('x', 0))
    y = int(frame.get('y', 0))
    width = int(frame.get('width', 0))
    height = int(frame.get('height', 0))
    
    center_x = x + width // 2
    center_y = y + height // 2
    
    return (center_x, center_y)


def filter_visible_elements(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter out elements that are not visible or have zero size.
    
    Args:
        elements: List of element dictionaries
        
    Returns:
        Filtered list of visible elements
    """
    visible_elements = []
    
    for element in elements:
        if not element.get('visible', False):
            continue
        
        frame = element.get('frame', {})
        width = frame.get('width', 0)
        height = frame.get('height', 0)
        
        if width > 0 and height > 0:
            visible_elements.append(element)
    
    return visible_elements


def find_elements_by_text(elements: List[Dict[str, Any]], text: str, exact_match: bool = False) -> List[Dict[str, Any]]:
    """
    Find elements containing specific text in name or label.
    
    Args:
        elements: List of element dictionaries
        text: Text to search for
        exact_match: Whether to use exact matching
        
    Returns:
        List of matching elements
    """
    matching_elements = []
    
    for element in elements:
        name = element.get('name', '').lower()
        label = element.get('label', '').lower()
        search_text = text.lower()
        
        if exact_match:
            if name == search_text or label == search_text:
                matching_elements.append(element)
        else:
            if search_text in name or search_text in label:
                matching_elements.append(element)
    
    return matching_elements


def get_element_hierarchy_path(element: Dict[str, Any], all_elements: List[Dict[str, Any]]) -> List[str]:
    """
    Get hierarchy path for an element (parent chain).
    
    Args:
        element: Target element
        all_elements: All elements in the tree
        
    Returns:
        List of element types in hierarchy path
    """
    # This is a simplified implementation
    # In a real scenario, we'd need parent-child relationships
    path = []
    element_type = element.get('type', '')
    if element_type:
        path.append(element_type)
    
    return path