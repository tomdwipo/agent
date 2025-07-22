import unittest
import gradio as gr
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components import ComponentFactory, TRDOutputComponent

class TestTRDUIComponents(unittest.TestCase):
    """Test cases for TRD-related UI components"""

    def test_create_trd_output_component(self):
        """Test the creation of the TRD output component"""
        trd_output = ComponentFactory.create_trd_output()
        self.assertIsInstance(trd_output, gr.Textbox)
        self.assertEqual(trd_output.label, "Technical Requirements Document")

    def test_trd_output_component_custom_props(self):
        """Test TRD output component with custom properties"""
        trd_output_component = TRDOutputComponent(
            label="Custom TRD Label",
            placeholder="Custom TRD Placeholder",
            lines=30,
            max_lines=60
        )
        trd_output = trd_output_component.create()
        self.assertEqual(trd_output.label, "Custom TRD Label")
        self.assertEqual(trd_output.placeholder, "Custom TRD Placeholder")
        self.assertEqual(trd_output.lines, 30)
        self.assertEqual(trd_output.max_lines, 60)

if __name__ == '__main__':
    unittest.main()
