# 🔧 Services API Reference

This document provides comprehensive API documentation for all service classes in the Audio Transcription Tool.

## Overview

The services layer provides the core business logic and external service integration. All services follow consistent patterns for initialization, error handling, and return values.

---

## WhisperService

Audio transcription service using OpenAI Whisper models.

### Class: `WhisperService`

**Location**: `services/whisper_service.py`

#### Constructor

```python
WhisperService(model_name=None)
```

**Parameters:**
- `model_name` (str, optional): Whisper model name (`tiny`, `base`, `small`, `medium`, `large`). If None, uses configuration setting.

**Example:**
```python
from services.whisper_service import WhisperService

# Use default model from configuration
whisper = WhisperService()

# Use specific model
whisper = WhisperService(model_name="base")
```

#### Methods

##### `load_model()`

Load and cache the Whisper model.

**Returns:**
- `whisper.Whisper`: Loaded Whisper model instance

**Example:**
```python
model = whisper.load_model()
```

##### `transcribe_audio(audio_path)`

Transcribe an audio file using the loaded Whisper model.

**Parameters:**
- `audio_path` (str): Path to the audio file

**Returns:**
- `tuple`: `(transcription_text, temp_file_path)` on success, `(error_message, None)` on error

**Example:**
```python
transcription, temp_file = whisper.transcribe_audio("meeting.mp3")
if temp_file:
    print(f"Transcription: {transcription}")
    print(f"Download file: {temp_file}")
else:
    print(f"Error: {transcription}")
```

##### `transcribe_for_gradio(audio_file)`

Transcribe audio specifically for Gradio interface.

**Parameters:**
- `audio_file`: Gradio audio file object or path

**Returns:**
- `tuple`: `(transcription_text, temp_file_path)` on success, `(error_message, None)` on error

**Example:**
```python
# In Gradio interface
def transcribe_handler(audio_file):
    return whisper.transcribe_for_gradio(audio_file)
```

#### Supported Models

| Model | Size | Speed | Accuracy | Languages |
|-------|------|-------|----------|-----------|
| `tiny` | ~39 MB | Very Fast | Basic | English-only |
| `base` | ~74 MB | Fast | Good | Multilingual |
| `small` | ~244 MB | Medium | Better | Multilingual |
| `medium` | ~769 MB | Slow | High | Multilingual |
| `large` | ~1550 MB | Very Slow | Highest | Multilingual |

#### Error Handling

Common error scenarios:
- Invalid model name: Falls back to default model
- Missing audio file: Returns error message
- Transcription failure: Returns detailed error message

---

## OpenAIService

AI-powered analysis service for generating meeting insights and PRDs.

### Class: `OpenAIService`

**Location**: `services/openai_service.py`

#### Constructor

```python
OpenAIService()
```

**Example:**
```python
from services.openai_service import OpenAIService

openai_service = OpenAIService()
```

#### Methods

##### `is_available()`

Check if OpenAI service is available and configured.

**Returns:**
- `bool`: True if OpenAI is available and configured

**Example:**
```python
if openai_service.is_available():
    # Use OpenAI features
    pass
else:
    print("OpenAI not configured")
```

##### `get_availability_status()`

Get detailed availability status message.

**Returns:**
- `str`: Detailed status message explaining availability

**Example:**
```python
status = openai_service.get_availability_status()
print(status)  # "✅ OpenAI service is available and configured."
```

##### `generate_meeting_key_points(transcription_text, model=None)`

Generate structured meeting key points from transcription.

**Parameters:**
- `transcription_text` (str): The transcription text to analyze
- `model` (str, optional): OpenAI model to use. If None, uses configuration setting.

**Returns:**
- `str`: Generated key meeting points in structured format, or error message

**Example:**
```python
key_points = openai_service.generate_meeting_key_points(transcription)
print(key_points)
```

