#!/usr/bin/env python3
"""
Comprehensive tests for PRD services

This module contains unit tests for PRD-related services including
OpenAIService PRD generation and FileService PRD file handling.
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, mock_open
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import OpenAIService
from services.file_service import FileService
from config.settings import settings


class TestPRDServices(unittest.TestCase):
    """Test cases for PRD-related services"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.openai_service = OpenAIService()
        self.file_service = FileService()
        self.sample_key_points = """
        Meeting Key Points:
        - Discussed new dashboard feature for user analytics
        - Need real-time data visualization
        - Target 40% increase in user engagement
        - Timeline: 10 weeks total
        - Technical stack: React.js with WebSocket integration
        - Risk: API performance under high load
        """
        self.sample_prd_content = """# Product Requirements Document
*Generated from meeting analysis*

## Executive Summary
New user dashboard feature with real-time analytics.

## Problem Statement
Users need better access to key metrics.

## Goals & Objectives
- Increase user engagement by 40%
- Improve data visibility

## User Stories/Requirements
- As a user, I want to see real-time metrics
- As an admin, I need customizable widgets

## Success Metrics
- User engagement: 40% increase
- Dashboard adoption: 80%

## Timeline/Milestones
- Phase 1 (Weeks 1-2): Design
- Phase 2 (Weeks 3-6): Development

## Technical Requirements
- React.js frontend
- WebSocket for real-time data

## Risk Assessment
- Risk: API performance
- Mitigation: Caching and rate limiting
"""

    def test_openai_service_has_prd_method(self):
        """Test that OpenAIService has PRD generation method"""
        self.assertTrue(hasattr(self.openai_service, 'generate_prd_from_key_points'))
        self.assertTrue(callable(getattr(self.openai_service, 'generate_prd_from_key_points')))

    @patch('services.openai_service.OpenAIService._make_openai_request')
    def test_generate_prd_from_key_points_success(self, mock_request):
        """Test successful PRD generation from key points"""
        # Mock OpenAI response
        mock_request.return_value = self.sample_prd_content
        
        # Test PRD generation
        result = self.openai_service.generate_prd_from_key_points(self.sample_key_points)
        
        # Assertions
        self.assertIsInstance(result, str)
        self.assertIn("Product Requirements Document", result)
        self.assertIn("Executive Summary", result)
        self.assertIn("Problem Statement", result)
        self.assertIn("Goals & Objectives", result)
        
        # Verify the OpenAI request was called with correct parameters
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertIn(self.sample_key_points, str(call_args))

    @patch('services.openai_service.OpenAIService._make_openai_request')
    def test_generate_prd_with_custom_model(self, mock_request):
        """Test PRD generation with custom OpenAI model"""
        mock_request.return_value = self.sample_prd_content
        
        custom_model = "gpt-4-turbo"
        result = self.openai_service.generate_prd_from_key_points(
            self.sample_key_points,
            model=custom_model
        )
        
        self.assertIsInstance(result, str)
        mock_request.assert_called_once()

    @patch('services.openai_service.OpenAIService._make_openai_request')
    def test_generate_prd_api_failure(self, mock_request):
        """Test PRD generation when OpenAI API fails"""
        mock_request.side_effect = Exception("OpenAI API Error")
        
        with self.assertRaises(Exception) as context:
            self.openai_service.generate_prd_from_key_points(self.sample_key_points)
        
        self.assertIn("OpenAI API Error", str(context.exception))

    def test_file_service_has_prd_methods(self):
        """Test that FileService has PRD-related methods"""
        self.assertTrue(hasattr(self.file_service, 'create_prd_download_file'))
        self.assertTrue(callable(getattr(self.file_service, 'create_prd_download_file')))
        
        self.assertTrue(hasattr(self.file_service, 'validate_prd_content'))
        self.assertTrue(callable(getattr(self.file_service, 'validate_prd_content')))

    def test_create_prd_download_file_success(self):
        """Test successful PRD file creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override the temp directory for testing
            with patch('tempfile.gettempdir', return_value=temp_dir):
                result_path = self.file_service.create_prd_download_file(self.sample_prd_content)
                
                # Verify file was created
                self.assertTrue(os.path.exists(result_path))
                self.assertTrue(result_path.endswith('.md'))
                
                # Verify file content
                with open(result_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertEqual(content, self.sample_prd_content)

    def test_create_prd_download_file_with_custom_filename(self):
        """Test PRD file creation with custom filename"""
        custom_filename = "custom_prd_test.md"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('tempfile.gettempdir', return_value=temp_dir):
                result_path = self.file_service.create_prd_download_file(
                    self.sample_prd_content,
                    filename=custom_filename
                )
                
                self.assertTrue(os.path.exists(result_path))
                self.assertIn(custom_filename, result_path)

    def test_create_prd_download_file_auto_filename(self):
        """Test PRD file creation with auto-generated filename"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('tempfile.gettempdir', return_value=temp_dir):
                result_path = self.file_service.create_prd_download_file(self.sample_prd_content)
                
                filename = os.path.basename(result_path)
                self.assertTrue(filename.startswith(settings.prd_file_prefix))
                self.assertTrue(filename.endswith('.md'))
                
                # Check that timestamp is in filename
                current_date = datetime.now().strftime('%Y-%m-%d')
                self.assertIn(current_date, filename)

    def test_validate_prd_content_valid(self):
        """Test PRD content validation with valid content"""
        is_valid, message = self.file_service.validate_prd_content(self.sample_prd_content)
        
        self.assertTrue(is_valid)
        self.assertEqual(message, "PRD content is valid")

    def test_validate_prd_content_empty(self):
        """Test PRD content validation with empty content"""
        is_valid, message = self.file_service.validate_prd_content("")
        
        self.assertFalse(is_valid)
        self.assertIn("empty", message.lower())

    def test_validate_prd_content_missing_sections(self):
        """Test PRD content validation with missing required sections"""
        incomplete_prd = "# Product Requirements Document\n\nOnly has title."
        
        is_valid, message = self.file_service.validate_prd_content(incomplete_prd)
        
        self.assertFalse(is_valid)
        self.assertIn("missing", message.lower())

    def test_prd_file_creation_permissions_error(self):
        """Test PRD file creation when permissions are denied"""
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = PermissionError("Permission denied")
            
            with self.assertRaises(Exception) as context:
                self.file_service.create_prd_download_file(self.sample_prd_content)
            
            self.assertIn("Permission denied", str(context.exception))

    def test_prd_generation_with_empty_key_points(self):
        """Test PRD generation with empty key points"""
        with patch('services.openai_service.OpenAIService._make_openai_request') as mock_request:
            mock_request.side_effect = Exception("Invalid input: key points cannot be empty")
            
            with self.assertRaises(Exception):
                self.openai_service.generate_prd_from_key_points("")

    def test_prd_content_encoding(self):
        """Test PRD file creation with special characters"""
        special_content = self.sample_prd_content + "\n\n特殊字符测试 éñcódíng tëst 🚀✨"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('tempfile.gettempdir', return_value=temp_dir):
                result_path = self.file_service.create_prd_download_file(special_content)
                
                # Verify file was created and content is preserved
                self.assertTrue(os.path.exists(result_path))
                
                with open(result_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertEqual(content, special_content)

    def test_prd_settings_integration(self):
        """Test PRD services integration with settings"""
        # Test that services respect configuration settings
        self.assertIsNotNone(settings.prd_openai_model)
        self.assertIsNotNone(settings.prd_max_tokens)
        self.assertIsNotNone(settings.prd_temperature)
        self.assertIsNotNone(settings.prd_file_prefix)
        
        # Test PRD config method
        prd_config = settings.get_prd_config()
        self.assertIsInstance(prd_config, dict)
        self.assertIn('model', prd_config)
        self.assertIn('max_tokens', prd_config)
        self.assertIn('temperature', prd_config)


class TestPRDIntegration(unittest.TestCase):
    """Integration tests for PRD services working together"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.openai_service = OpenAIService()
        self.file_service = FileService()
        self.sample_key_points = """
        Product meeting notes:
        - Building mobile app for task management
        - Target small business owners
        - Key features: task creation, team collaboration, deadline tracking
        - Launch timeline: 6 months
        - Success metric: 1000 active users in first quarter
        """

    @patch('services.openai_service.OpenAIService._make_openai_request')
    def test_full_prd_workflow(self, mock_request):
        """Test complete PRD generation and file creation workflow"""
        # Mock successful PRD generation
        mock_prd_content = """# Product Requirements Document

## Executive Summary
Mobile task management app for small businesses.

## Problem Statement
Small businesses need better task organization.

## Goals & Objectives
- Launch within 6 months
- Achieve 1000 active users

## User Stories/Requirements
- Task creation and management
- Team collaboration features
- Deadline tracking

## Success Metrics
- 1000 active users in Q1
- User satisfaction > 4.5/5

## Timeline/Milestones
- Month 1-2: Design phase
- Month 3-5: Development
- Month 6: Launch

## Technical Requirements
- Mobile-first responsive design
- Cloud-based synchronization

## Risk Assessment
- Market competition
- User adoption challenges
"""
        mock_request.return_value = mock_prd_content
        
        # Step 1: Generate PRD from key points
        prd_content = self.openai_service.generate_prd_from_key_points(self.sample_key_points)
        self.assertIsInstance(prd_content, str)
        self.assertIn("Product Requirements Document", prd_content)
        
        # Step 2: Validate PRD content
        is_valid, message = self.file_service.validate_prd_content(prd_content)
        self.assertTrue(is_valid)
        
        # Step 3: Create downloadable file
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('tempfile.gettempdir', return_value=temp_dir):
                file_path = self.file_service.create_prd_download_file(prd_content)
                
                # Verify end-to-end workflow
                self.assertTrue(os.path.exists(file_path))
                self.assertTrue(file_path.endswith('.md'))
                
                # Verify file content matches generated PRD
                with open(file_path, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                    self.assertEqual(saved_content, prd_content)


def run_prd_tests():
    """Run all PRD service tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestPRDServices))
    suite.addTest(unittest.makeSuite(TestPRDIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("🧪 Running PRD Services Tests")
    print("=" * 60)
    
    success = run_prd_tests()
    
    if success:
        print("\n🎉 All PRD service tests passed!")
    else:
        print("\n❌ Some PRD service tests failed!")
    
    sys.exit(0 if success else 1)