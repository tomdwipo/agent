# 🎵 Audio Transcription Tool

A powerful, production-ready audio transcription application built with OpenAI Whisper and enhanced with AI-powered meeting analysis and PRD generation. This project features a clean, service-oriented architecture with configurable UI components and comprehensive customization options.

**Version 1.0.0** - Production Ready ✅

## ✨ Features

### Core Functionality
- **🎯 Audio Transcription**: High-quality transcription using OpenAI Whisper models
- **🔑 AI Meeting Analysis**: Generate key meeting points, action items, and summaries using OpenAI GPT
- **📋 PRD Generation**: Transform meeting discussions into structured Product Requirements Documents
- **🤖 Android TRD Generation**: Convert PRDs into comprehensive Android Technical Requirements Documents
- **📁 Multi-Format Support**: MP3, WAV, M4A, FLAC, AAC, OGG, WMA, MP4, MOV, AVI
- **💾 Download Options**: Export transcriptions as text files, PRDs and TRDs as markdown files
- **⚙️ Configurable Settings**: Extensive customization through environment variables

### Enhanced Workflow
```
Audio File → Transcription → Key Points → PRD Generation → Android TRD Generation → Download (.md)
```

**PRD Generation Workflow:**
```
Audio File → Transcription → Key Points → PRD Generation → Download PRD (.md)
```

**NEW: Android TRD Generation Workflow:**
```
PRD Content → Android TRD Generation → Download TRD (.md)
```

**Complete UI Integration:**
- ✅ PRD output component with copy functionality
- ✅ Generate PRD button in main interface
- ✅ Automatic .md file download
- ✅ Error handling and validation
- ✅ Seamless workflow integration

**8-Section PRD Template:**
- Executive Summary
- Problem Statement  
- Goals & Objectives
- User Stories/Requirements
- Success Metrics
- Timeline/Milestones
- Technical Requirements
- Risk Assessment

### Interface Options
- **🖥️ Standard Interface**: Full-featured web interface with all capabilities
- **⚡ Simple Interface**: Lightweight interface for basic transcription
- **🛠️ Custom Interface**: Fully customizable for specialized workflows
- **📱 Responsive Design**: Works on desktop and mobile devices

### Architecture Highlights
- **🏗️ Modular Services**: Independent, reusable service components
- **⚙️ Configuration Management**: Centralized settings with validation
- **🎨 Component-Based UI**: Reusable, customizable interface components
- **🔧 Developer-Friendly**: Clean APIs and comprehensive documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd audio-transcription-tool
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key
   ```


   ```bash
   uv run transcribe_gradio.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:7860`

## 📋 Requirements

```
gradio>=4.0.0
openai-whisper>=20231117
openai>=1.0.0
python-dotenv>=1.0.0
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required for AI meeting analysis
OPENAI_API_KEY=your-openai-api-key-here

# Optional configurations
WHISPER_MODEL=base                    # tiny, base, small, medium, large
OPENAI_MODEL=gpt-3.5-turbo           # gpt-3.5-turbo, gpt-4, gpt-4-turbo
MAX_FILE_SIZE_MB=500                 # Maximum file size in MB
GRADIO_SERVER_PORT=7860              # Web interface port
GRADIO_THEME=soft                    # soft, default, monochrome, glass
ENABLE_KEY_POINTS=true               # Enable/disable AI analysis
APP_TITLE=Audio Transcription Tool   # Custom application title

# PRD Feature Configuration
ENABLE_PRD_GENERATION=true           # Enable/disable PRD feature
PRD_OPENAI_MODEL=gpt-4              # OpenAI model for PRD generation
PRD_MAX_TOKENS=2000                 # Maximum tokens for PRD generation
PRD_TEMPERATURE=0.3                 # Temperature for PRD generation (more structured)
PRD_FILE_PREFIX=PRD_                # Prefix for downloaded PRD files

