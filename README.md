# 🎵 Audio Transcription Tool

A powerful, production-ready audio transcription application built with OpenAI Whisper and enhanced with AI-powered meeting analysis and PRD generation. This project features a clean, service-oriented architecture with configurable UI components and comprehensive customization options.

**Version 1.0.0** - Production Ready ✅

## ✨ Key Features

- **🎯 High-Quality Transcription**: Audio transcription using OpenAI Whisper models
- **🔑 AI-Powered Analysis**: Generate meeting summaries, key points, and action items
- **📋 PRD Generation**: Transform meeting discussions into structured Product Requirements Documents
- **🤖 Android TRD Generation**: Convert PRDs into comprehensive Android Technical Requirements Documents, complete with architecture, UI/UX, API, database, security, performance, and testing specifications.
- **📁 Multi-Format Support**: MP3, WAV, M4A, FLAC, AAC, OGG, WMA, and more
- **💾 Download Options**: Export transcriptions, PRDs, and TRDs as markdown files
- **⚙️ Configurable Settings**: Extensive customization through environment variables
- **🎨 Modular UI**: Reusable components with multiple interface types

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone git@github.com:tomdwipo/agent.git
cd agent

# Install dependencies (uv recommended)
uv sync
```

### 2. Configuration

```bash
# Create environment file
cp .env.example .env

# Edit .env with your OpenAI API key
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. Run the Application

```bash
# Start the development server
uv run transcribe_gradio.py
```

### 4. Access the Application

Open your browser and navigate to:
- **Local**: http://localhost:7860

## 📚 Documentation

For comprehensive documentation, please visit our **[Documentation Center](docs/README.md)**.

### Quick Links

- **[🚀 Setup Guide](docs/development/setup-guide.md)**: Detailed installation and setup instructions
- **[📖 API Reference](docs/api/)**: Complete API documentation for all services and components
- **[🏗️ Architecture](docs/architecture/)**: Technical architecture and design decisions
- **[⭐ Features](docs/features/)**: Feature specifications and development status
- **[🤝 Contributing](docs/development/contributing.md)**: Guidelines for contributing to the project

## 🎯 Core Workflows

### PRD Generation Workflow
```
Audio File → Transcription → Key Points → PRD Generation → Download PRD (.md)
```

### Android TRD Generation Workflow
```
PRD Content → Android TRD Generation → Download TRD (.md)
```

## 🤝 Contributing

We welcome contributions! Please see our **[Contributing Guidelines](docs/development/contributing.md)** for more information.

### Development Process

1. **Fork & Clone**: Fork the repository and clone it locally
2. **Create Branch**: `git checkout -b feature/your-feature`
3. **Make Changes**: Implement your feature or fix
4. **Test**: Run tests and ensure they pass
5. **Submit PR**: Create a pull request for review

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [OpenAI API](https://openai.com/api/) for AI-powered analysis
- [Gradio](https://gradio.app/) for the web interface framework
- The open-source community for inspiration and tools

## 📞 Support

For issues, questions, or feature requests, please use our **[GitHub Issues](https://github.com/tomdwipo/agent/issues)**.

---

**Built with ❤️ using OpenAI Whisper, Gradio, and modern Python architecture patterns.**
