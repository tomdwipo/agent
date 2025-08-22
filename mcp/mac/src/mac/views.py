"""
Mac Views Module

Contains classes for representing Mac desktop state and UI structure.
"""

from typing import Optional
from dataclasses import dataclass
from src.page import PageState


@dataclass
class MacState:
    """Represents the current state of a Mac desktop."""
    
    desktop_state: PageState
    screenshot: Optional[bytes] = None
    
    def __str__(self) -> str:
        """String representation of the Mac state."""
        result = f"Mac Desktop State:\n"
        result += f"Desktop State: {self.desktop_state}\n"
        result += f"Screenshot: {'Available' if self.screenshot else 'Not available'}"
        return result