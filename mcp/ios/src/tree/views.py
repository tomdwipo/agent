"""
iOS Tree Views

Visualization and representation utilities for iOS UI trees.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass 
class ElementView:
    """View representation of a single iOS element."""
    
    index: int
    element_type: str
    name: str
    label: str
    bounds: tuple
    center: tuple
    interactive: bool
    
    def __str__(self) -> str:
        """String representation of element view."""
        result = f"{self.index}. {self.element_type}"
        
        if self.name:
            result += f" '{self.name}'"
        if self.label and self.label != self.name:
            result += f" [{self.label}]"
        
        result += f" at {self.bounds}"
        if self.interactive:
            result += " (interactive)"
        
        return result


class TreeView:
    """View manager for iOS UI trees."""
    
    def __init__(self, tree_state):
        """Initialize with tree state."""
        self.tree_state = tree_state
    
    def get_interactive_elements_view(self) -> List[ElementView]:
        """Get view representation of interactive elements."""
        views = []
        
        for i, element in enumerate(self.tree_state.interactive_elements):
            view = ElementView(
                index=i + 1,
                element_type=element.className,
                name=element.name,
                label=element.label,
                bounds=element.bounds,
                center=element.center,
                interactive=element.interactive
            )
            views.append(view)
        
        return views
    
    def format_elements_list(self) -> str:
        """Format interactive elements as a readable list."""
        views = self.get_interactive_elements_view()
        
        if not views:
            return "No interactive elements found."
        
        result = f"Found {len(views)} interactive elements:\n\n"
        for view in views:
            result += f"{view}\n"
        
        return result
    
    def get_summary(self) -> str:
        """Get summary of the tree state."""
        return (
            f"iOS UI Tree Summary:\n"
            f"Window Size: {self.tree_state.window_size}\n"
            f"Orientation: {self.tree_state.orientation}\n"
            f"Total Elements: {len(self.tree_state.elements)}\n"
            f"Interactive Elements: {len(self.tree_state.interactive_elements)}\n"
        )