# TRD Feature Configuration
ENABLE_TRD_GENERATION=true           # Enable/disable TRD feature
TRD_OPENAI_MODEL=gpt-4              # OpenAI model for TRD generation
TRD_MAX_TOKENS=3000                 # Maximum tokens for TRD generation
TRD_TEMPERATURE=0.2                 # Temperature for TRD generation (more structured)
TRD_FILE_PREFIX=TRD_Android_        # Prefix for downloaded TRD files
```

### Whisper Models

| Model | Size | Speed | Accuracy | Languages |
|-------|------|-------|----------|-----------|
| `tiny` | ~39 MB | Very Fast | Basic | English-only |
| `base` | ~74 MB | Fast | Good | Multilingual |
| `small` | ~244 MB | Medium | Better | Multilingual |
| `medium` | ~769 MB | Slow | High | Multilingual |
| `large` | ~1550 MB | Very Slow | Highest | Multilingual |



```
audio-transcription-tool/
├── transcribe_gradio.py          # Main application entry point
├── requirements.txt              # Python dependencies
├── .env                         # Environment configuration
├── README.md                    # This file
├── REFACTORING_SUMMARY.md       # Detailed architecture documentation
│
├── services/                    # Business logic services
│   ├── __init__.py
│   ├── whisper_service.py       # Audio transcription service
│   ├── openai_service.py        # AI analysis service
│   └── file_service.py          # File handling service
│
├── config/                      # Configuration management
│   ├── __init__.py
│   ├── settings.py              # Environment & settings
│   └── constants.py             # Application constants
│
├── ui/                          # User interface components
│   ├── __init__.py
│   ├── components.py            # Reusable UI components
│   └── gradio_interface.py      # Interface implementations
│
├── demos/                       # Demo scripts and examples
│   ├── __init__.py             # Demo registry system
│   ├── README.md               # Demo documentation
│   ├── config_demo.py          # Configuration demonstration
│   ├── services_demo.py        # Service usage examples
│   ├── ui_demo.py              # UI components demonstration
│   └── test_runner.py          # Test runner with PRD support
│
├── docs/                        # Comprehensive documentation
│   ├── README.md               # Documentation hub
│   ├── architecture/           # Technical architecture docs
│   ├── features/               # Feature specifications
│   ├── api/                    # API reference
│   └── development/            # Development guides
│
└── tests/                       # Test suite
    ├── __init__.py
    ├── test_prd_services.py    # PRD service tests
    └── test_prd_ui.py          # PRD UI tests
```

## 🎯 Usage Examples

### Basic Usage

```python
# Simple transcription
from services.whisper_service import WhisperService

whisper = WhisperService()
transcription, temp_file = whisper.transcribe_audio("audio.mp3")
print(transcription)
```

### AI Analysis

```python
# Generate meeting key points
from services.openai_service import OpenAIService

openai_service = OpenAIService()
if openai_service.is_available():
    key_points = openai_service.generate_meeting_key_points(transcription)
    print(key_points)
```

### PRD Generation

```python
# Generate PRD from meeting key points
from services.openai_service import OpenAIService
from services.file_service import FileService

openai_service = OpenAIService()
file_service = FileService()

# Generate PRD content
if openai_service.is_available():
    prd_content = openai_service.generate_prd_from_key_points(key_points)
    
    # Create downloadable PRD file
    prd_file = file_service.create_prd_download_file(prd_content)
    print(f"PRD saved to: {prd_file}")
    
    # Validate PRD content
    is_valid, message = file_service.validate_prd_content(prd_content)
    print(f"PRD validation: {message}")
```

### Android TRD Generation

```python
# Generate Android TRD from PRD content
from services.openai_service import OpenAIService
from services.file_service import FileService

openai_service = OpenAIService()
file_service = FileService()

