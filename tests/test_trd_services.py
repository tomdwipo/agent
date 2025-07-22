#!/usr/bin/env python3
"""
Comprehensive tests for TRD services

This module contains unit tests for TRD-related services including
OpenAIService TRD generation.
"""

import unittest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import OpenAIService
from config.settings import settings
from config.constants import TRD_SECTIONS

class TestTRDServices(unittest.TestCase):
    """Test cases for TRD-related services"""

    def setUp(self):
        """Set up test fixtures"""
        self.openai_service = OpenAIService()
        self.sample_prd_content = """
# Product Requirements Document

## Executive Summary
A mobile app that allows users to track their daily water intake.

## User Stories
- As a user, I want to log my water consumption.
- As a user, I want to see my daily progress.
"""
        self.sample_trd_content = """
# Technical Requirements Document

## 1. Architecture Overview
- **App Architecture Pattern**: MVVM (Model-View-ViewModel)
- **Core Components**: Activities, Fragments, ViewModels, Repositories

## 2. UI/UX Specifications
- **Screen Hierarchy**: Main screen with water log, progress view.
- **UI Components**: Custom progress bar, RecyclerView for logs.

## 3. API Requirements
- No external APIs needed for this version.

## 4. Database Schema
- **Local Database**: Room
- **Entities**: WaterLog (id, amount, timestamp)

## 5. Security Requirements
- No sensitive data stored.

## 6. Performance Requirements
- App should launch in under 2 seconds.

## 7. Testing Strategy
- **Unit Testing**: ViewModels and Repositories.
- **UI Testing**: Espresso tests for user flows.
"""

    def test_openai_service_has_trd_method(self):
        """Test that OpenAIService has TRD generation method"""
        self.assertTrue(hasattr(self.openai_service, 'generate_android_trd_from_prd'))
        self.assertTrue(callable(getattr(self.openai_service, 'generate_android_trd_from_prd')))

    @patch('services.openai_service.OpenAIService._initialize_client')
    @patch('openai.OpenAI')
    def test_generate_trd_from_prd_success(self, mock_openai, mock_init_client):
        """Test successful TRD generation from PRD content"""
        # Arrange
        service = OpenAIService()
        mock_client = unittest.mock.MagicMock()
        service.client = mock_client
        
        mock_choice = unittest.mock.Mock()
        mock_choice.message.content = self.sample_trd_content
        mock_response = unittest.mock.Mock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        # Act
        result = service.generate_android_trd_from_prd(self.sample_prd_content)

        # Assert
        self.assertIsInstance(result, str)
        for section in TRD_SECTIONS:
            self.assertIn(section, result)
        mock_client.chat.completions.create.assert_called_once()

    def test_generate_trd_with_empty_prd_content(self):
        """Test TRD generation with empty PRD content"""
        result = self.openai_service.generate_android_trd_from_prd("")
        self.assertIn("Please provide PRD content", result)

    @patch('services.openai_service.OpenAIService._initialize_client')
    @patch('openai.OpenAI')
    def test_generate_trd_api_failure(self, mock_openai, mock_init_client):
        """Test TRD generation when OpenAI API fails"""
        # Arrange
        service = OpenAIService()
        mock_client = unittest.mock.MagicMock()
        service.client = mock_client
        mock_client.chat.completions.create.side_effect = Exception("OpenAI API Error")

        # Act
        result = service.generate_android_trd_from_prd(self.sample_prd_content)

        # Assert
        self.assertIn("Error generating TRD", result)
        self.assertIn("OpenAI API Error", result)

    def test_trd_settings_integration(self):
        """Test TRD services integration with settings"""
        self.assertIsNotNone(settings.trd_openai_model)
        self.assertIsNotNone(settings.trd_max_tokens)
        self.assertIsNotNone(settings.trd_temperature)
        self.assertIsNotNone(settings.trd_file_prefix)

        trd_config = settings.get_trd_config()
        self.assertIsInstance(trd_config, dict)
        self.assertIn('model', trd_config)
        self.assertIn('max_tokens', trd_config)
        self.assertIn('temperature', trd_config)

if __name__ == '__main__':
    unittest.main()
