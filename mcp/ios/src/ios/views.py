"""
iOS Views Module

Contains classes for representing iOS device state and UI structure.
"""

from typing import Optional
from dataclasses import dataclass
from src.tree import TreeState


@dataclass
class IOSState:
    """Represents the current state of an iOS device."""
    
    tree_state: TreeState
    screenshot: Optional[bytes] = None
    
    def __str__(self) -> str:
        """String representation of the iOS state."""
        result = f"iOS Device State:\n"
        result += f"Tree State: {self.tree_state}\n"
        result += f"Screenshot: {'Available' if self.screenshot else 'Not available'}"
        return result