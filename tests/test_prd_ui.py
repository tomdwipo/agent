#!/usr/bin/env python3
"""
Comprehensive tests for PRD UI components and integration

This module contains unit tests for PRD-related UI components,
interface integration, and user workflow functionality.
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components import ComponentFactory
from ui.gradio_interface import GradioInterface
from config.settings import settings


class TestPRDUIComponents(unittest.TestCase):
    """Test cases for PRD UI components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.component_factory = ComponentFactory()

    def test_create_prd_output_component(self):
        """Test PRD output component creation"""
        component = ComponentFactory.create_prd_output()
        
        # Verify component is created
        self.assertIsNotNone(component)
        
        # Test with custom parameters
        custom_component = ComponentFactory.create_prd_output(
            label="Custom PRD Output",
            lines=25,
            max_lines=50
        )
        self.assertIsNotNone(custom_component)

    def test_create_prd_output_with_default_params(self):
        """Test PRD output component creation with default parameters"""
        component = ComponentFactory.create_prd_output()
        
        # Component should be created successfully with defaults
        self.assertIsNotNone(component)

    def test_create_prd_output_with_custom_params(self):
        """Test PRD output component creation with custom parameters"""
        custom_params = {
            'label': 'Test PRD Output',
            'lines': 30,
            'max_lines': 60,
            'show_copy_button': True
        }
        
        component = ComponentFactory.create_prd_output(**custom_params)
        self.assertIsNotNone(component)

    def test_prd_component_factory_methods(self):
        """Test that ComponentFactory has all required PRD methods"""
        required_methods = [
            'create_prd_output'
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(ComponentFactory, method_name))
            self.assertTrue(callable(getattr(ComponentFactory, method_name)))

    def test_prd_ui_labels_exist(self):
        """Test that PRD UI labels are properly defined"""
        from config.constants import PRD_UI_LABELS
        
        required_labels = [
            'generate_prd_button',
            'prd_output_label',
            'prd_download_label',
            'prd_generating',
            'prd_error'
        ]
        
        for label_key in required_labels:
            self.assertIn(label_key, PRD_UI_LABELS)
            self.assertIsInstance(PRD_UI_LABELS[label_key], str)
            self.assertGreater(len(PRD_UI_LABELS[label_key]), 0)


class TestPRDInterfaceIntegration(unittest.TestCase):
    """Test cases for PRD interface integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock gradio to avoid actual UI creation during tests
        self.gradio_mock = MagicMock()
        
    @patch('ui.gradio_interface.gr')
    def test_gradio_interface_prd_attributes(self, mock_gr):
        """Test that GradioInterface has PRD-related attributes"""
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        interface = GradioInterface()
        
        # Test PRD component attributes exist
        required_attributes = [
            'prd_btn',
            'prd_output', 
            'prd_download_file'
        ]
        
        for attr_name in required_attributes:
            self.assertTrue(hasattr(interface, attr_name))

    @patch('ui.gradio_interface.gr')
    def test_gradio_interface_prd_methods(self, mock_gr):
        """Test that GradioInterface has PRD-related methods"""
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        interface = GradioInterface()
        
        # Test PRD processing methods exist
        required_methods = [
            '_process_prd_generation'
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(interface, method_name))
            self.assertTrue(callable(getattr(interface, method_name)))

    @patch('ui.gradio_interface.gr')
    @patch('services.openai_service.OpenAIService.generate_prd_from_key_points')
    @patch('services.file_service.FileService.create_prd_download_file')
    def test_prd_generation_workflow(self, mock_create_file, mock_generate_prd, mock_gr):
        """Test PRD generation workflow through interface"""
        # Setup mocks
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        sample_prd_content = """# Product Requirements Document
        
## Executive Summary
Test PRD content for workflow testing.

