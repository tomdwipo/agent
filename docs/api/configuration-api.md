# ⚙️ Configuration API Reference

This document provides comprehensive API documentation for the configuration system in the Audio Transcription Tool.

## Overview

The configuration system provides centralized management of application settings, environment variables, and constants. It consists of two main components:

- **Settings API**: Dynamic configuration from environment variables
- **Constants API**: Static application constants and defaults

---

## Settings API

The Settings API manages environment variables and provides validated configuration access.

### Class: `AppSettings`

**Location**: `config/settings.py`

#### Constructor

```python
AppSettings()
```

Automatically loads and validates all settings from environment variables.

**Example:**
```python
from config.settings import AppSettings

settings = AppSettings()
```

#### Properties

##### OpenAI Configuration

```python
settings.openai_api_key: str          # OpenAI API key
settings.openai_model: str            # Default: "gpt-4"
settings.openai_max_tokens: int       # Default: 1000
settings.openai_temperature: float    # Default: 0.3
```

##### Whisper Configuration

```python
settings.whisper_model: str           # Default: "base"
settings.whisper_fp16: bool           # Default: False
```

##### File Configuration

```python
settings.max_file_size_mb: int        # Default: 500
settings.temp_file_prefix: str        # Default: "transcription_"
settings.download_file_suffix: str    # Default: ".txt"
```

##### Gradio Configuration

```python
settings.gradio_server_name: str      # Default: "0.0.0.0"
settings.gradio_server_port: int      # Default: 7860
settings.gradio_share: bool           # Default: False
settings.gradio_debug: bool           # Default: True
settings.gradio_theme: str            # Default: "soft"
```

##### Application Configuration

```python
settings.app_title: str               # Default: "Audio Transcription with Whisper"
settings.app_description: str         # Application description
settings.enable_key_points: bool      # Default: True
```

##### PRD Configuration

```python
settings.enable_prd_generation: bool  # Default: True
settings.prd_openai_model: str        # Default: same as openai_model
settings.prd_max_tokens: int          # Default: 2000
settings.prd_temperature: float       # Default: 0.3
settings.prd_file_prefix: str         # Default: "PRD_"
```

##### Logging Configuration

```python
settings.log_level: str               # Default: "INFO"
settings.enable_logging: bool         # Default: True
```

#### Methods

##### `is_openai_configured()`

Check if OpenAI is properly configured.

**Returns:**
- `bool`: True if OpenAI API key is set and valid

**Example:**
```python
if settings.is_openai_configured():
    print("OpenAI is ready to use")
else:
    print("Please configure OpenAI API key")
```

##### `get_openai_config()`

Get OpenAI configuration as dictionary.

**Returns:**
- `Dict[str, Any]`: OpenAI configuration dictionary

**Example:**
```python
openai_config = settings.get_openai_config()
print(f"Model: {openai_config['model']}")
print(f"Max tokens: {openai_config['max_tokens']}")
```

**Return Structure:**
```python
{
    "api_key": "sk-...",
    "model": "gpt-4",
    "max_tokens": 1000,
    "temperature": 0.3
}
```

##### `get_whisper_config()`

Get Whisper configuration as dictionary.

**Returns:**
- `Dict[str, Any]`: Whisper configuration dictionary

**Example:**
```python
whisper_config = settings.get_whisper_config()
print(f"Model: {whisper_config['model']}")
```

##### `get_file_config()`

Get file handling configuration as dictionary.

**Returns:**
- `Dict[str, Any]`: File configuration dictionary

**Example:**
```python
file_config = settings.get_file_config()
print(f"Max size: {file_config['max_size_mb']}MB")
```

##### `get_gradio_config()`

Get Gradio UI configuration as dictionary.

**Returns:**
- `Dict[str, Any]`: Gradio configuration dictionary

**Example:**
```python
gradio_config = settings.get_gradio_config()
print(f"Port: {gradio_config['server_port']}")
```

##### `get_prd_config()`

Get PRD generation configuration as dictionary.

**Returns:**
- `Dict[str, Any]`: PRD configuration dictionary

**Example:**
```python
prd_config = settings.get_prd_config()
if prd_config['enabled']:
    print(f"PRD model: {prd_config['model']}")
```

##### `get_app_config()`

Get general application configuration as dictionary.

**Returns:**
- `Dict[str, Any]`: Application configuration dictionary

**Example:**
```python
app_config = settings.get_app_config()
print(f"Title: {app_config['title']}")
```

##### `validate_settings()`

Validate all settings and return any issues.

**Returns:**
- `Dict[str, str]`: Dictionary of validation issues (empty if all valid)

**Example:**
```python
issues = settings.validate_settings()
if issues:
    for key, issue in issues.items():
        print(f"❌ {key}: {issue}")
else:
    print("✅ All settings are valid")
```

##### `print_settings_summary()`

Print a formatted summary of current settings.

**Example:**
```python
settings.print_settings_summary()
```

**Output:**
```
🔧 Application Settings Summary
==================================================
App Title: Audio Transcription with Whisper
Whisper Model: base
OpenAI Configured: ✅
Key Points Enabled: ✅
PRD Generation Enabled: ✅
Max File Size: 500MB
Gradio Port: 7860
Debug Mode: ✅

✅ All settings are valid
```

