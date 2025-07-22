import unittest
import os
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.file_service import FileService
from config.constants import TRD_SECTIONS

class TestTRDFileService(unittest.TestCase):
    """Test cases for TRD-related file services"""

    def setUp(self):
        """Set up test fixtures"""
        self.file_service = FileService()
        self.sample_trd_content = """
# Technical Requirements Document

## Architecture Overview
- **App Architecture Pattern**: MVVM

## UI/UX Specifications
- **Screen Hierarchy**: Main screen

## API Requirements
- No external APIs needed.

## Database Schema
- **Local Database**: Room

## Security Requirements
- No sensitive data.

## Performance Requirements
- App launch in under 2s.

## Testing Strategy
- **Unit Testing**: ViewModels.
- **Lorem Ipsum**: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede.
"""

    def test_create_trd_download_file(self):
        """Test creating a TRD download file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override the temp directory for testing
            with patch('tempfile.gettempdir', return_value=temp_dir):
                file_path = self.file_service.create_trd_download_file(self.sample_trd_content)
                self.assertTrue(os.path.exists(file_path))
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertEqual(content, self.sample_trd_content)

    def test_validate_trd_content_valid(self):
        """Test validating valid TRD content"""
        is_valid, message = self.file_service.validate_trd_content(self.sample_trd_content)
        self.assertTrue(is_valid)
        self.assertEqual(message, "TRD content is valid")

    def test_validate_trd_content_empty(self):
        """Test validating empty TRD content"""
        is_valid, message = self.file_service.validate_trd_content("")
        self.assertFalse(is_valid)
        self.assertEqual(message, "TRD content is empty")

    def test_validate_trd_content_missing_sections(self):
        """Test validating TRD content with missing sections"""
        incomplete_content = "# Technical Requirements Document\n\n## 1. Architecture Overview\n- MVVM"
        is_valid, message = self.file_service.validate_trd_content(incomplete_content)
        self.assertFalse(is_valid)
        self.assertIn("Missing required sections", message)

    def test_validate_trd_content_too_short(self):
        """Test validating TRD content that is too short"""
        short_content = """
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
        is_valid, message = self.file_service.validate_trd_content(short_content)
        self.assertFalse(is_valid)
        self.assertEqual(message, "TRD content appears to be too short")

if __name__ == '__main__':
    unittest.main()
