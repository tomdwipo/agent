"""
Settings Configuration Module

Centralizes environment variables, API configurations, and application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()


def _clean_env_value(value: str) -> str:
    """
    Clean environment variable value by removing comments and whitespace.
    
    Args:
        value: Raw environment variable value
        
    Returns:
        Cleaned value with comments and extra whitespace removed
    """
    if not value:
        return value
    
    # Remove inline comments (anything after #)
    if '#' in value:
        value = value.split('#')[0]
    
    # Strip whitespace
    return value.strip()


def _get_env_int(key: str, default: str) -> int:
    """
    Safely get an integer environment variable.
    
    Args:
        key: Environment variable key
        default: Default value as string
        
    Returns:
        Integer value
        
    Raises:
        ValueError: If the value cannot be converted to int
    """
    raw_value = os.getenv(key, default)
    clean_value = _clean_env_value(raw_value)
    
    try:
        return int(clean_value)
    except ValueError as e:
        raise ValueError(f"Invalid integer value for {key}: '{raw_value}' (cleaned: '{clean_value}')") from e


def _get_env_float(key: str, default: str) -> float:
    """
    Safely get a float environment variable.
    
    Args:
        key: Environment variable key
        default: Default value as string
        
    Returns:
        Float value
        
    Raises:
        ValueError: If the value cannot be converted to float
    """
    raw_value = os.getenv(key, default)
    clean_value = _clean_env_value(raw_value)
    
    try:
        return float(clean_value)
    except ValueError as e:
        raise ValueError(f"Invalid float value for {key}: '{raw_value}' (cleaned: '{clean_value}')") from e


def _get_env_str(key: str, default: str) -> str:
    """
    Safely get a string environment variable.
    
    Args:
        key: Environment variable key
        default: Default value
        
    Returns:
        Cleaned string value
    """
    raw_value = os.getenv(key, default)
    return _clean_env_value(raw_value)


class AppSettings:
    """Application settings and configuration management"""
    
    def __init__(self):
        """Initialize application settings"""
        self._load_settings()
    
    def _load_settings(self):
        """Load all settings from environment variables"""
        # OpenAI Configuration
        self.openai_api_key = _get_env_str("OPENAI_API_KEY", "")
        self.openai_model = _get_env_str("OPENAI_MODEL", "gpt-3.5-turbo")
        self.openai_max_tokens = _get_env_int("OPENAI_MAX_TOKENS", "1000")
        self.openai_temperature = _get_env_float("OPENAI_TEMPERATURE", "0.3")
        
        # Whisper Configuration
        self.whisper_model = _get_env_str("WHISPER_MODEL", "base")
        self.whisper_fp16 = _get_env_str("WHISPER_FP16", "false").lower() == "true"
        
        # File Configuration
        self.max_file_size_mb = _get_env_int("MAX_FILE_SIZE_MB", "500")
        self.temp_file_prefix = _get_env_str("TEMP_FILE_PREFIX", "transcription_")
        self.download_file_suffix = _get_env_str("DOWNLOAD_FILE_SUFFIX", ".txt")
        
        # Gradio Configuration
        self.gradio_server_name = _get_env_str("GRADIO_SERVER_NAME", "0.0.0.0")
        self.gradio_server_port = _get_env_int("GRADIO_SERVER_PORT", "7860")
        self.gradio_share = _get_env_str("GRADIO_SHARE", "false").lower() == "true"
        self.gradio_debug = _get_env_str("GRADIO_DEBUG", "true").lower() == "true"
        self.gradio_theme = _get_env_str("GRADIO_THEME", "soft")
        
        # Application Configuration
        self.app_title = _get_env_str("APP_TITLE", "Audio Transcription with Whisper")
        self.app_description = _get_env_str("APP_DESCRIPTION", "Upload an audio file (MP3, WAV, etc.) and get the transcription using OpenAI's Whisper model.")
        self.enable_key_points = _get_env_str("ENABLE_KEY_POINTS", "true").lower() == "true"
        
        # PRD Configuration
        self.enable_prd_generation = _get_env_str("ENABLE_PRD_GENERATION", "true").lower() == "true"
        self.prd_openai_model = _get_env_str("PRD_OPENAI_MODEL", self.openai_model)
        self.prd_max_tokens = _get_env_int("PRD_MAX_TOKENS", "2000")
        self.prd_temperature = _get_env_float("PRD_TEMPERATURE", "0.3")
        self.prd_file_prefix = _get_env_str("PRD_FILE_PREFIX", "PRD_")
        
        # Logging Configuration
        self.log_level = _get_env_str("LOG_LEVEL", "INFO")
        self.enable_logging = _get_env_str("ENABLE_LOGGING", "true").lower() == "true"
    
    def is_openai_configured(self) -> bool:
        """Check if OpenAI is properly configured"""
        return bool(self.openai_api_key and self.openai_api_key != "sk-your-openai-api-key-here")
    
    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI configuration as dictionary"""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "max_tokens": self.openai_max_tokens,
            "temperature": self.openai_temperature
        }
    
    def get_whisper_config(self) -> Dict[str, Any]:
        """Get Whisper configuration as dictionary"""
        return {
            "model": self.whisper_model,
            "fp16": self.whisper_fp16
        }
    
    def get_file_config(self) -> Dict[str, Any]:
        """Get file handling configuration as dictionary"""
        return {
            "max_size_mb": self.max_file_size_mb,
            "max_size_bytes": self.max_file_size_mb * 1024 * 1024,
            "temp_prefix": self.temp_file_prefix,
            "download_suffix": self.download_file_suffix
        }
    
    def get_gradio_config(self) -> Dict[str, Any]:
        """Get Gradio configuration as dictionary"""
        return {
            "server_name": self.gradio_server_name,
            "server_port": self.gradio_server_port,
            "share": self.gradio_share,
            "debug": self.gradio_debug,
            "theme": self.gradio_theme,
            "title": self.app_title,
            "description": self.app_description
        }
    
    def get_prd_config(self) -> Dict[str, Any]:
        """Get PRD configuration as dictionary"""
        return {
            "enabled": self.enable_prd_generation,
            "model": self.prd_openai_model,
            "max_tokens": self.prd_max_tokens,
            "temperature": self.prd_temperature,
            "file_prefix": self.prd_file_prefix
        }
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get general application configuration as dictionary"""
        return {
            "title": self.app_title,
            "description": self.app_description,
            "enable_key_points": self.enable_key_points,
            "enable_prd_generation": self.enable_prd_generation,
            "log_level": self.log_level,
            "enable_logging": self.enable_logging
        }
    
    def validate_settings(self) -> Dict[str, str]:
        """Validate all settings and return any issues"""
        issues = {}
        
        # Validate OpenAI settings
        if self.enable_key_points and not self.is_openai_configured():
            issues["openai"] = "OpenAI API key not configured but key points feature is enabled"
        
        # Validate PRD settings
        if self.enable_prd_generation and not self.is_openai_configured():
            issues["prd_openai"] = "OpenAI API key not configured but PRD generation feature is enabled"
        
        if self.prd_max_tokens <= 0:
            issues["prd_tokens"] = "PRD max tokens must be greater than 0"
        
        if not (0.0 <= self.prd_temperature <= 2.0):
            issues["prd_temperature"] = "PRD temperature must be between 0.0 and 2.0"
        
        # Validate Whisper settings
        valid_whisper_models = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
        if self.whisper_model not in valid_whisper_models:
            issues["whisper_model"] = f"Invalid Whisper model: {self.whisper_model}. Valid options: {valid_whisper_models}"
        
        # Validate file settings
        if self.max_file_size_mb <= 0:
            issues["file_size"] = "Maximum file size must be greater than 0"
        
        # Validate Gradio settings
        if not (1 <= self.gradio_server_port <= 65535):
            issues["gradio_port"] = "Gradio server port must be between 1 and 65535"
        
        return issues
    
    def print_settings_summary(self):
        """Print a summary of current settings"""
        print("🔧 Application Settings Summary")
        print("=" * 50)
        print(f"App Title: {self.app_title}")
        print(f"Whisper Model: {self.whisper_model}")
        print(f"OpenAI Configured: {'✅' if self.is_openai_configured() else '❌'}")
        print(f"Key Points Enabled: {'✅' if self.enable_key_points else '❌'}")
        print(f"PRD Generation Enabled: {'✅' if self.enable_prd_generation else '❌'}")
        print(f"Max File Size: {self.max_file_size_mb}MB")
        print(f"Gradio Port: {self.gradio_server_port}")
        print(f"Debug Mode: {'✅' if self.gradio_debug else '❌'}")
        
        # Check for issues
        issues = self.validate_settings()
        if issues:
            print("\n⚠️  Configuration Issues:")
            for key, issue in issues.items():
                print(f"  - {key}: {issue}")
        else:
            print("\n✅ All settings are valid")


class EnvironmentConfig:
    """Environment-specific configuration"""
    
    @staticmethod
    def get_environment() -> str:
        """Get current environment (development, production, testing)"""
        return os.getenv("ENVIRONMENT", "development").lower()
    
    @staticmethod
    def is_development() -> bool:
        """Check if running in development environment"""
        return EnvironmentConfig.get_environment() == "development"
    
    @staticmethod
    def is_production() -> bool:
        """Check if running in production environment"""
        return EnvironmentConfig.get_environment() == "production"
    
    @staticmethod
    def is_testing() -> bool:
        """Check if running in testing environment"""
        return EnvironmentConfig.get_environment() == "testing"
    
    @staticmethod
    def get_project_root() -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent
    
    @staticmethod
    def get_env_file_path() -> Path:
        """Get .env file path"""
        return EnvironmentConfig.get_project_root() / ".env"


# Global settings instance
settings = AppSettings()
env_config = EnvironmentConfig()

# Legacy functions for backward compatibility
def get_openai_api_key() -> Optional[str]:
    """Legacy function to get OpenAI API key"""
    return settings.openai_api_key if settings.is_openai_configured() else None

def get_whisper_model_name() -> str:
    """Legacy function to get Whisper model name"""
    return settings.whisper_model

def is_openai_available() -> bool:
    """Legacy function to check OpenAI availability"""
    return settings.is_openai_configured()
