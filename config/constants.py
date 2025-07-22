"""
Constants Configuration Module

Centralizes application constants, default values, and static configurations.
"""

from typing import Set, Dict, List

# Application Information
APP_NAME = "Audio Transcription Tool"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Audio Transcription Team"
APP_DESCRIPTION = "AI-powered audio transcription with meeting analysis"

# Supported Audio Formats
SUPPORTED_AUDIO_EXTENSIONS: Set[str] = {
    '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma', '.mp4', '.mov', '.avi'
}

SUPPORTED_AUDIO_FORMATS: List[str] = [
    "MP3", "WAV", "M4A", "FLAC", "AAC", "OGG", "WMA", "MP4", "MOV", "AVI"
]

# File Size Limits
DEFAULT_MAX_FILE_SIZE_MB = 500
DEFAULT_MAX_FILE_SIZE_BYTES = DEFAULT_MAX_FILE_SIZE_MB * 1024 * 1024
MIN_FILE_SIZE_BYTES = 1024  # 1KB minimum

# Whisper Model Configuration
WHISPER_MODELS: Dict[str, Dict[str, str]] = {
    "tiny": {
        "name": "tiny",
        "description": "Fastest, least accurate (~39 MB)",
        "languages": "English-only",
        "speed": "Very Fast"
    },
    "base": {
        "name": "base", 
        "description": "Good balance of speed and accuracy (~74 MB)",
        "languages": "Multilingual",
        "speed": "Fast"
    },
    "small": {
        "name": "small",
        "description": "Better accuracy, slower (~244 MB)",
        "languages": "Multilingual", 
        "speed": "Medium"
    },
    "medium": {
        "name": "medium",
        "description": "High accuracy (~769 MB)",
        "languages": "Multilingual",
        "speed": "Slow"
    },
    "large": {
        "name": "large",
        "description": "Highest accuracy (~1550 MB)",
        "languages": "Multilingual",
        "speed": "Very Slow"
    },
    "large-v2": {
        "name": "large-v2",
        "description": "Latest large model with improvements (~1550 MB)",
        "languages": "Multilingual",
        "speed": "Very Slow"
    },
    "large-v3": {
        "name": "large-v3",
        "description": "Most recent large model (~1550 MB)",
        "languages": "Multilingual",
        "speed": "Very Slow"
    }
}

DEFAULT_WHISPER_MODEL = "base"
WHISPER_MODEL_NAMES = list(WHISPER_MODELS.keys())

# OpenAI Configuration
OPENAI_MODELS: Dict[str, Dict[str, str]] = {
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "description": "Fast and cost-effective",
        "max_tokens": 4096,
        "cost": "Low"
    },
    "gpt-4": {
        "name": "gpt-4",
        "description": "More capable, higher quality",
        "max_tokens": 8192,
        "cost": "High"
    },
    "gpt-4-turbo": {
        "name": "gpt-4-turbo",
        "description": "Latest GPT-4 with improved performance",
        "max_tokens": 128000,
        "cost": "Medium"
    }
}

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
DEFAULT_OPENAI_MAX_TOKENS = 1000
DEFAULT_OPENAI_TEMPERATURE = 0.3

# Gradio UI Configuration
GRADIO_THEMES = ["default", "soft", "monochrome", "glass", "base"]
DEFAULT_GRADIO_THEME = "soft"
DEFAULT_GRADIO_PORT = 7860
DEFAULT_GRADIO_SERVER_NAME = "0.0.0.0"

# UI Text and Labels
UI_LABELS = {
    "app_title": "🎵 Audio Transcription Tool",
    "upload_label": "Upload Audio File",
    "transcribe_button": "🎯 Transcribe Audio",
    "key_points_button": "🔑 Generate Key Meeting Points",
    "prd_button": "📋 Generate PRD",
    "transcription_label": "Transcription Result",
    "key_points_label": "Key Meeting Points",
    "prd_label": "Product Requirements Document",
    "download_label": "Download Transcription",
    "download_prd_label": "Download PRD (.md)",
    "instructions_title": "📝 Instructions:",
    "status_processing": "Processing...",
    "status_complete": "✅ Complete",
    "status_error": "❌ Error",
    "prd_generating": "Generating PRD...",
    "prd_complete": "✅ PRD Generated"
}

UI_PLACEHOLDERS = {
    "transcription": "Transcription will appear here...",
    "key_points": "Key meeting points will appear here after generating...",
    "prd": "Generated PRD will appear here...",
    "upload_audio": "Click to upload an audio file"
}

UI_INSTRUCTIONS = """
1. Click on the audio upload area above to select your audio file
2. Supported formats: MP3, WAV, M4A, FLAC, and more
3. Click 'Transcribe Audio' to start the process
4. The transcription will appear in the text area below
5. Click 'Generate Key Meeting Points' to get AI-powered meeting summary
6. You can copy both the transcription and key points, or download the transcription as a .txt file

**Note:** To use the key meeting points feature, you need to add your OpenAI API key to the .env file.
"""

# PRD Configuration
PRD_TEMPLATE_SECTIONS = [
    "Executive Summary",
    "Problem Statement", 
    "Goals & Objectives",
    "User Stories/Requirements",
    "Success Metrics",
    "Timeline/Milestones",
    "Technical Requirements",
    "Risk Assessment"
]

DEFAULT_PRD_MAX_TOKENS = 2000
DEFAULT_PRD_TEMPERATURE = 0.3
DEFAULT_PRD_FILE_PREFIX = "PRD_"