### Class: `EnvironmentConfig`

**Location**: `config/settings.py`

Static methods for environment detection and project paths.

#### Methods

##### `get_environment()`

Get current environment name.

**Returns:**
- `str`: Environment name ("development", "production", "testing")

**Example:**
```python
from config.settings import EnvironmentConfig

env = EnvironmentConfig.get_environment()
print(f"Running in {env} environment")
```

##### `is_development()`, `is_production()`, `is_testing()`

Check specific environment types.

**Returns:**
- `bool`: True if running in specified environment

**Example:**
```python
if EnvironmentConfig.is_development():
    print("Development mode - debug enabled")
```

##### `get_project_root()`

Get project root directory path.

**Returns:**
- `Path`: Project root directory

**Example:**
```python
root = EnvironmentConfig.get_project_root()
config_file = root / "config" / "settings.py"
```

##### `get_env_file_path()`

Get .env file path.

**Returns:**
- `Path`: Path to .env file

**Example:**
```python
env_file = EnvironmentConfig.get_env_file_path()
if env_file.exists():
    print("Environment file found")
```

---

## Constants API

The Constants API provides static application constants and helper functions.

### Module: `config.constants`

**Location**: `config/constants.py`

#### Application Information

```python
APP_NAME: str = "Audio Transcription Tool"
APP_VERSION: str = "1.0.0"
APP_AUTHOR: str = "Audio Transcription Team"
APP_DESCRIPTION: str = "AI-powered audio transcription with meeting analysis"
```

#### Audio Format Constants

```python
SUPPORTED_AUDIO_EXTENSIONS: Set[str]  # {'.mp3', '.wav', '.m4a', ...}
SUPPORTED_AUDIO_FORMATS: List[str]    # ["MP3", "WAV", "M4A", ...]
AUDIO_MIME_TYPES: Dict[str, str]      # {'.mp3': 'audio/mpeg', ...}
```

#### Model Configuration

```python
WHISPER_MODELS: Dict[str, Dict[str, str]]  # Model info and capabilities
OPENAI_MODELS: Dict[str, Dict[str, str]]   # OpenAI model specifications
```

**Whisper Models:**
```python
{
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
    # ... more models
}
```

#### UI Constants

```python
UI_LABELS: Dict[str, str]        # UI text labels
UI_PLACEHOLDERS: Dict[str, str]  # Input placeholders
UI_INSTRUCTIONS: str             # User instructions
```

#### Error and Success Messages

```python
ERROR_MESSAGES: Dict[str, str]   # Error message templates
SUCCESS_MESSAGES: Dict[str, str] # Success message templates
```

#### Helper Functions

##### `get_version_string()`

Get formatted version string.

**Returns:**
- `str`: Formatted version (e.g., "1.0.0")

**Example:**
```python
from config.constants import get_version_string

version = get_version_string()
print(f"Version: {version}")
```

##### `get_supported_formats_string()`

Get comma-separated string of supported formats.

**Returns:**
- `str`: Formatted format list (e.g., "MP3, WAV, M4A, FLAC")

**Example:**
```python
from config.constants import get_supported_formats_string

formats = get_supported_formats_string()
print(f"Supported formats: {formats}")
```

##### `is_supported_audio_format(file_extension)`

Check if file extension is supported.

**Parameters:**
- `file_extension` (str): File extension (e.g., ".mp3")

**Returns:**
- `bool`: True if format is supported

**Example:**
```python
from config.constants import is_supported_audio_format

if is_supported_audio_format(".mp3"):
    print("MP3 is supported")
```

##### `get_whisper_model_info(model_name)`

Get information about a Whisper model.

**Parameters:**
- `model_name` (str): Model name (e.g., "base")

**Returns:**
- `Dict[str, str]`: Model information

**Example:**
```python
from config.constants import get_whisper_model_info

info = get_whisper_model_info("base")
print(f"Description: {info['description']}")
print(f"Speed: {info['speed']}")
```

##### `get_openai_model_info(model_name)`

Get information about an OpenAI model.

**Parameters:**
- `model_name` (str): Model name (e.g., "gpt-4")

**Returns:**
- `Dict[str, str]`: Model information

**Example:**
```python
from config.constants import get_openai_model_info

info = get_openai_model_info("gpt-4")
print(f"Max tokens: {info['max_tokens']}")
```

---

## Environment Variables Reference

### Required Variables

