"""
Test package for Audio Transcription Tool with PRD Generation

This package contains comprehensive tests for all components of the
Audio Transcription Tool, including the PRD generation feature.
"""

__version__ = "1.0.0"
__author__ = "Audio Transcription Tool Team"

# Test modules
from .test_prd_services import TestPRDServices, TestPRDIntegration
from .test_prd_ui import TestPRDUIComponents, TestPRDInterfaceIntegration, TestPRDIntegrationScript

__all__ = [
    'TestPRDServices',
    'TestPRDIntegration', 
    'TestPRDUIComponents',
    'TestPRDInterfaceIntegration',
    'TestPRDIntegrationScript'
]