# TRD Configuration
TRD_SECTIONS = [
    "Architecture Overview",
    "UI/UX Specifications", 
    "API Requirements",
    "Database Schema",
    "Security Requirements",
    "Performance Requirements",
    "Testing Strategy"
]
DEFAULT_TRD_MAX_TOKENS = 3000
DEFAULT_TRD_TEMPERATURE = 0.2
DEFAULT_TRD_FILE_PREFIX = "TRD_Android_"

# Error Messages
ERROR_MESSAGES = {
    "no_file": "Please upload an audio file.",
    "invalid_format": "Unsupported audio format. Please use: {formats}",
    "file_too_large": "File too large. Maximum size: {max_size}MB",
    "file_not_found": "File not found: {file_path}",
    "transcription_failed": "Transcription failed: {error}",
    "openai_not_configured": "❌ OpenAI API key not configured. Please add your API key to the .env file.",
    "openai_not_available": "❌ OpenAI library not installed. Please install it with: pip install openai",
    "openai_request_failed": "❌ Error generating key meeting points: {error}",
    "no_transcription": "Please transcribe audio first before generating key meeting points.",
    "no_key_points": "Please generate key meeting points first before creating PRD.",
    "prd_generation_failed": "❌ Error generating PRD: {error}",
    "prd_feature_disabled": "❌ PRD generation feature is disabled.",
    "no_prd_content": "Please provide PRD content before generating TRD.",
    "trd_generation_failed": "❌ Error generating TRD: {error}",
    "trd_feature_disabled": "❌ TRD generation feature is disabled.",
    "model_load_failed": "Failed to load Whisper model: {error}",
    "file_creation_failed": "Failed to create temporary file: {error}"
}

# Success Messages
SUCCESS_MESSAGES = {
    "transcription_complete": "✅ Transcription completed successfully!",
    "key_points_generated": "✅ Key points generated successfully!",
    "file_saved": "✅ File saved: {file_path}",
    "model_loaded": "✅ Model loaded successfully",
    "service_available": "✅ Service is available and configured"
}

# File Extensions and MIME Types
AUDIO_MIME_TYPES = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.m4a': 'audio/mp4',
    '.flac': 'audio/flac',
    '.aac': 'audio/aac',
    '.ogg': 'audio/ogg',
    '.wma': 'audio/x-ms-wma'
}

# Temporary File Configuration
TEMP_FILE_SETTINGS = {
    "prefix": "transcription_",
    "suffix": ".txt",
    "key_points_suffix": "_keypoints.txt",
    "encoding": "utf-8",
    "cleanup_on_exit": True
}

# Logging Configuration
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# API Rate Limits and Timeouts
API_TIMEOUTS = {
    "openai_request": 60,  # seconds
    "whisper_transcription": 300,  # seconds
    "file_upload": 120  # seconds
}

# Environment Variables
ENV_VARS = {
    "required": [
        "OPENAI_API_KEY"  # Only required if using key points or PRD features
    ],
    "optional": [
        "WHISPER_MODEL",
        "OPENAI_MODEL", 
        "MAX_FILE_SIZE_MB",
        "GRADIO_SERVER_PORT",
        "GRADIO_SHARE",
        "GRADIO_DEBUG",
        "LOG_LEVEL",
        "ENABLE_PRD_GENERATION",
        "PRD_OPENAI_MODEL",
        "PRD_MAX_TOKENS",
        "PRD_TEMPERATURE",
        "PRD_FILE_PREFIX",
        "ENABLE_TRD_GENERATION",
        "TRD_OPENAI_MODEL",
        "TRD_MAX_TOKENS",
        "TRD_TEMPERATURE",
        "TRD_FILE_PREFIX"
    ]
}

# Feature Flags
FEATURES = {
    "key_points_generation": True,
    "prd_generation": True,
    "trd_generation": True,
    "custom_analysis": True,
    "file_validation": True,
    "model_caching": True,
    "temp_file_cleanup": True,
    "settings_validation": True
}

# Development and Testing
DEV_SETTINGS = {
    "debug_mode": True,
    "verbose_logging": True,
    "mock_openai": False,
    "test_audio_file": "test_audio.mp3"
}

# Production Settings
PROD_SETTINGS = {
    "debug_mode": False,
    "verbose_logging": False,
    "enable_analytics": True,
    "security_headers": True
}

# Version Information
VERSION_INFO = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "pre_release": None,
    "build": None
}

def get_version_string() -> str:
    """Get formatted version string"""
    version = f"{VERSION_INFO['major']}.{VERSION_INFO['minor']}.{VERSION_INFO['patch']}"
    if VERSION_INFO['pre_release']:
        version += f"-{VERSION_INFO['pre_release']}"
    if VERSION_INFO['build']:
        version += f"+{VERSION_INFO['build']}"
    return version

def get_supported_formats_string() -> str:
    """Get comma-separated string of supported formats"""
    return ", ".join(SUPPORTED_AUDIO_FORMATS)

def is_supported_audio_format(file_extension: str) -> bool:
    """Check if file extension is supported"""
    return file_extension.lower() in SUPPORTED_AUDIO_EXTENSIONS

def get_whisper_model_info(model_name: str) -> Dict[str, str]:
    """Get information about a Whisper model"""
    return WHISPER_MODELS.get(model_name, WHISPER_MODELS[DEFAULT_WHISPER_MODEL])

def get_openai_model_info(model_name: str) -> Dict[str, str]:
    """Get information about an OpenAI model"""
    return OPENAI_MODELS.get(model_name, OPENAI_MODELS[DEFAULT_OPENAI_MODEL])