**Output Format:**
```markdown
## 📋 Meeting Summary
[2-3 sentence summary]

## 🎯 Key Topics Discussed
• Topic 1
• Topic 2

## ✅ Action Items
• Action item 1 - Person responsible
• Action item 2 - Person responsible

## 🔑 Decisions Made
• Decision 1
• Decision 2

## 🚀 Next Steps
• Next step 1
• Next step 2

## 👥 Participants
• Participant names
```

##### `generate_prd_from_key_points(key_points_text, model=None)`

Generate a Product Requirements Document from meeting key points.

**Parameters:**
- `key_points_text` (str): The meeting key points text to analyze
- `model` (str, optional): OpenAI model to use. If None, uses configuration setting.

**Returns:**
- `str`: Generated PRD in markdown format, or error message

**Example:**
```python
prd_content = openai_service.generate_prd_from_key_points(key_points)
print(prd_content)
```

**PRD Structure:**
1. Executive Summary
2. Problem Statement
3. Goals & Objectives
4. User Stories/Requirements
5. Success Metrics
6. Timeline/Milestones
7. Technical Requirements
8. Risk Assessment

##### `generate_custom_analysis(transcription_text, custom_prompt, model="gpt-3.5-turbo")`

Generate custom analysis using a user-defined prompt.

**Parameters:**
- `transcription_text` (str): The transcription text to analyze
- `custom_prompt` (str): Custom prompt for analysis
- `model` (str): OpenAI model to use (default: "gpt-3.5-turbo")

**Returns:**
- `str`: Generated analysis or error message

**Example:**
```python
custom_prompt = "Extract all technical terms and their definitions from this meeting."
analysis = openai_service.generate_custom_analysis(transcription, custom_prompt)
```

#### Configuration

The service uses these configuration settings:
- `OPENAI_API_KEY`: Required API key
- `OPENAI_MODEL`: Default model (e.g., "gpt-3.5-turbo", "gpt-4")
- `OPENAI_MAX_TOKENS`: Maximum tokens for responses
- `OPENAI_TEMPERATURE`: Response creativity (0.0-1.0)

#### Error Handling

Common error scenarios:
- Missing API key: Returns configuration error message
- Invalid model: Uses fallback model
- API request failure: Returns detailed error message
- Empty input: Returns validation error message

---

## FileService

File handling, validation, and download operations service.

### Class: `FileService`

**Location**: `services/file_service.py`

#### Constructor

```python
FileService()
```

**Example:**
```python
from services.file_service import FileService

file_service = FileService()
```

#### Methods

##### `validate_audio_file(file_path)`

Validate if a file is a supported audio format.

**Parameters:**
- `file_path` (str): Path to the audio file

**Returns:**
- `tuple`: `(is_valid, error_message)` where `is_valid` is bool

**Example:**
```python
is_valid, message = file_service.validate_audio_file("audio.mp3")
if is_valid:
    print("File is valid")
else:
    print(f"Validation error: {message}")
```

**Validation Checks:**
- File existence
- Supported format (MP3, WAV, M4A, FLAC, AAC, OGG, WMA)
- File size limits

##### `get_file_info(file_path)`

Get detailed information about a file.

**Parameters:**
- `file_path` (str): Path to the file

**Returns:**
- `dict`: File information or None if error

**Example:**
```python
info = file_service.get_file_info("audio.mp3")
if info:
    print(f"Name: {info['name']}")
    print(f"Size: {info['size_mb']} MB")
    print(f"Extension: {info['extension']}")
```

**Return Structure:**
```python
{
    'name': 'audio.mp3',
    'size': 1024000,  # bytes
    'size_mb': 1.02,
    'extension': '.mp3',
    'modified': 1640995200.0,  # timestamp
    'path': '/path/to/audio.mp3'
}
```

##### `create_temp_text_file(content, suffix=None, prefix=None)`

Create a temporary text file with given content.

**Parameters:**
- `content` (str): Content to write to the file
- `suffix` (str, optional): File suffix (default from configuration)
- `prefix` (str, optional): File prefix (default from configuration)

**Returns:**
- `str`: Path to created temporary file, or None if failed

