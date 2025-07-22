# 📖 API Reference

Welcome to the Audio Transcription Tool API Reference. This documentation provides comprehensive information about all available APIs, services, and components.

## 📋 API Overview

The Audio Transcription Tool provides a clean, modular API architecture with three main layers:

### Service Layer APIs
Core business logic and external service integration:
- **[WhisperService](services-api.md#whisperservice)**: Audio transcription using OpenAI Whisper models
- **[OpenAIService](services-api.md#openaiservice)**: AI-powered analysis, key points, and PRD generation
- **[FileService](services-api.md#fileservice)**: File handling, validation, and download operations

### Configuration APIs
Centralized settings and constants management:
- **[Settings API](configuration-api.md#settings-api)**: Environment variable loading and validation
- **[Constants API](configuration-api.md#constants-api)**: Application constants and helper functions

### UI Component APIs
User interface components and interaction handling:
- **[ComponentFactory](ui-components-api.md#componentfactory)**: Factory pattern for UI component creation
- **[Interface APIs](ui-components-api.md#interface-apis)**: Standard, Simple, and Custom interface implementations

## 🚀 Quick Start

### Basic Service Usage

```python
# Import services
from services.whisper_service import WhisperService
from services.openai_service import OpenAIService
from services.file_service import FileService

# Initialize services
whisper = WhisperService()
openai_service = OpenAIService()
file_service = FileService()

# Basic transcription workflow
transcription, temp_file = whisper.transcribe_audio("audio.mp3")
key_points = openai_service.generate_meeting_key_points(transcription)
prd_content = openai_service.generate_prd_from_key_points(key_points)
prd_file = file_service.create_prd_download_file(prd_content)
```

### Configuration Usage

```python
# Import configuration
from config.settings import settings
from config.constants import SUPPORTED_AUDIO_FORMATS

# Access configuration
print(f"Whisper model: {settings.whisper_model}")
print(f"OpenAI available: {settings.is_openai_configured()}")
print(f"Supported formats: {SUPPORTED_AUDIO_FORMATS}")
```

### UI Component Usage

```python
# Import UI components
from ui.components import ComponentFactory
from ui.gradio_interface import create_gradio_interface

# Create components
audio_input = ComponentFactory.create_audio_input()
transcription_output = ComponentFactory.create_transcription_output()

# Create interface
interface = create_gradio_interface('standard')
interface.launch()
```

## 📚 API Documentation Structure

### [Services API Reference](services-api.md)
Complete documentation for all service classes and methods:
- Method signatures and parameters
- Return values and error handling
- Usage examples and best practices
- Configuration options

### [Configuration API Reference](configuration-api.md)
Settings and constants management:
- Environment variable configuration
- Settings validation and access
- Constants and helper functions
- Configuration examples

### [UI Components API Reference](ui-components-api.md)
User interface components and factories:
- Component creation and customization
- Interface types and implementations
- Event handling and interactions
- Styling and theming options

## 🔧 API Design Principles

### Consistency
- Uniform method naming conventions
- Consistent parameter patterns
- Standardized return value formats
- Common error handling approaches

### Modularity
- Independent service components
- Reusable UI components
- Configurable behavior
- Clean separation of concerns

### Extensibility
- Plugin-friendly architecture
- Customizable components
- Configurable settings
- Easy integration points

### Error Handling
- Comprehensive error messages
- Graceful degradation
- Validation at all levels
- Clear error reporting

## 🎯 Common Use Cases

### Audio Transcription
```python
# Simple transcription
whisper = WhisperService()
result, temp_file = whisper.transcribe_audio("meeting.mp3")
```

### AI Analysis
```python
# Generate meeting insights
openai_service = OpenAIService()
if openai_service.is_available():
    key_points = openai_service.generate_meeting_key_points(transcription)
```

### PRD Generation
```python
# Create Product Requirements Document
prd_content = openai_service.generate_prd_from_key_points(key_points)
prd_file = file_service.create_prd_download_file(prd_content)
```

### File Operations
```python
# Validate and process files
is_valid, message = file_service.validate_audio_file("audio.mp3")
file_info = file_service.get_file_info("audio.mp3")
```

### Custom UI
```python
# Create custom interface
custom_interface = create_gradio_interface('custom', {
    'audio_input': {'label': 'Upload Meeting Recording'},
    'transcription_output': {'lines': 20}
})
```

## 📊 API Status and Versioning

### Current API Version
- **Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: January 2025

### API Stability
- **Services API**: ✅ Stable (v1.0)
- **Configuration API**: ✅ Stable (v1.0)
- **UI Components API**: ✅ Stable (v1.0)

### Versioning Policy
- **Major Version**: Breaking changes to public APIs
- **Minor Version**: New features, backward compatible
- **Patch Version**: Bug fixes and improvements

## 🔗 Related Documentation

- **[Main README](../../README.md)**: Project overview and quick start
- **[Architecture Documentation](../architecture/)**: Technical architecture details
- **[Feature Documentation](../features/)**: Feature specifications and status
- **[Development Guide](../development/)**: Setup and contribution guidelines

## 📞 API Support

### Getting Help
1. **Check Documentation**: Review the specific API documentation
2. **Code Examples**: See usage examples in each API section
3. **Demo Scripts**: Run demo scripts in the `demos/` directory
4. **GitHub Issues**: Report bugs or request features

### Best Practices
- Always check service availability before using OpenAI features
- Validate file inputs before processing
- Handle errors gracefully in your applications
- Use configuration settings for customization
- Follow the established patterns for consistency

---

**API Documentation Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
