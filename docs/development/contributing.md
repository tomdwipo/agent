# 🤝 Contributing Guidelines

Thank you for your interest in contributing to the Audio Transcription Tool! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Architecture Guidelines](#architecture-guidelines)

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Development Environment**: Follow the [Setup Guide](setup-guide.md)
2. **Understanding of the Project**: Review the [Architecture Documentation](../architecture/)
3. **Familiarity with APIs**: Check the [API Reference](../api/)

### First-Time Contributors

1. **Fork the Repository**: Create your own fork on GitHub
2. **Clone Your Fork**:
   ```bash
   git clone git@github.com:YOUR_USERNAME/agent.git
   cd agent
   ```
3. **Set Up Development Environment**: Follow the [Setup Guide](setup-guide.md)
4. **Explore the Codebase**: Run demo scripts to understand functionality

## Development Workflow

### Branch Strategy

We use a feature branch workflow:

```
main (production-ready)
├── feature/new-feature-name
├── bugfix/issue-description
├── docs/documentation-update
└── refactor/component-name
```

### Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/descriptive-name

# Example branch names
git checkout -b feature/android-trd-generation
git checkout -b bugfix/audio-upload-validation
git checkout -b docs/api-documentation-update
```

### Development Process

1. **Make Changes**: Implement your feature or fix
2. **Test Locally**: Run tests and demo scripts
3. **Format Code**: Use Black and check with Pylint
4. **Commit Changes**: Use descriptive commit messages
5. **Push Branch**: Push to your fork
6. **Create Pull Request**: Submit for review

### Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add Android TRD generation service"
git commit -m "Fix audio file validation for large files"
git commit -m "Update API documentation for new endpoints"
git commit -m "Refactor UI components for better reusability"

# Avoid vague messages
git commit -m "Fix bug"
git commit -m "Update code"
git commit -m "Changes"
```

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(services): add Android TRD generation service
fix(ui): resolve audio upload validation issue
docs(api): update services API documentation
refactor(components): improve ComponentFactory pattern
```

## Code Standards

### Python Code Style

We follow PEP 8 with some modifications:

#### Formatting with Black

```bash
# Format all code
black .

# Check specific files
black services/ ui/ config/
```

#### Linting with Pylint

```bash
# Check all code
pylint services/ ui/ config/

# Check specific file
pylint services/openai_service.py
```

#### Code Style Guidelines

1. **Line Length**: Maximum 88 characters (Black default)
2. **Imports**: Group imports (standard library, third-party, local)
3. **Docstrings**: Use Google-style docstrings
4. **Type Hints**: Use type hints for function parameters and returns
5. **Variable Names**: Use descriptive names (snake_case)
6. **Constants**: Use UPPER_CASE for constants

#### Example Code Style

```python
"""
Module docstring describing the purpose.
"""

import os
from typing import Optional, Dict, Any

from openai import OpenAI
from config.settings import settings


class ExampleService:
    """
    Example service class demonstrating code style.
    
    This class shows proper formatting, documentation,
    and type hints according to project standards.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the service.
        
        Args:
            api_key: Optional API key override
        """
        self.api_key = api_key or settings.openai_api_key
        self.client = None
    
    def process_data(self, input_data: str, options: Dict[str, Any]) -> str:
        """
        Process input data with given options.
        
        Args:
            input_data: The data to process
            options: Processing options
            
        Returns:
            Processed data as string
            
        Raises:
            ValueError: If input_data is empty
        """
        if not input_data.strip():
            raise ValueError("Input data cannot be empty")
        
        # Processing logic here
        result = self._internal_process(input_data, options)
        return result
    
    def _internal_process(self, data: str, options: Dict[str, Any]) -> str:
        """Internal processing method."""
        # Implementation details
        return f"Processed: {data}"
```

### Documentation Standards

#### Docstring Format

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of the first parameter
        param2: Description of the second parameter with default value
        
    Returns:
        Description of the return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Example:
        >>> result = example_function("test", 20)
        >>> print(result)
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    return len(param1) > param2
```

#### Code Comments

```python
# Good comments explain WHY, not WHAT
def calculate_tokens(text: str) -> int:
    # OpenAI uses approximately 4 characters per token for English text
    # This is a rough estimation for token counting
    return len(text) // 4

# Avoid obvious comments
def get_file_size(file_path: str) -> int:
    # Don't do this: "Get the size of the file"
    return os.path.getsize(file_path)
```

## Testing Requirements

### Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── __init__.py
├── test_services.py          # Service layer tests
├── test_ui_components.py     # UI component tests
├── test_configuration.py     # Configuration tests
└── test_integration.py       # Integration tests
```

### Writing Tests

#### Unit Tests

```python
import pytest
from services.openai_service import OpenAIService


class TestOpenAIService:
    """Test cases for OpenAIService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = OpenAIService()
    
    def test_is_available_with_valid_key(self):
        """Test service availability with valid API key."""
        # Arrange
        self.service.client = "mock_client"
        
        # Act
        result = self.service.is_available()
        
        # Assert
        assert result is True
    
    def test_is_available_without_key(self):
        """Test service availability without API key."""
        # Arrange
        self.service.client = None
        
        # Act
        result = self.service.is_available()
        
        # Assert
        assert result is False
    
    @pytest.mark.parametrize("input_text,expected", [
        ("", False),
        ("   ", False),
        ("valid text", True),
    ])
    def test_input_validation(self, input_text, expected):
        """Test input validation with various inputs."""
        result = self.service._validate_input(input_text)
        assert result == expected
```

#### Integration Tests

```python
def test_complete_transcription_workflow():
    """Test the complete transcription workflow."""
    # This test would use actual services but with test data
    from services.whisper_service import WhisperService
    from services.file_service import FileService
    
    whisper = WhisperService(model_name="tiny")  # Use fastest model for tests
    file_service = FileService()
    
    # Test with a small audio file
    test_audio_path = "tests/fixtures/test_audio.wav"
    
    # Test transcription
    transcription, temp_file = whisper.transcribe_audio(test_audio_path)
    
    assert transcription is not None
    assert len(transcription) > 0
    assert temp_file is not None
    
    # Clean up
    file_service.cleanup_temp_file(temp_file)
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=services --cov=ui --cov=config --cov-report=html

# Run specific test file
python -m pytest tests/test_services.py

# Run specific test method
python -m pytest tests/test_services.py::TestOpenAIService::test_is_available

# Run tests with verbose output
python -m pytest -v

# Run tests and stop on first failure
python -m pytest -x
```

### Test Coverage Requirements

- **Minimum Coverage**: 80% for new code
- **Critical Components**: 90%+ coverage for services
- **Test Types**: Unit tests, integration tests, and demo script tests

## Pull Request Process

### Before Creating a Pull Request

1. **Update Your Branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run All Tests**:
   ```bash
   python -m pytest
   python -m demos all
   ```

3. **Format and Lint Code**:
   ```bash
   black .
   pylint services/ ui/ config/
   ```

4. **Update Documentation**: If you've added features or changed APIs

### Pull Request Template

When creating a pull request, include:

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Changes Made
- List specific changes
- Include any new files or modified files
- Mention any configuration changes

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed
- [ ] Demo scripts run successfully

## Documentation
- [ ] Code is properly documented
- [ ] API documentation updated (if applicable)
- [ ] README updated (if applicable)

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Code is properly commented
- [ ] No unnecessary console.log or debug statements
- [ ] Changes generate no new warnings
```

### Review Process

1. **Automated Checks**: GitHub Actions will run tests and linting
2. **Code Review**: At least one maintainer will review your code
3. **Feedback**: Address any feedback or requested changes
4. **Approval**: Once approved, your PR will be merged

### Review Criteria

Reviewers will check for:

- **Code Quality**: Follows style guidelines and best practices
- **Functionality**: Changes work as intended
- **Tests**: Adequate test coverage for new code
- **Documentation**: Proper documentation for new features
- **Architecture**: Follows project architecture patterns
- **Performance**: No significant performance regressions

## Issue Guidelines

### Reporting Bugs

Use the bug report template:

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. macOS, Windows, Linux]
- Python Version: [e.g. 3.9.0]
- Browser: [e.g. chrome, safari]
- Version: [e.g. 1.0.0]

**Additional Context**
Add any other context about the problem here.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## Architecture Guidelines

### Adding New Services

When adding new services:

1. **Follow the Service Pattern**:
   ```python
   class NewService:
       def __init__(self):
           # Initialize service
           pass
       
       def main_method(self, input_data):
           # Main functionality
           pass
       
       def _private_method(self):
           # Internal helper methods
           pass
   ```

2. **Add Configuration**: Update `config/settings.py` and `config/constants.py`
3. **Create Tests**: Add comprehensive tests
4. **Update Documentation**: Add to API documentation

### Adding New UI Components

When adding UI components:

1. **Follow the Component Pattern**: Use the existing component structure
2. **Add to ComponentFactory**: Include factory method
3. **Update Interfaces**: Integrate with existing interfaces
4. **Test Components**: Add UI component tests

### Configuration Changes

When modifying configuration:

1. **Update Settings**: Modify `config/settings.py`
2. **Add Constants**: Update `config/constants.py`
3. **Environment Variables**: Document new variables
4. **Validation**: Add validation for new settings

## Code Review Guidelines

### For Contributors

- **Self-Review**: Review your own code before submitting
- **Small PRs**: Keep pull requests focused and reasonably sized
- **Clear Description**: Explain what and why, not just what
- **Test Coverage**: Include tests for new functionality

### For Reviewers

- **Be Constructive**: Provide helpful feedback
- **Focus on Important Issues**: Don't nitpick minor style issues
- **Ask Questions**: If something is unclear, ask for clarification
- **Approve When Ready**: Don't delay approval for minor issues

## Getting Help

### Resources

- **[Setup Guide](setup-guide.md)**: Development environment setup
- **[Architecture Documentation](../architecture/)**: Technical architecture
- **[API Reference](../api/)**: Complete API documentation
- **[Demo Scripts](../../demos/)**: Working examples

### Communication

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Request Comments**: For code-specific discussions

### Mentorship

New contributors are welcome! If you're new to the project:

1. **Start Small**: Begin with documentation or small bug fixes
2. **Ask Questions**: Don't hesitate to ask for help
3. **Learn the Codebase**: Explore existing code and patterns
4. **Follow Guidelines**: Adhere to the established patterns

## Recognition

Contributors are recognized in:

- **README.md**: Contributors section
- **Release Notes**: Major contributions mentioned
- **GitHub**: Contributor statistics and graphs

Thank you for contributing to the Audio Transcription Tool! 🎉

---

**Contributing Guidelines Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
