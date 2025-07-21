# 🎵 Audio Transcription Tool

A powerful, modular audio transcription application built with OpenAI Whisper and enhanced with AI-powered meeting analysis. This project features a clean, service-oriented architecture with configurable UI components and comprehensive customization options.

## ✨ Features

### Core Functionality
- **🎯 Audio Transcription**: High-quality transcription using OpenAI Whisper models
- **🔑 AI Meeting Analysis**: Generate key meeting points, action items, and summaries using OpenAI GPT
- **📁 Multi-Format Support**: MP3, WAV, M4A, FLAC, AAC, OGG, WMA, MP4, MOV, AVI
- **💾 Download Options**: Export transcriptions as text files
- **⚙️ Configurable Settings**: Extensive customization through environment variables

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

4. **Run the application**
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
```

### Whisper Models

| Model | Size | Speed | Accuracy | Languages |
|-------|------|-------|----------|-----------|
| `tiny` | ~39 MB | Very Fast | Basic | English-only |
| `base` | ~74 MB | Fast | Good | Multilingual |
| `small` | ~244 MB | Medium | Better | Multilingual |
| `medium` | ~769 MB | Slow | High | Multilingual |
| `large` | ~1550 MB | Very Slow | Highest | Multilingual |

## 🏗️ Project Structure

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
├── example_usage.py             # Service usage examples
├── config_demo.py               # Configuration demonstration
└── ui_demo.py                   # UI components demonstration
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
```

## 🛠️ Development

### Running Demo Scripts

```bash
# Service usage examples
uv run example_usage.py

# Configuration demonstration
uv run config_demo.py

# UI components showcase
uv run ui_demo.py
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

This project follows a clean, modular architecture with three main layers:

### Service Layer (`services/`)
- **WhisperService**: Audio transcription using OpenAI Whisper
- **OpenAIService**: AI-powered analysis and key points generation
- **FileService**: File validation, handling, and temporary file management

### Configuration Layer (`config/`)
- **Settings**: Environment variable management and validation
- **Constants**: Application constants, UI labels, and error messages

### UI Layer (`ui/`)
- **Components**: Reusable, configurable UI components
- **Interfaces**: Different interface types for various use cases

## 🧪 Testing

The project includes comprehensive testing through demo scripts:

```bash
# Test all services independently
uv run example_usage.py

# Test configuration system
uv run config_demo.py

# Test UI components
uv run ui_demo.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [OpenAI API](https://openai.com/api/) for AI-powered analysis
- [Gradio](https://gradio.app/) for the web interface framework
- The open-source community for inspiration and tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for detailed architecture documentation
2. Run the demo scripts to understand the system
3. Review the configuration options
4. Open an issue on GitHub

## 🚀 What's Next

- **Phase 4**: Utilities and Helpers (planned)
- **Phase 5**: Application Orchestration (planned)
- Additional AI analysis features
- More interface customization options
- Performance optimizations
- Extended audio format support

---

**Built with ❤️ using OpenAI Whisper, Gradio, and modern Python architecture patterns.**