# Generate TRD content from PRD
if openai_service.is_available():
    trd_content = openai_service.generate_android_trd_from_prd(prd_content)
    
    # Create downloadable TRD file
    trd_file = file_service.create_trd_download_file(trd_content)
    print(f"Android TRD saved to: {trd_file}")
    
    # Validate TRD content
    is_valid, message = file_service.validate_trd_content(trd_content)
    print(f"TRD validation: {message}")
```

### Custom Interface

```python
# Create custom interface
from ui.gradio_interface import create_gradio_interface

# Simple interface
simple_interface = create_gradio_interface('simple')
simple_interface.launch()

# Custom interface with modifications
custom_interface = create_gradio_interface('custom', 
    custom_components={'audio_input': {'label': 'Upload Audio'}})
```

### Using Individual Components

```python
# Use UI components independently
from ui.components import ComponentFactory

audio_input = ComponentFactory.create_audio_input(
    label="Upload Your Audio File",
    sources=["upload", "microphone"]
)

transcription_output = ComponentFactory.create_transcription_output(
    lines=15,
    placeholder="Transcription will appear here..."
)

# Create PRD-specific components
prd_output = ComponentFactory.create_prd_output(
    label="Generated PRD",
    lines=20,
    max_lines=50
)

action_button = ComponentFactory.create_action_button(
    text="📋 Generate PRD",
    variant="primary",
    size="lg"
)
```

### Component Factory Pattern

The project uses a factory pattern for consistent UI component creation:

```python
from ui.components import ComponentFactory

# Available component types
components = {
    'audio_input': ComponentFactory.create_audio_input,
    'transcription_output': ComponentFactory.create_transcription_output,
    'key_points_output': ComponentFactory.create_key_points_output,
    'prd_output': ComponentFactory.create_prd_output,
    'action_button': ComponentFactory.create_action_button,
    'download_file': ComponentFactory.create_download_file,
    'header': ComponentFactory.create_header,
    'instructions': ComponentFactory.create_instructions,
    'status_indicator': ComponentFactory.create_status_indicator,
    'progress_bar': ComponentFactory.create_progress_bar,
    'settings_display': ComponentFactory.create_settings_display,
    'theme': ComponentFactory.create_theme
}

# Create customized components
custom_header = ComponentFactory.create_header(
    title="My Custom Transcription Tool",
    description="Powered by OpenAI Whisper and GPT"
)
```

## 🛠️ Development

### Running Demo Scripts

```bash
# Service usage examples
uv run demos/services_demo.py

# Configuration demonstration
uv run demos/config_demo.py

# UI components showcase
uv run demos/ui_demo.py

# Test runner with PRD support
uv run demos/test_runner.py
```

### Demo Registry System

The project includes a comprehensive demo registry for easy access:

```bash
# List all available demos
python -m demos list

# Run all demos sequentially
python -m demos all

# Run specific demos
python -m demos config
python -m demos services
python -m demos ui
python -m demos test
```

### Programmatic Demo Access

```python
# Import and run demos programmatically
from demos import config_demo, services_demo, ui_demo, test_runner

# Run individual demos
config_demo()       # Configuration system demonstration
services_demo()     # Service usage examples
ui_demo()          # UI components showcase
test_runner()      # Run comprehensive tests

# Or use the registry system
from demos import list_available_demos, run_all_demos

list_available_demos()  # Show all available demos
run_all_demos()         # Run all demos sequentially
```

### Adding New Services

1. Create a new service in `services/`
2. Follow the existing service patterns
3. Add configuration options in `config/`
4. Update the main interface as needed

### Creating Custom Components

```python
# Example: Custom status component
from ui.components import ComponentFactory
import gradio as gr

class CustomStatusComponent:
    def create(self):
        return gr.Textbox(
            label="Custom Status",
            interactive=False
        )
```

### Extending Configuration

Add new settings in `config/settings.py`:

```python
# In AppSettings._load_settings()
self.my_new_setting = os.getenv("MY_NEW_SETTING", "default_value")

# Add to get_app_config()
def get_app_config(self):
    return {
        # ... existing config
        "my_new_setting": self.my_new_setting
    }