**Example:**
```python
temp_file = file_service.create_temp_text_file("Hello World", suffix=".txt")
if temp_file:
    print(f"Created: {temp_file}")
```

##### `create_prd_download_file(prd_content, filename=None)`

Create a downloadable PRD file in markdown format.

**Parameters:**
- `prd_content` (str): The PRD content in markdown format
- `filename` (str, optional): Custom filename (auto-generated if not provided)

**Returns:**
- `str`: Path to created PRD file, or None if failed

**Example:**
```python
prd_file = file_service.create_prd_download_file(prd_content)
if prd_file:
    print(f"PRD saved: {prd_file}")
```

**File Naming:**
- Auto-generated: `PRD_YYYY-MM-DD_HH-MM.md`
- Custom: Uses provided filename with `.md` extension

##### `validate_prd_content(prd_content)`

Validate PRD content structure and completeness.

**Parameters:**
- `prd_content` (str): PRD content to validate

**Returns:**
- `tuple`: `(is_valid, validation_message)` where `is_valid` is bool

**Example:**
```python
is_valid, message = file_service.validate_prd_content(prd_content)
if is_valid:
    print("PRD is valid")
else:
    print(f"Validation issues: {message}")
```

**Validation Checks:**
- Required sections presence
- Minimum content length
- Structure validation

##### `cleanup_temp_file(file_path)`

Clean up a temporary file.

**Parameters:**
- `file_path` (str): Path to the temporary file

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = file_service.cleanup_temp_file(temp_file)
```

#### Supported Audio Formats

| Format | Extension | MIME Type |
|--------|-----------|-----------|
| MP3 | `.mp3` | `audio/mpeg` |
| WAV | `.wav` | `audio/wav` |
| M4A | `.m4a` | `audio/mp4` |
| FLAC | `.flac` | `audio/flac` |
| AAC | `.aac` | `audio/aac` |
| OGG | `.ogg` | `audio/ogg` |
| WMA | `.wma` | `audio/x-ms-wma` |

#### Error Handling

Common error scenarios:
- File not found: Returns specific error message
- Unsupported format: Lists supported formats
- File too large: Shows size limit
- Permission errors: Returns access error message

---

## Legacy Functions

For backward compatibility, the following legacy functions are available:

### WhisperService Legacy Functions

```python
from services.whisper_service import load_whisper_model, transcribe_audio_gradio

# Legacy functions (use WhisperService class instead)
model = load_whisper_model()
result = transcribe_audio_gradio(audio_file)
```

### OpenAIService Legacy Functions

```python
from services.openai_service import generate_meeting_key_points, generate_prd_from_key_points

# Legacy functions (use OpenAIService class instead)
key_points = generate_meeting_key_points(transcription)
prd = generate_prd_from_key_points(key_points)
```

### FileService Legacy Functions

```python
from services.file_service import validate_audio_file, create_prd_download_file

# Legacy functions (use FileService class instead)
is_valid, msg = validate_audio_file(file_path)
prd_file = create_prd_download_file(content)
```

---

## Best Practices

### Service Initialization
```python
# Initialize services once and reuse
whisper = WhisperService()
openai_service = OpenAIService()
file_service = FileService()
```

### Error Handling
```python
# Always check availability for OpenAI features
if openai_service.is_available():
    result = openai_service.generate_meeting_key_points(text)
else:
    print("OpenAI not configured")

# Validate files before processing
is_valid, message = file_service.validate_audio_file(file_path)
if not is_valid:
    print(f"File validation failed: {message}")
    return
```

### Resource Management
```python
# Clean up temporary files
temp_file = file_service.create_temp_text_file(content)
try:
    # Use temp_file
    pass
finally:
    file_service.cleanup_temp_file(temp_file)
```

### Configuration
```python
# Use configuration settings
from config.settings import settings

# Services automatically use configuration
whisper = WhisperService()  # Uses settings.whisper_model
openai_service = OpenAIService()  # Uses settings.openai_model
```

---

**Services API Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
