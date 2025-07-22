import unittest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import OpenAIService
from services.file_service import FileService
from ui.gradio_interface import GradioInterface

class TestTRDIntegration(unittest.TestCase):
    """Integration tests for the complete TRD workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.openai_service = OpenAIService()
        self.file_service = FileService()
        self.gradio_interface = GradioInterface()
        self.sample_prd_content = """
# Product Requirements Document

## Executive Summary
A mobile app that allows users to track their daily water intake.
"""
        self.sample_trd_content = """
# Technical Requirements Document

## Architecture Overview
- MVVM
## UI/UX Specifications
- Main screen
## API Requirements
- None
## Database Schema
- Room
## Security Requirements
- None
## Performance Requirements
- Fast
## Testing Strategy
- Unit tests
"""

    @patch('services.openai_service.OpenAIService.is_available', return_value=True)
    @patch('services.openai_service.OpenAIService.generate_android_trd_from_prd')
    def test_full_trd_workflow(self, mock_generate_trd, mock_is_available):
        """Test the full PRD to TRD workflow"""
        # Arrange
        mock_generate_trd.return_value = self.sample_trd_content

        # Act
        trd_content, download_file = self.gradio_interface._process_trd_generation(self.sample_prd_content)

        # Assert
        self.assertEqual(trd_content, self.sample_trd_content)
        self.assertTrue(download_file.visible)
        print(download_file.value)
        self.assertTrue(os.path.exists(download_file.value['path']))

if __name__ == '__main__':
    unittest.main()