```

## 🎨 Interface Types

### Standard Interface
- Full-featured interface with all capabilities
- Audio transcription and AI analysis
- File download and copy functionality
- Settings display in debug mode

### Simple Interface
- Minimal design for basic transcription
- Single input/output workflow
- Lightweight and fast loading
- Perfect for embedding in other applications

### Custom Interface
- Fully customizable components
- Custom event handlers
- Specialized workflows
- Advanced integration capabilities

## 📊 Supported Audio Formats

| Format | Extension | MIME Type |
|--------|-----------|-----------|
| MP3 | `.mp3` | `audio/mpeg` |
| WAV | `.wav` | `audio/wav` |
| M4A | `.m4a` | `audio/mp4` |
| FLAC | `.flac` | `audio/flac` |
| AAC | `.aac` | `audio/aac` |
| OGG | `.ogg` | `audio/ogg` |
| WMA | `.wma` | `audio/x-ms-wma` |

## 🔧 Advanced Configuration

### Custom Whisper Settings

```env
WHISPER_MODEL=medium
WHISPER_FP16=false
```

### OpenAI Customization

```env
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=1500
OPENAI_TEMPERATURE=0.2
```

### UI Customization

```env
GRADIO_THEME=monochrome
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SHARE=false
GRADIO_DEBUG=true
```

## 🏛️ Architecture

This project follows a clean, modular architecture that evolved through multiple refactoring phases, resulting in a robust service-oriented design with excellent separation of concerns.

### Architecture Evolution

#### Phase 1: Service Layer Extraction ✅
**Transformed from**: Monolithic `transcribe_gradio.py` (150+ lines) with mixed functionality
**Result**: Clean service-oriented architecture with dedicated responsibilities

#### Phase 2: Configuration Management ✅  
**Added**: Centralized settings management with environment variable support
**Result**: Configuration-driven behavior with comprehensive validation

#### Phase 3: UI Component Extraction ✅
**Created**: Modular, reusable UI component system with multiple interface types
**Result**: Clean separation of UI logic from business logic

### Current Architecture Layers

#### Service Layer (`services/`)
**Purpose**: Business logic and external service integration

- **WhisperService**: 
  - Audio transcription using OpenAI Whisper models
  - Model caching and memory management
  - Configurable model selection (tiny, base, small, medium, large)
  - Error handling and logging

- **OpenAIService**: 
  - AI-powered meeting analysis and key points generation
  - **PRD generation** from meeting key points
  - Custom analysis with user-defined prompts
  - Automatic API key detection and service availability checking
  - Comprehensive error handling and status reporting

- **FileService**: 
  - Audio file validation and format checking
  - Temporary file creation and cleanup
  - **PRD file operations** with automatic naming and validation
  - File information extraction and download preparation
  - Support for multiple audio formats (MP3, WAV, M4A, FLAC, AAC, OGG, WMA)

#### Configuration Layer (`config/`)
**Purpose**: Centralized settings and constants management

- **Settings (`config/settings.py`)**:
  - Environment variable loading with `.env` file support
  - Configuration validation with detailed error reporting
  - Structured configuration access via `get_*_config()` methods
  - Environment detection (development/production/testing)
  - Settings summary display with validation status

- **Constants (`config/constants.py`)**:
  - Application information and version constants
  - Supported audio formats with MIME type validation
  - Model configurations for Whisper and OpenAI
  - UI labels, error messages, and internationalization support
  - Feature flags and helper functions

#### UI Layer (`ui/`)
**Purpose**: User interface components and interaction handling

- **Components (`ui/components.py`)**:
  - **ComponentFactory**: Factory pattern for consistent component creation
  - **Reusable Components**: AudioInput, TranscriptionOutput, KeyPointsOutput, ActionButton, DownloadFile, Header, Instructions, StatusIndicator, ProgressBar, SettingsDisplay, Theme
  - **Configuration-driven**: Uses settings and constants for behavior
  - **Customizable**: Accept parameters for different use cases

- **Interfaces (`ui/gradio_interface.py`)**:
  - **GradioInterface (Standard)**: Full-featured interface with all capabilities
  - **SimpleGradioInterface**: Minimal interface for basic transcription
  - **CustomGradioInterface**: Fully customizable for specialized workflows
  - **Factory Functions**: Easy interface creation and launching

### Architecture Benefits

#### ✅ Separation of Concerns
- Each layer has well-defined responsibilities
- Business logic separated from UI logic
- Configuration isolated from implementation
- Clear boundaries between different functionalities

#### ✅ Reusability & Modularity
- Services can be used independently in other projects
- UI components are reusable across different interfaces
- Configuration system supports multiple environments
- Clean APIs for each service and component

#### ✅ Maintainability & Extensibility
- Easy to locate and modify specific functionality
- Modular structure supports future growth
- Component-based development approach
- Easy to add new features without affecting existing ones

#### ✅ Configuration-Driven Behavior
- Dynamic UI behavior based on settings
- Feature toggles control component visibility
- Environment-specific configuration loading
- Easy customization without code changes

#### ✅ Testing & Quality
- Each service can be tested in isolation
- Mock dependencies easily for unit testing
- Clear input/output contracts
- Comprehensive error handling throughout

### Interface Types

#### Standard Interface
- **Full-featured** with transcription, key points, and PRD generation
- **Configuration-driven** layout and behavior
- **Debug mode** with settings display
- **Event handling** for all interactions
- **Download functionality** for transcriptions and PRDs

#### Simple Interface  
- **Minimal design** for basic transcription only
- **Single input/output** workflow
- **Lightweight and fast** loading
- **Easy integration** into other applications

#### Custom Interface
- **Fully customizable** components and handlers
- **Advanced use cases** and specialized workflows
- **Extensible architecture** for future needs
- **Custom event handling** and business logic

## 🧪 Testing

The project includes comprehensive testing through demo scripts:

```bash
# Test all services independently
uv run demos/services_demo.py

