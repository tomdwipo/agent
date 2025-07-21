# Demo Scripts

This directory contains demonstration scripts for the Audio Transcription Tool with PRD Generation functionality.

## Available Demos

### 1. Configuration Demo (`config_demo.py`)
Demonstrates the configuration management system introduced in Phase 2.

**Features:**
- Application information display
- Settings overview and validation
- Available models listing
- Supported audio formats
- Environment detection
- Configuration usage examples

**Usage:**
```bash
uv run demos/config_demo.py
```

### 2. Services Demo (`services_demo.py`)
Shows how to use the refactored services independently without the Gradio interface.

**Features:**
- Service availability checking
- File validation examples
- Audio transcription workflow
- Key points generation
- PRD generation from key points
- Custom analysis examples

**Usage:**
```bash
uv run demos/services_demo.py
```

### 3. UI Components Demo (`ui_demo.py`)
Demonstrates the modular UI component system introduced in Phase 3.

**Features:**
- Individual component showcase
- Interface types demonstration
- Component customization examples
- Configuration integration
- Interactive demo interface (optional)

**Usage:**
```bash
uv run demos/ui_demo.py
```

### 4. Test Runner (`test_runner.py`)
Comprehensive test runner for the application including PRD-related functionality.

**Features:**
- Automatic test discovery
- PRD-specific test execution
- Detailed test results and coverage
- Multiple execution modes

**Usage:**
```bash
# Run all tests
uv run demos/test_runner.py

# Run with verbose output
uv run demos/test_runner.py --verbose

# Run only PRD tests
uv run demos/test_runner.py --prd-only

# Show help
uv run demos/test_runner.py --help
```

## Programmatic Usage

You can also import and run demos programmatically:

```python
from demos import config_demo, services_demo, ui_demo, test_runner

# Run individual demos
config_demo()
services_demo()
ui_demo()
test_runner()

# Or use the registry
from demos import list_available_demos, run_all_demos

list_available_demos()  # Show all available demos
run_all_demos()         # Run all demos sequentially
```

## Demo Registry Usage

The `demos` module provides a registry system for easy access:

```bash
# List all available demos
python -m demos list

# Run all demos
python -m demos all

# Run specific demo
python -m demos config
python -m demos services
python -m demos ui
python -m demos test
```

## Requirements

All demos require the same dependencies as the main application:
- Python 3.8+
- Dependencies listed in `requirements.txt` or `pyproject.toml`
- OpenAI API key (for AI-powered features)
- Audio files for transcription demos

## Notes

- **Configuration Demo**: Shows current settings and validates configuration
- **Services Demo**: Requires audio files (like `denver_extract.mp3`) for full demonstration
- **UI Demo**: Can launch interactive Gradio interface if uncommented
- **Test Runner**: Discovers and runs all tests in the `tests/` directory

## Troubleshooting

If you encounter import errors:
1. Ensure you're running from the project root directory
2. Check that all dependencies are installed: `uv sync`
3. Verify your Python environment is activated

For OpenAI-related demos:
1. Set your `OPENAI_API_KEY` environment variable
2. Check your API key has sufficient credits
3. Ensure network connectivity for API calls