```bash
# OpenAI Configuration (required for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Optional Variables

#### Whisper Configuration
```bash
WHISPER_MODEL=base                    # tiny, base, small, medium, large
WHISPER_FP16=false                   # Enable FP16 for faster processing
```

#### OpenAI Configuration
```bash
OPENAI_MODEL=gpt-4                   # gpt-3.5-turbo, gpt-4, gpt-4-turbo
OPENAI_MAX_TOKENS=1000               # Maximum tokens for responses
OPENAI_TEMPERATURE=0.3               # Response creativity (0.0-2.0)
```

#### File Configuration
```bash
MAX_FILE_SIZE_MB=500                 # Maximum file size in MB
TEMP_FILE_PREFIX=transcription_      # Prefix for temporary files
DOWNLOAD_FILE_SUFFIX=.txt            # Suffix for download files
```

#### Gradio Configuration
```bash
GRADIO_SERVER_NAME=0.0.0.0          # Server bind address
GRADIO_SERVER_PORT=7860             # Server port
GRADIO_SHARE=false                  # Enable public sharing
GRADIO_DEBUG=true                   # Enable debug mode
GRADIO_THEME=soft                   # UI theme
```

#### Application Configuration
```bash
APP_TITLE=Audio Transcription Tool   # Application title
APP_DESCRIPTION=Custom description   # Application description
ENABLE_KEY_POINTS=true              # Enable key points feature
```

#### PRD Configuration
```bash
ENABLE_PRD_GENERATION=true          # Enable PRD generation
PRD_OPENAI_MODEL=gpt-4             # Model for PRD generation
PRD_MAX_TOKENS=2000                # Max tokens for PRD
PRD_TEMPERATURE=0.3                # Temperature for PRD generation
PRD_FILE_PREFIX=PRD_               # Prefix for PRD files
```

#### Logging Configuration
```bash
LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR, CRITICAL
ENABLE_LOGGING=true                 # Enable logging
```

#### Environment Detection
```bash
ENVIRONMENT=development             # development, production, testing
```

---

## Usage Examples

### Basic Configuration Access

```python
from config.settings import settings
from config.constants import SUPPORTED_AUDIO_FORMATS

# Check configuration
if settings.is_openai_configured():
    print("OpenAI is ready")

# Access specific settings
print(f"Whisper model: {settings.whisper_model}")
print(f"Max file size: {settings.max_file_size_mb}MB")
print(f"Supported formats: {SUPPORTED_AUDIO_FORMATS}")
```

### Configuration Validation

```python
from config.settings import settings

# Validate all settings
issues = settings.validate_settings()
if issues:
    print("Configuration issues found:")
    for key, issue in issues.items():
        print(f"  {key}: {issue}")
else:
    print("Configuration is valid")

# Print summary
settings.print_settings_summary()
```

### Environment-Specific Configuration

```python
from config.settings import EnvironmentConfig

if EnvironmentConfig.is_development():
    # Development-specific settings
    debug_mode = True
    verbose_logging = True
elif EnvironmentConfig.is_production():
    # Production-specific settings
    debug_mode = False
    verbose_logging = False
```

### Service Configuration

```python
from config.settings import settings

# Get service-specific configuration
openai_config = settings.get_openai_config()
whisper_config = settings.get_whisper_config()
file_config = settings.get_file_config()

# Use in services
from services.openai_service import OpenAIService
from services.whisper_service import WhisperService

openai_service = OpenAIService()  # Uses settings automatically
whisper = WhisperService(model_name=whisper_config['model'])
```

### Dynamic Configuration Updates

```python
import os
from config.settings import AppSettings

# Update environment variable
os.environ['WHISPER_MODEL'] = 'medium'

# Reload settings
settings = AppSettings()  # Will pick up new values
print(f"New model: {settings.whisper_model}")
```

---

## Configuration Best Practices

### Environment File Setup

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=sk-your-actual-api-key-here
WHISPER_MODEL=base
OPENAI_MODEL=gpt-4
MAX_FILE_SIZE_MB=500
GRADIO_SERVER_PORT=7860
ENABLE_PRD_GENERATION=true
```

### Validation and Error Handling

```python
from config.settings import settings

# Always validate before using
issues = settings.validate_settings()
if issues:
    # Handle configuration errors
    for key, issue in issues.items():
        print(f"Config error - {key}: {issue}")
    exit(1)

# Check service availability
if not settings.is_openai_configured():
    print("Warning: OpenAI features will be disabled")
```

### Service Integration

```python
# Services automatically use configuration
from services.whisper_service import WhisperService
from services.openai_service import OpenAIService

# No need to pass configuration manually
whisper = WhisperService()  # Uses settings.whisper_model
openai_service = OpenAIService()  # Uses settings.openai_* values
```

### Testing Configuration

```python
import os
from config.settings import AppSettings

# Override for testing
os.environ['WHISPER_MODEL'] = 'tiny'  # Faster for tests
os.environ['MAX_FILE_SIZE_MB'] = '10'  # Smaller for tests

test_settings = AppSettings()
assert test_settings.whisper_model == 'tiny'
```

---

## Legacy Functions

For backward compatibility, these legacy functions are available:

```python
from config.settings import get_openai_api_key, get_whisper_model_name, is_openai_available

# Legacy functions (use settings instance instead)
api_key = get_openai_api_key()
model = get_whisper_model_name()
available = is_openai_available()
```

---

## Global Instances

Pre-configured instances are available for immediate use:

```python
from config.settings import settings, env_config

# Use global instances
print(f"Model: {settings.whisper_model}")
print(f"Environment: {env_config.get_environment()}")
```

---

**Configuration API Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