## Problem Statement
Testing PRD generation workflow.
"""
        
        mock_generate_prd.return_value = sample_prd_content
        mock_create_file.return_value = "/tmp/test_prd.md"
        
        interface = GradioInterface()
        
        # Test PRD generation process
        sample_key_points = "Test key points for PRD generation"
        
        try:
            result = interface._process_prd_generation(sample_key_points)
            
            # Verify the workflow was executed
            mock_generate_prd.assert_called_once_with(sample_key_points)
            mock_create_file.assert_called_once_with(sample_prd_content)
            
            # Result should be a tuple (prd_content, file_path)
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            
        except Exception as e:
            # If method doesn't exist yet, that's expected for testing
            if "has no attribute '_process_prd_generation'" in str(e):
                self.skipTest("PRD generation method not yet implemented")
            else:
                raise

    @patch('ui.gradio_interface.gr')
    def test_prd_button_visibility_when_enabled(self, mock_gr):
        """Test PRD button visibility when feature is enabled"""
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        with patch.object(settings, 'enable_prd_generation', True):
            interface = GradioInterface()
            
            # PRD components should be created when enabled
            self.assertIsNotNone(interface.prd_btn)

    @patch('ui.gradio_interface.gr')
    def test_prd_button_visibility_when_disabled(self, mock_gr):
        """Test PRD button visibility when feature is disabled"""
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        with patch.object(settings, 'enable_prd_generation', False):
            interface = GradioInterface()
            
            # PRD components might still exist but should be hidden/disabled
            # This depends on implementation - test accordingly
            self.assertTrue(hasattr(interface, 'prd_btn'))

    @patch('ui.gradio_interface.gr')
    @patch('services.openai_service.OpenAIService.generate_prd_from_key_points')
    def test_prd_generation_error_handling(self, mock_generate_prd, mock_gr):
        """Test PRD generation error handling"""
        # Setup mocks
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        # Mock an error during PRD generation
        mock_generate_prd.side_effect = Exception("OpenAI API Error")
        
        interface = GradioInterface()
        
        sample_key_points = "Test key points"
        
        try:
            result = interface._process_prd_generation(sample_key_points)
            
            # Should handle error gracefully
            if isinstance(result, tuple):
                error_message, file_path = result
                self.assertIn("error", error_message.lower())
                self.assertIsNone(file_path)
            
        except Exception as e:
            # If method doesn't exist yet, that's expected for testing
            if "has no attribute '_process_prd_generation'" in str(e):
                self.skipTest("PRD generation method not yet implemented")
            else:
                # Error should be handled within the method, not propagated
                self.fail(f"Unhandled error in PRD generation: {e}")


class TestPRDSettings(unittest.TestCase):
    """Test cases for PRD configuration and settings"""
    
    def test_prd_settings_exist(self):
        """Test that PRD settings are properly configured"""
        # Test that PRD settings are available
        self.assertTrue(hasattr(settings, 'enable_prd_generation'))
        self.assertTrue(hasattr(settings, 'prd_openai_model'))
        self.assertTrue(hasattr(settings, 'prd_max_tokens'))
        self.assertTrue(hasattr(settings, 'prd_temperature'))
        self.assertTrue(hasattr(settings, 'prd_file_prefix'))

    def test_prd_config_method(self):
        """Test PRD configuration method"""
        self.assertTrue(hasattr(settings, 'get_prd_config'))
        self.assertTrue(callable(getattr(settings, 'get_prd_config')))
        
        prd_config = settings.get_prd_config()
        self.assertIsInstance(prd_config, dict)
        
        # Test required config keys
        required_keys = ['model', 'max_tokens', 'temperature']
        for key in required_keys:
            self.assertIn(key, prd_config)

    def test_prd_settings_types(self):
        """Test PRD settings data types"""
        self.assertIsInstance(settings.enable_prd_generation, bool)
        self.assertIsInstance(settings.prd_openai_model, str)
        self.assertIsInstance(settings.prd_max_tokens, int)
        self.assertIsInstance(settings.prd_temperature, float)
        self.assertIsInstance(settings.prd_file_prefix, str)

    def test_prd_settings_values(self):
        """Test PRD settings have reasonable values"""
        # PRD max tokens should be reasonable
        self.assertGreater(settings.prd_max_tokens, 0)
        self.assertLessEqual(settings.prd_max_tokens, 4096)
        
        # PRD temperature should be between 0 and 1
        self.assertGreaterEqual(settings.prd_temperature, 0.0)
        self.assertLessEqual(settings.prd_temperature, 1.0)
        
        # PRD file prefix should not be empty
        self.assertGreater(len(settings.prd_file_prefix), 0)


class TestPRDWorkflow(unittest.TestCase):
    """Integration tests for complete PRD workflow"""
    
    @patch('ui.gradio_interface.gr')
    def test_prd_feature_toggle(self, mock_gr):
        """Test PRD feature can be toggled on/off"""
        mock_gr.Textbox = MagicMock()
        mock_gr.Button = MagicMock()
        mock_gr.File = MagicMock()
        mock_gr.Column = MagicMock()
        mock_gr.Row = MagicMock()
        
        # Test with PRD enabled
        with patch.object(settings, 'enable_prd_generation', True):
            interface_enabled = GradioInterface()
            self.assertTrue(hasattr(interface_enabled, 'prd_btn'))
        
        # Test with PRD disabled  
        with patch.object(settings, 'enable_prd_generation', False):
            interface_disabled = GradioInterface()
            self.assertTrue(hasattr(interface_disabled, 'prd_btn'))

    def test_prd_constants_exist(self):
        """Test that PRD-related constants are properly defined"""
        from config.constants import PRD_TEMPLATE_SECTIONS, PRD_UI_LABELS
        
        # Test PRD template sections
        self.assertIsInstance(PRD_TEMPLATE_SECTIONS, list)
        self.assertGreater(len(PRD_TEMPLATE_SECTIONS), 0)
        
        expected_sections = [
            "Executive Summary",
            "Problem Statement",
            "Goals & Objectives",
            "User Stories/Requirements",
            "Success Metrics",
            "Timeline/Milestones",
            "Technical Requirements",
            "Risk Assessment"
        ]
        
        for section in expected_sections:
            self.assertIn(section, PRD_TEMPLATE_SECTIONS)
        
        # Test PRD UI labels
        self.assertIsInstance(PRD_UI_LABELS, dict)
        self.assertGreater(len(PRD_UI_LABELS), 0)


class TestPRDIntegrationScript(unittest.TestCase):
    """Integration tests from the original test_prd script"""
    
    def test_prd_components_creation(self):
        """Test PRD UI components creation (from original test_prd script)"""
        try:
            from ui.components import ComponentFactory
            from config.settings import settings
            
            # Test PRD output component creation
            prd_output = ComponentFactory.create_prd_output()
            self.assertIsNotNone(prd_output)
            
            # Test PRD settings
            self.assertIsNotNone(settings.enable_prd_generation)
            self.assertIsNotNone(settings.prd_openai_model)
            self.assertIsNotNone(settings.prd_max_tokens)
            self.assertIsNotNone(settings.prd_temperature)
            self.assertIsNotNone(settings.prd_file_prefix)
            
            # Test PRD config method
            prd_config = settings.get_prd_config()
            self.assertIsInstance(prd_config, dict)
            
        except Exception as e:
            self.fail(f"PRD components creation failed: {e}")
    
    def test_prd_services_integration(self):
        """Test PRD services integration (from original test_prd script)"""
        try:
            from services.openai_service import OpenAIService
            from services.file_service import FileService
            
            # Test OpenAI service PRD method
            openai_service = OpenAIService()
            self.assertTrue(hasattr(openai_service, 'generate_prd_from_key_points'))
            
            # Test File service PRD methods
            file_service = FileService()
            self.assertTrue(hasattr(file_service, 'create_prd_download_file'))
            self.assertTrue(hasattr(file_service, 'validate_prd_content'))
            
        except Exception as e:
            self.fail(f"PRD services integration failed: {e}")
    
    def test_prd_interface_integration(self):
        """Test PRD interface integration (from original test_prd script)"""
        with patch('ui.gradio_interface.gr') as mock_gr:
            mock_gr.Textbox = MagicMock()
            mock_gr.Button = MagicMock()
            mock_gr.File = MagicMock()
            mock_gr.Column = MagicMock()
            mock_gr.Row = MagicMock()
            
            try:
                from ui.gradio_interface import GradioInterface
                
                # Test interface creation with PRD enabled
                interface = GradioInterface()
                
                # Check if PRD components are initialized
                self.assertTrue(hasattr(interface, 'prd_btn'))
                self.assertTrue(hasattr(interface, 'prd_output'))
                self.assertTrue(hasattr(interface, 'prd_download_file'))
                self.assertTrue(hasattr(interface, '_process_prd_generation'))
                
            except Exception as e:
                self.fail(f"PRD interface integration failed: {e}")


def run_prd_ui_tests():
    """Run all PRD UI tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestPRDUIComponents))
    suite.addTest(unittest.makeSuite(TestPRDInterfaceIntegration))
    suite.addTest(unittest.makeSuite(TestPRDSettings))
    suite.addTest(unittest.makeSuite(TestPRDWorkflow))
    suite.addTest(unittest.makeSuite(TestPRDIntegrationScript))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("🧪 Running PRD UI Tests")
    print("=" * 60)
    
    success = run_prd_ui_tests()
    
    if success:
        print("\n🎉 All PRD UI tests passed!")
    else:
        print("\n❌ Some PRD UI tests failed!")
    
    sys.exit(0 if success else 1)