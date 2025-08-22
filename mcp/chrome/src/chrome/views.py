"""
Chrome Views Module

Contains classes for representing Chrome browser state and page structure.
"""

from typing import Optional
from dataclasses import dataclass
from src.page import PageState


@dataclass
class ChromeState:
    """Represents the current state of a Chrome browser."""
    
    page_state: PageState
    screenshot: Optional[bytes] = None
    
    def __str__(self) -> str:
        """String representation of the Chrome state."""
        result = f"Chrome Browser State:\n"
        result += f"Page State: {self.page_state}\n"
        result += f"Screenshot: {'Available' if self.screenshot else 'Not available'}"
        return result