# 🎯 SDLC Agent Workflow

**AI-Powered Software Development Life Cycle Automation Platform**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/tomdwipo/agent)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)](https://github.com/tomdwipo/agent)

Transform your software development process with AI-powered automation. From meeting transcriptions to complete technical documentation, streamline your entire SDLC workflow.

---

## 🚀 What is SDLC Agent Workflow?

The SDLC Agent Workflow is a production-ready AI platform that automates key aspects of software development, starting with audio transcription and document generation, with a comprehensive roadmap to become a complete SDLC automation solution.

### 🎯 Current Capabilities (Production Ready ✅)

- **🎤 Audio Transcription**: High-quality transcription using OpenAI Whisper models
- **🤖 AI Meeting Analysis**: Generate key meeting points and summaries with OpenAI GPT
- **📋 PRD Generation**: Transform discussions into industry-standard Product Requirements Documents
- **🔧 Android TRD Generation**: Convert PRDs into comprehensive Android Technical Requirements Documents
- **📁 Multi-Format Support**: MP3, WAV, M4A, FLAC, AAC, OGG, WMA, MP4, MOV, AVI
- **⚙️ Configurable Settings**: Extensive customization through environment variables

### 🔮 Future Vision (2025-2026 Roadmap)

Complete SDLC automation platform covering:
- **Requirements & Planning** → **Design & Architecture** → **Development Support** → **Testing & Quality** → **Deployment & Operations** → **Documentation & Knowledge**

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- `uv` package manager (recommended) or `pip`

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:tomdwipo/agent.git
   cd agent
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" >> .env
   ```

4. **Launch the application**
   ```bash
   # Using uv
   uv run python transcribe_gradio.py
   
   # Or using python directly
   python transcribe_gradio.py
   ```

5. **Access the interface**
   Open your browser to `http://localhost:7860`

---

## 🎯 Features Overview

### ✅ Production Features

| Feature | Status | Description | Documentation |
|---------|--------|-------------|---------------|
| **Audio Transcription** | ✅ Complete | OpenAI Whisper integration with multi-format support | [API Docs](docs/api/services-api.md) |
| **AI Meeting Analysis** | ✅ Complete | Key points extraction and meeting summaries | [API Docs](docs/api/services-api.md) |
| **PRD Generation v1.0** | ✅ Complete | 8-section industry-standard Product Requirements Documents | [Feature Docs](docs/features/01-prd-generation-v1.md) |
| **Android TRD Generation v1.0** | ✅ Complete | 7-section Android Technical Requirements Documents | [Feature Docs](docs/features/02-trd-generation-android.md) |

### 📋 Planned Features (2025-2026)

| Phase | Timeline | Key Components | Expected Impact |
|-------|----------|----------------|-----------------|
| **Phase 1: Requirements & Planning** | Q3 2025 | Enhanced PRD + Project Planning Agent | 50% planning time reduction |
| **Phase 2: Design & Architecture** | Q4 2025 | System Design + UI/UX Design Agents | 60% faster architecture documentation |
| **Phase 3: Development Support** | Q1 2026 | Code Generation + Development Standards | 70% boilerplate code reduction |
| **Phase 4: Testing & Quality** | Q2 2026 | Test Planning + Quality Assurance Agents | 80% test coverage automation |
| **Phase 5: Deployment & Operations** | Q3 2026 | DevOps + Infrastructure Management | 90% deployment automation |
| **Phase 6: Documentation & Knowledge** | Q4 2026 | Documentation + Knowledge Management | 75% documentation automation |

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Service Layer  │    │ Configuration   │
│                 │    │                 │    │                 │
│ • Gradio UI     │◄──►│ • OpenAI Service│◄──►│ • Settings      │
│ • Components    │    │ • Whisper Service│   │ • Constants     │
│ • Interface     │    │ • File Service  │    │ • Environment   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Backend**: Python 3.10+, OpenAI API, Whisper
- **Frontend**: Gradio (Web UI)
- **Package Management**: `uv` with `pyproject.toml`
- **Configuration**: Environment variables with `.env` support
- **Testing**: Comprehensive test suite with pytest

### Project Structure

```
agent/
├── main.py                 # Main application entry point
├── transcribe_gradio.py    # Gradio interface launcher
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
├── config/               # Configuration management
│   ├── settings.py       # Application settings
│   ├── constants.py      # System constants
│   └── __init__.py
├── services/             # Core business logic
│   ├── openai_service.py # OpenAI API integration
│   ├── whisper_service.py# Audio transcription
│   ├── file_service.py   # File operations
│   └── __init__.py
├── ui/                   # User interface components
│   ├── gradio_interface.py# Main UI interface
│   ├── components.py     # UI components
│   └── __init__.py
├── tests/                # Test suite
├── demos/                # Demo applications
└── docs/                 # Comprehensive documentation
```

---

## 📚 Documentation

### 🎯 For Users
- **[Quick Start Guide](docs/development/setup-guide.md)** - Get up and running quickly
- **[Features Overview](docs/features/features-index.md)** - Complete feature documentation
- **[User Manual](docs/README.md)** - Comprehensive user guide

### 🛠️ For Developers
- **[Architecture Overview](docs/architecture/current-architecture.md)** - Technical system design
- **[API Reference](docs/api/README.md)** - Complete API documentation
- **[Contributing Guide](docs/development/contributing.md)** - Development workflow
- **[Testing Guide](docs/development/testing.md)** - Testing procedures

### 📋 For Project Managers & Stakeholders
- **[Complete Project Proposal](docs/proposal/SDLC-Agent-Workflow-Proposal.md)** - Full business case and roadmap
- **[Architecture Evolution](docs/architecture/README.md)** - Technical progress history
- **[Feature Status Tracking](docs/features/features-index.md)** - Development progress

---

## 🚀 Usage Examples

### Basic Audio Transcription

```python
from services.whisper_service import WhisperService

# Initialize service
whisper = WhisperService()

# Transcribe audio file
result = whisper.transcribe("meeting.mp3")
print(result["text"])
```

### PRD Generation

```python
from services.openai_service import OpenAIService

# Initialize service
openai_service = OpenAIService()

# Generate PRD from meeting transcript
prd = openai_service.generate_prd(transcript_text)
print(prd)
```

### Complete Workflow

1. **Upload Audio** → Transcribe meeting recording
2. **Generate Analysis** → Extract key points and action items
3. **Create PRD** → Transform discussion into structured requirements
4. **Generate TRD** → Convert PRD into technical specifications
5. **Download Documents** → Export all generated documents

---

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000

# Whisper Configuration
WHISPER_MODEL=base
WHISPER_LANGUAGE=auto

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

### Advanced Configuration

See [Configuration API Documentation](docs/api/configuration-api.md) for complete configuration options.

---

## 🧪 Development

### Setup Development Environment

```bash
# Clone repository
git clone git@github.com:tomdwipo/agent.git
cd agent

# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run with development settings
uv run python transcribe_gradio.py
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_prd_services.py

# Run with coverage
uv run pytest --cov=services
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

See [Contributing Guidelines](docs/development/contributing.md) for detailed information.

---

## 📈 Project Status & Roadmap

### Current Status: **Production Ready v1.0** ✅

- **Core Foundation**: Fully functional audio transcription and document generation
- **Production Features**: PRD and Android TRD generation complete
- **Architecture**: Modular, scalable design ready for expansion
- **Documentation**: Comprehensive documentation and testing


#### Success Metrics by Phase
- **Phase 1**: 50% planning time reduction
- **Phase 2**: 60% faster architecture documentation
- **Phase 3**: 70% boilerplate code reduction
- **Phase 4**: 80% test coverage automation
- **Phase 5**: 90% deployment automation
- **Phase 6**: 75% documentation automation

### Complete Workflow Vision
```
Meeting/Discussion → Transcription → PRD → TRD → Architecture → Code → Tests → Deployment → Documentation
```

---

## 🤝 Community & Support

### Getting Help

- **Documentation**: Comprehensive guides in [docs/](docs/)
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/tomdwipo/agent/issues)
- **Discussions**: Join community discussions

### Contributing

We welcome contributions! See our [Contributing Guide](docs/development/contributing.md) for:
- Code contribution guidelines
- Development setup instructions
- Testing requirements
- Documentation standards

---

## 📊 Metrics & Performance

### Current Application Metrics
- **Features Implemented**: 4/4 core features (100%)
- **Architecture Phases**: 3/3 complete (Service Layer, Configuration, UI Components)
- **Test Coverage**: Comprehensive test suite
- **Production Readiness**: ✅ Ready for deployment

### Performance Benchmarks
- **Transcription Speed**: Real-time processing for most audio formats
- **PRD Generation**: ~30 seconds for typical meeting transcript
- **TRD Generation**: ~45 seconds from PRD input
- **Multi-format Support**: 9 audio/video formats supported

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎉 Acknowledgments

- **OpenAI** for Whisper and GPT API
- **Gradio** for the excellent web UI framework
- **Python Community** for the amazing ecosystem
- **Contributors** who help make this project better

---

## 📞 Contact & Links

- **Repository**: [github.com/tomdwipo/agent](https://github.com/tomdwipo/agent)
- **Documentation**: [Complete Documentation Hub](docs/README.md)
- **Project Proposal**: [SDLC Agent Workflow Proposal](docs/proposal/SDLC-Agent-Workflow-Proposal.md)
- **Issues**: [GitHub Issues](https://github.com/tomdwipo/agent/issues)

---

**🚀 Ready to transform your SDLC workflow? Get started with the Quick Start guide above!**

*Last Updated: 2025-07-23 | Version: 1.0.0 | Status: Production Ready*