# Test configuration system
uv run demos/config_demo.py

# Test UI components
uv run demos/ui_demo.py

# Run comprehensive test suite
uv run demos/test_runner.py

# Or use the demo registry
python -m demos all
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

### 📖 Complete Documentation Hub
For comprehensive project documentation, visit our **[Documentation Center](docs/README.md)**

### 🎯 Quick Links
- **[Architecture Evolution](docs/architecture/)** - Technical architecture history and design decisions
- **[Feature Documentation](docs/features/)** - Detailed feature specifications and status
- **[API Reference](docs/api/)** - Complete API documentation for services and components
- **[Development Guide](docs/development/)** - Setup, contribution guidelines, and testing

### 📊 Current Project Status
- **Architecture**: Phase 3 Complete (UI Components) ✅
- **Features**: PRD Generation v1.0 - FULLY COMPLETE ✅
- **Next Milestone**: Advanced Analytics Planning & Development

### 📋 Feature Status Overview
| Feature | Version | Status | Completion | Next Milestone |
|---------|---------|--------|------------|----------------|
| Audio Transcription | v3.0 | ✅ Stable | 100% | Maintenance |
| AI Meeting Analysis | v2.0 | ✅ Stable | 100% | Enhancements |
| **PRD Generation** | **v1.0** | **✅ Complete** | **100%** | **Future Enhancements** |
| **Android TRD Generation** | **v1.0** | **📋 Planning** | **0%** | **Implementation** |

