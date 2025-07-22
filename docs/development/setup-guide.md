# 🚀 Development Setup Guide

This guide will help you set up the Audio Transcription Tool for local development.

## Prerequisites

### Required Software

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **OpenAI API Key**: [Get API Key](https://platform.openai.com/api-keys)

### Recommended Tools

- **UV Package Manager**: [Install UV](https://docs.astral.sh/uv/) (recommended)
- **VS Code**: [Download VS Code](https://code.visualstudio.com/) with Python extension
- **Terminal/Command Prompt**: For running commands

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:tomdwipo/agent.git
cd agent
```

### 2. Set Up Python Environment

#### Option A: Using UV (Recommended)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

#### Option B: Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

#### Create Environment File

```bash
# Copy example environment file
cp .env.example .env

# Edit the .env file with your settings
```

#### Configure Environment Variables

Edit `.env` file with your settings:

```env
# Required for AI features
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional configurations
WHISPER_MODEL=base
OPENAI_MODEL=gpt-4
MAX_FILE_SIZE_MB=500
GRADIO_SERVER_PORT=7860
GRADIO_DEBUG=true

# Feature toggles
ENABLE_KEY_POINTS=true
ENABLE_PRD_GENERATION=true

# PRD Configuration
PRD_OPENAI_MODEL=gpt-4
PRD_MAX_TOKENS=2000
PRD_TEMPERATURE=0.3
```

### 4. Verify Installation

#### Check Python Environment

```bash
# Verify Python version
python --version

# Verify packages are installed
pip list | grep -E "(gradio|openai|whisper)"
```

#### Test Configuration

```bash
# Run configuration demo
python -m demos config

# Or run directly
python demos/config_demo.py
```

#### Test Services

```bash
# Run services demo
python -m demos services

# Test individual services
python demos/services_demo.py
```

### 5. Run the Application

#### Start Development Server

```bash
# Run the main application
python transcribe_gradio.py

# Or use UV
uv run transcribe_gradio.py
```

#### Access the Application

Open your browser and navigate to:
- **Local**: http://localhost:7860
- **Network**: http://0.0.0.0:7860 (if configured)

## Development Environment Setup

### IDE Configuration

#### VS Code Setup

1. **Install Extensions**:
   - Python
   - Python Docstring Generator
   - GitLens
   - Pylance

2. **Configure Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true
}
```

3. **Configure Launch** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Run Main App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/transcribe_gradio.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### Code Quality Tools

#### Install Development Tools

```bash
# Using UV
uv add --dev black pylint pytest pytest-cov

# Using pip
pip install black pylint pytest pytest-cov
```

#### Configure Code Formatting

```bash
# Format code with Black
black .

# Check code style
pylint services/ ui/ config/
```

## Project Structure Overview

```
audio-transcription-tool/
├── transcribe_gradio.py          # Main application entry point
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
├── .env                         # Environment variables
│
├── services/                    # Business logic services
│   ├── whisper_service.py       # Audio transcription
│   ├── openai_service.py        # AI analysis and PRD generation
│   └── file_service.py          # File operations
│
├── config/                      # Configuration management
│   ├── settings.py              # Environment settings
│   └── constants.py             # Application constants
│
├── ui/                          # User interface components
│   ├── components.py            # Reusable UI components
│   └── gradio_interface.py      # Interface implementations
│
├── demos/                       # Demo scripts and examples
├── tests/                       # Test suite
└── docs/                        # Documentation
```

## Common Development Tasks

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=services --cov=ui --cov=config

# Run specific test file
python -m pytest tests/test_prd_services.py
```

### Running Demo Scripts

```bash
# List available demos
python -m demos list

# Run all demos
python -m demos all

# Run specific demo
python -m demos services
python -m demos ui
python -m demos config
```

### Code Quality Checks

```bash
# Format code
black .

# Check linting
pylint services/ ui/ config/

# Type checking (if using mypy)
mypy services/ ui/ config/
```

### Adding New Dependencies

#### Using UV

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv sync
```

#### Using pip

```bash
# Install and add to requirements
pip install package-name
pip freeze > requirements.txt
```

## Environment-Specific Setup

### Development Environment

```env
ENVIRONMENT=development
GRADIO_DEBUG=true
LOG_LEVEL=DEBUG
ENABLE_LOGGING=true
```

### Production Environment

```env
ENVIRONMENT=production
GRADIO_DEBUG=false
GRADIO_SHARE=false
LOG_LEVEL=INFO
```

### Testing Environment

```env
ENVIRONMENT=testing
WHISPER_MODEL=tiny
MAX_FILE_SIZE_MB=10
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError` when importing services
**Solution**:
```bash
# Ensure you're in the project root
pwd

# Activate virtual environment
source .venv/bin/activate  # or venv/bin/activate

# Reinstall dependencies
uv sync  # or pip install -r requirements.txt
```

#### 2. OpenAI API Issues

**Problem**: OpenAI features not working
**Solution**:
```bash
# Check API key configuration
python -c "from config.settings import settings; print(settings.is_openai_configured())"

# Test API connection
python demos/services_demo.py
```

#### 3. Gradio Port Issues

**Problem**: Port 7860 already in use
**Solution**:
```bash
# Use different port
GRADIO_SERVER_PORT=8080 python transcribe_gradio.py

# Or kill existing process
lsof -ti:7860 | xargs kill -9
```

#### 4. Audio File Issues

**Problem**: Audio files not processing
**Solution**:
```bash
# Check supported formats
python -c "from config.constants import SUPPORTED_AUDIO_FORMATS; print(SUPPORTED_AUDIO_FORMATS)"

# Test with small file
python demos/services_demo.py
```

### Getting Help

1. **Check Configuration**:
   ```bash
   python demos/config_demo.py
   ```

2. **Run Diagnostics**:
   ```bash
   python demos/test_runner.py
   ```

3. **Check Logs**: Look for error messages in the terminal output

4. **Review Documentation**: Check the [API documentation](../api/) for detailed usage

## Development Workflow

### Daily Development

1. **Start Development Session**:
   ```bash
   cd /path/to/project
   source .venv/bin/activate
   git pull origin main
   ```

2. **Make Changes**: Edit code, add features, fix bugs

3. **Test Changes**:
   ```bash
   python -m pytest
   python demos/test_runner.py
   ```

4. **Format and Lint**:
   ```bash
   black .
   pylint services/ ui/ config/
   ```

5. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature-branch
   ```

### Feature Development

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement Feature**: Follow the architecture patterns

3. **Add Tests**: Write tests for new functionality

4. **Update Documentation**: Update relevant docs

5. **Create Pull Request**: Submit for review

## Next Steps

After completing setup:

1. **Explore the Codebase**: Review the [Architecture Documentation](../architecture/)
2. **Run Demo Scripts**: Understand how components work
3. **Read API Documentation**: Learn the [Services API](../api/services-api.md)
4. **Check Contributing Guidelines**: Review [Contributing Guide](contributing.md)
5. **Start Development**: Begin with small changes or bug fixes

## Additional Resources

- **[Architecture Documentation](../architecture/)**: Technical architecture details
- **[API Reference](../api/)**: Complete API documentation
- **[Feature Documentation](../features/)**: Feature specifications
- **[Main README](../../README.md)**: Project overview and usage

---

**Setup Guide Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
