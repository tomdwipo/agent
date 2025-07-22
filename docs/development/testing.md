# 🧪 Testing Documentation

This document provides comprehensive information about testing in the Audio Transcription Tool project.

## Table of Contents

- [Testing Overview](#testing-overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Demo Scripts](#demo-scripts)
- [Test Coverage](#test-coverage)
- [Testing Best Practices](#testing-best-practices)

## Testing Overview

The project uses a multi-layered testing approach:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Demo Scripts**: Interactive testing and examples
- **Manual Testing**: UI and workflow testing

### Testing Framework

- **pytest**: Primary testing framework
- **pytest-cov**: Coverage reporting
- **Demo Scripts**: Custom testing and demonstration system

## Test Structure

### Directory Organization

```
tests/
├── __init__.py
├── test_prd_services.py         # PRD service tests
├── test_prd_ui.py              # PRD UI tests
├── fixtures/                   # Test data and fixtures
│   ├── sample_audio.wav        # Test audio files
│   ├── sample_transcription.txt # Test transcriptions
│   └── sample_prd.md           # Test PRD content
└── conftest.py                 # Pytest configuration
```

### Demo Scripts Structure

```
demos/
├── __init__.py                 # Demo registry system
├── README.md                   # Demo documentation
├── config_demo.py             # Configuration testing
├── services_demo.py           # Service testing
├── ui_demo.py                 # UI component testing
└── test_runner.py             # Comprehensive test runner
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_prd_services.py

# Run specific test method
python -m pytest tests/test_prd_services.py::test_prd_generation

# Stop on first failure
python -m pytest -x

# Run tests in parallel (if pytest-xdist installed)
python -m pytest -n auto
```

### Coverage Testing

```bash
# Run tests with coverage
python -m pytest --cov=services --cov=ui --cov=config

# Generate HTML coverage report
python -m pytest --cov=services --cov=ui --cov=config --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Demo Script Testing

```bash
# List available demos
python -m demos list

# Run all demos
python -m demos all

# Run specific demos
python -m demos config
python -m demos services
python -m demos ui
python -m demos test

# Run demos directly
python demos/config_demo.py
python demos/services_demo.py
python demos/ui_demo.py
python demos/test_runner.py
```

## Writing Tests

### Unit Test Example

```python
# tests/test_services.py
import pytest
from unittest.mock import Mock, patch
from services.openai_service import OpenAIService
from services.file_service import FileService


class TestOpenAIService:
    """Test cases for OpenAIService."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = OpenAIService()
    
    def teardown_method(self):
        """Clean up after each test method."""
        # Clean up any resources if needed
        pass
    
    def test_is_available_with_valid_client(self):
        """Test service availability with valid client."""
        # Arrange
        self.service.client = Mock()
        
        # Act
        result = self.service.is_available()
        
        # Assert
        assert result is True
    
    def test_is_available_without_client(self):
        """Test service availability without client."""
        # Arrange
        self.service.client = None
        
        # Act
        result = self.service.is_available()
        
        # Assert
        assert result is False
    
    @patch('services.openai_service.OpenAI')
    def test_generate_meeting_key_points_success(self, mock_openai):
        """Test successful key points generation."""
        # Arrange
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated key points"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        self.service.client = mock_client
        
        test_transcription = "This is a test meeting transcription."
        
        # Act
        result = self.service.generate_meeting_key_points(test_transcription)
        
        # Assert
        assert result == "Generated key points"
        mock_client.chat.completions.create.assert_called_once()
    
    def test_generate_meeting_key_points_empty_input(self):
        """Test key points generation with empty input."""
        # Act
        result = self.service.generate_meeting_key_points("")
        
        # Assert
        assert "No transcription text provided" in result
    
    @pytest.mark.parametrize("input_text,expected_valid", [
        ("", False),
        ("   ", False),
        ("Valid transcription text", True),
        ("Short", True),
    ])
    def test_input_validation(self, input_text, expected_valid):
        """Test input validation with various inputs."""
        # Act
        is_valid = len(input_text.strip()) > 0
        
        # Assert
        assert is_valid == expected_valid


class TestFileService:
    """Test cases for FileService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = FileService()
    
    def test_validate_audio_file_valid_format(self):
        """Test audio file validation with valid format."""
        # This would require a test audio file
        # For now, we'll test the format checking logic
        test_path = "test_audio.mp3"
        
        # Mock file existence and size
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):
            
            is_valid, message = self.service.validate_audio_file(test_path)
            
            # The validation should pass for MP3 format
            assert is_valid is True
    
    def test_validate_audio_file_invalid_format(self):
        """Test audio file validation with invalid format."""
        test_path = "test_file.txt"
        
        with patch('os.path.exists', return_value=True):
            is_valid, message = self.service.validate_audio_file(test_path)
            
            assert is_valid is False
            assert "Unsupported audio format" in message
    
    def test_create_prd_download_file(self):
        """Test PRD file creation."""
        test_content = "# Test PRD\n\nThis is test content."
        
        # Act
        file_path = self.service.create_prd_download_file(test_content)
        
        # Assert
        assert file_path is not None
        assert file_path.endswith('.md')
        
        # Clean up
        if file_path:
            self.service.cleanup_temp_file(file_path)
```

### Integration Test Example

```python
# tests/test_integration.py
import pytest
from services.whisper_service import WhisperService
from services.openai_service import OpenAIService
from services.file_service import FileService


class TestWorkflowIntegration:
    """Integration tests for complete workflows."""
    
    def setup_method(self):
        """Set up services for integration testing."""
        self.whisper_service = WhisperService(model_name="tiny")  # Fastest for tests
        self.openai_service = OpenAIService()
        self.file_service = FileService()
    
    @pytest.mark.integration
    def test_complete_prd_workflow(self):
        """Test complete PRD generation workflow."""
        # This test requires actual services and would be marked as integration
        # Skip if OpenAI is not configured
        if not self.openai_service.is_available():
            pytest.skip("OpenAI not configured for integration tests")
        
        # Test data
        sample_transcription = """
        This is a sample meeting transcription about developing a new mobile app.
        We discussed the user interface, backend requirements, and timeline.
        The app should have user authentication and data synchronization.
        """
        
        # Step 1: Generate key points
        key_points = self.openai_service.generate_meeting_key_points(sample_transcription)
        assert key_points is not None
        assert len(key_points) > 0
        assert not key_points.startswith("❌")
        
        # Step 2: Generate PRD from key points
        prd_content = self.openai_service.generate_prd_from_key_points(key_points)
        assert prd_content is not None
        assert len(prd_content) > 0
        assert not prd_content.startswith("❌")
        
        # Step 3: Create PRD file
        prd_file = self.file_service.create_prd_download_file(prd_content)
        assert prd_file is not None
        
        # Step 4: Validate PRD content
        is_valid, message = self.file_service.validate_prd_content(prd_content)
        assert is_valid is True
        
        # Clean up
        self.file_service.cleanup_temp_file(prd_file)
    
    @pytest.mark.slow
    def test_audio_transcription_workflow(self):
        """Test audio transcription workflow with actual audio file."""
        # This would require a test audio file
        test_audio_path = "tests/fixtures/sample_audio.wav"
        
        # Skip if test audio file doesn't exist
        import os
        if not os.path.exists(test_audio_path):
            pytest.skip("Test audio file not available")
        
        # Test transcription
        transcription, temp_file = self.whisper_service.transcribe_audio(test_audio_path)
        
        assert transcription is not None
        assert len(transcription) > 0
        assert temp_file is not None
        
        # Clean up
        self.file_service.cleanup_temp_file(temp_file)
```

### Fixture Example

```python
# tests/conftest.py
import pytest
import tempfile
import os
from services.openai_service import OpenAIService
from services.file_service import FileService


@pytest.fixture
def openai_service():
    """Provide OpenAI service instance for testing."""
    return OpenAIService()


@pytest.fixture
def file_service():
    """Provide file service instance for testing."""
    return FileService()


@pytest.fixture
def sample_transcription():
    """Provide sample transcription text for testing."""
    return """
    This is a sample meeting transcription for testing purposes.
    We discussed project requirements, timeline, and deliverables.
    The team agreed on the technical approach and next steps.
    Action items were assigned to team members.
    """


@pytest.fixture
def sample_key_points():
    """Provide sample key points for testing."""
    return """
    ## Meeting Summary
    Project planning meeting to discuss requirements and timeline.
    
    ## Key Topics Discussed
    • Technical requirements
    • Project timeline
    • Team responsibilities
    
    ## Action Items
    • Complete technical specification - John
    • Set up development environment - Sarah
    
    ## Next Steps
    • Begin development phase
    • Schedule weekly check-ins
    """


@pytest.fixture
def temp_audio_file():
    """Create a temporary audio file for testing."""
    # Create a minimal WAV file for testing
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        # Write minimal WAV header (44 bytes)
        wav_header = b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        f.write(wav_header)
        temp_path = f.name
    
    yield temp_path
    
    # Clean up
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return {
        "whisper_model": "tiny",
        "max_file_size": 10,  # MB
        "test_timeout": 30,   # seconds
    }
```

## Demo Scripts

### Demo Script Structure

Demo scripts serve as both testing tools and usage examples:

```python
# demos/services_demo.py
"""
Services Demo Script

Demonstrates and tests all service functionality.
"""

def demo_whisper_service():
    """Demonstrate WhisperService functionality."""
    print("🎯 Testing WhisperService...")
    
    from services.whisper_service import WhisperService
    
    # Test service initialization
    whisper = WhisperService()
    print(f"✅ WhisperService initialized with model: {whisper.model_name}")
    
    # Test model loading
    try:
        model = whisper.load_model()
        print("✅ Whisper model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    return True


def demo_openai_service():
    """Demonstrate OpenAIService functionality."""
    print("\n🤖 Testing OpenAIService...")
    
    from services.openai_service import OpenAIService
    
    service = OpenAIService()
    
    # Test availability
    if service.is_available():
        print("✅ OpenAI service is available")
        
        # Test key points generation
        sample_text = "This is a test meeting about project planning."
        try:
            key_points = service.generate_meeting_key_points(sample_text)
            if not key_points.startswith("❌"):
                print("✅ Key points generation successful")
                return True
            else:
                print(f"❌ Key points generation failed: {key_points}")
        except Exception as e:
            print(f"❌ Error generating key points: {e}")
    else:
        print("❌ OpenAI service not available")
        print(f"Status: {service.get_availability_status()}")
    
    return False


def main():
    """Run all service demos."""
    print("🚀 Running Services Demo")
    print("=" * 50)
    
    results = []
    
    # Test each service
    results.append(demo_whisper_service())
    results.append(demo_openai_service())
    
    # Summary
    print("\n📊 Demo Results:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    
    return all(results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

### Running Demo Scripts

```bash
# Individual demos
python demos/config_demo.py
python demos/services_demo.py
python demos/ui_demo.py

# Using demo registry
python -m demos config
python -m demos services
python -m demos ui
python -m demos all

# Comprehensive test runner
python demos/test_runner.py
```

## Test Coverage

### Coverage Configuration

Create `.coveragerc` file:

```ini
[run]
source = services, ui, config
omit = 
    */tests/*
    */demos/*
    */__init__.py
    */conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

### Coverage Targets

- **Overall Coverage**: 80% minimum
- **Services**: 90% minimum (critical business logic)
- **UI Components**: 70% minimum
- **Configuration**: 85% minimum

### Checking Coverage

```bash
# Generate coverage report
python -m pytest --cov=services --cov=ui --cov=config --cov-report=term-missing

# Generate HTML report
python -m pytest --cov=services --cov=ui --cov=config --cov-report=html

# Coverage with specific threshold
python -m pytest --cov=services --cov-fail-under=80
```

## Testing Best Practices

### Test Organization

1. **Group Related Tests**: Use test classes to group related functionality
2. **Descriptive Names**: Use clear, descriptive test method names
3. **Arrange-Act-Assert**: Follow the AAA pattern
4. **One Assertion Per Test**: Focus each test on a single behavior

### Test Data Management

```python
# Good: Use fixtures for test data
@pytest.fixture
def sample_data():
    return {"key": "value", "number": 42}

def test_function_with_data(sample_data):
    result = process_data(sample_data)
    assert result is not None

# Good: Use parametrize for multiple test cases
@pytest.mark.parametrize("input_val,expected", [
    ("valid", True),
    ("", False),
    (None, False),
])
def test_validation(input_val, expected):
    assert validate_input(input_val) == expected
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

# Mock external API calls
@patch('services.openai_service.OpenAI')
def test_openai_integration(mock_openai):
    mock_client = Mock()
    mock_openai.return_value = mock_client
    
    # Test your code without making actual API calls
    service = OpenAIService()
    # ... test logic

# Mock file system operations
@patch('os.path.exists')
@patch('os.path.getsize')
def test_file_validation(mock_getsize, mock_exists):
    mock_exists.return_value = True
    mock_getsize.return_value = 1024
    
    # Test file validation logic
    result = validate_file("test.mp3")
    assert result is True
```

### Performance Testing

```python
import time
import pytest

@pytest.mark.performance
def test_transcription_performance():
    """Test that transcription completes within reasonable time."""
    start_time = time.time()
    
    # Run transcription
    result = transcribe_audio("small_test_file.wav")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Should complete within 30 seconds for small file
    assert duration < 30
    assert result is not None
```

### Error Testing

```python
def test_error_handling():
    """Test proper error handling."""
    service = OpenAIService()
    
    # Test with invalid input
    with pytest.raises(ValueError):
        service.process_invalid_input(None)
    
    # Test error message content
    try:
        service.process_invalid_input("")
    except ValueError as e:
        assert "cannot be empty" in str(e)
```

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m pytest --cov=services --cov=ui --cov=config
    
    - name: Run demo scripts
      run: |
        python demos/config_demo.py
        python demos/services_demo.py
```

## Troubleshooting Tests

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH includes project root
2. **Missing Dependencies**: Install test dependencies with `pip install pytest pytest-cov`
3. **API Key Issues**: Set test environment variables or skip API-dependent tests
4. **File Path Issues**: Use absolute paths or proper fixtures for test files

### Debug Test Failures

```bash
# Run with verbose output
python -m pytest -v -s

# Run specific failing test
python -m pytest tests/test_services.py::TestOpenAIService::test_specific_method -v

# Drop into debugger on failure
python -m pytest --pdb

# Show local variables on failure
python -m pytest --tb=long
```

---

**Testing Documentation Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