For detailed feature tracking and roadmap, see [Features Overview](docs/features/features-index.md)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [OpenAI API](https://openai.com/api/) for AI-powered analysis
- [Gradio](https://gradio.app/) for the web interface framework
- The open-source community for inspiration and tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the **[Documentation Center](docs/README.md)** for comprehensive guides
2. Review **[Architecture Documentation](docs/architecture/README.md)** for technical details
3. See **[Features Status](docs/features/features-index.md)** for current development progress
4. Run the demo scripts to understand the system
5. Review the configuration options
6. Open an issue on GitHub

## 📋 PRD Generation Features - Production Ready!

### Current Implementation Status

## 🎉 PRD Generation v1.0 - PRODUCTION READY!

**Status**: ✅ **FULLY IMPLEMENTED, TESTED, AND DEPLOYED**

### Complete Feature Implementation (12/12 ✅)

#### ✅ **Phase 1**: Core PRD Generation (4/4 Complete)
- ✅ OpenAIService extended with `generate_prd_from_key_points()`
- ✅ FileService enhanced with PRD file operations and validation
- ✅ Configuration system updated with PRD-specific settings
- ✅ 8-section industry-standard PRD template implemented

#### ✅ **Phase 2**: UI Integration (4/4 Complete)  
- ✅ PRD output component with copy functionality
- ✅ Generate PRD button integrated into main workflow
- ✅ Automatic .md file download with proper naming
- ✅ Comprehensive error handling and user feedback

#### ✅ **Phase 3**: Testing & Documentation (4/4 Complete)
- ✅ Complete test suite with validation scenarios
- ✅ Comprehensive API documentation and examples
- ✅ User guides and troubleshooting documentation
- ✅ Production deployment documentation

**🚀 PRD Generation is now a core production feature of the Audio Transcription Tool!**

### Production Usage Statistics
- **Template Sections**: 8 comprehensive sections implemented
- **File Formats**: Markdown (.md) with proper structure
- **Validation**: Content validation and quality checks
- **Integration**: Seamless workflow from audio → transcription → key points → PRD

### PRD Template Structure
The generated PRDs follow a comprehensive 8-section industry-standard template:

1. **Executive Summary** - High-level overview and value propositions
2. **Problem Statement** - Clear problem definition and market opportunity
3. **Goals & Objectives** - Primary/secondary objectives and success criteria
4. **User Stories/Requirements** - Functional requirements and use cases
5. **Success Metrics** - KPIs and measurable outcomes
6. **Timeline/Milestones** - Development phases and deliverables
7. **Technical Requirements** - System requirements and constraints
8. **Risk Assessment** - Potential risks and mitigation strategies

### PRD File Management
- **Automatic Naming**: `PRD_YYYY-MM-DD_HH-MM.md` format
- **Content Validation**: Ensures all required sections are present
- **Markdown Format**: Professional formatting with proper structure
- **Download Support**: Direct download as `.md` files

## 🚀 What's Next

### PRD Feature Roadmap

## 🎉 PRD Generation v1.0 - COMPLETE!

- ✅ **Phase 1**: Core Implementation (complete)
  - [x] OpenAI service PRD generation
  - [x] File service PRD operations
  - [x] Configuration integration
  - [x] Basic UI components

- ✅ **Phase 2**: UI Integration (complete)
  - [x] Complete PRD UI components integration
  - [x] Add PRD generation workflow to main interface
  - [x] Implement download functionality
  - [x] Add comprehensive error handling

- ✅ **Phase 3**: Testing & Documentation (complete)
  - [x] Update example_usage.py with PRD examples
  - [x] Enhanced documentation and API reference
  - [x] Create comprehensive PRD tests
  - [x] Performance optimization and validation

- **Phase 4**: Future Enhancements (planned for v2.0)
  - [ ] Multiple PRD templates (Technical PRD, Feature PRD)
  - [ ] PRD template customization
  - [ ] Export to other formats (PDF, DOCX)
  - [ ] PRD version management

### General Development
- **Phase 4**: Utilities and Helpers (planned)
- **Phase 5**: Application Orchestration (planned)
- Additional AI analysis features
- More interface customization options
- Performance optimizations
- Extended audio format support

---

**Built with ❤️ using OpenAI Whisper, Gradio, and modern Python architecture patterns.**
