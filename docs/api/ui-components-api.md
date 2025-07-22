# 🎨 UI Components API Reference

This document provides comprehensive API documentation for the UI components system in the Audio Transcription Tool.

## Overview

The UI components system provides reusable Gradio components and interfaces using a factory pattern. It consists of:

- **Component Classes**: Individual UI component implementations
- **ComponentFactory**: Factory for creating components consistently
- **Interface Classes**: Complete interface implementations (Standard, Simple, Custom)

---

## Component Classes

Individual component classes that encapsulate specific UI functionality.

### AudioInputComponent

Audio file upload component with customizable sources.

**Location**: `ui/components.py`

#### Constructor

```python
AudioInputComponent(label=None, sources=None)
```

**Parameters:**
- `label` (str, optional): Custom label for the audio input. Default: "Upload Audio File"
- `sources` (List[str], optional): Input sources. Default: ["upload"]

**Available Sources:**
- `"upload"`: File upload
- `"microphone"`: Microphone recording

**Example:**
```python
from ui.components import AudioInputComponent

# Basic audio input
audio_input = AudioInputComponent()

# Custom audio input with microphone
audio_input = AudioInputComponent(
    label="Record or Upload Audio",
    sources=["upload", "microphone"]
)
```

#### Methods

##### `create()`

Create and return the Gradio Audio component.

**Returns:**
- `gr.Audio`: Configured Gradio Audio component

**Example:**
```python
audio_component = audio_input.create()
```

---

### TranscriptionOutputComponent

Text output component for displaying transcription results.

#### Constructor

```python
TranscriptionOutputComponent(label=None, placeholder=None, lines=10, max_lines=20)
```

**Parameters:**
- `label` (str, optional): Custom label. Default: "Transcription Result"
- `placeholder` (str, optional): Placeholder text. Default: "Transcription will appear here..."
- `lines` (int): Number of visible lines. Default: 10
- `max_lines` (int): Maximum number of lines. Default: 20

**Example:**
```python
transcription_output = TranscriptionOutputComponent(
    label="Audio Transcription",
    lines=15,
    max_lines=30
)
```

#### Methods

##### `create()`

Create and return the Gradio Textbox component.

**Returns:**
- `gr.Textbox`: Configured Gradio Textbox with copy functionality

---

### KeyPointsOutputComponent

Text output component for displaying meeting key points.

#### Constructor

```python
KeyPointsOutputComponent(label=None, placeholder=None, lines=15, max_lines=25)
```

**Parameters:**
- `label` (str, optional): Custom label. Default: "Key Meeting Points"
- `placeholder` (str, optional): Placeholder text. Default: "Key meeting points will appear here..."
- `lines` (int): Number of visible lines. Default: 15
- `max_lines` (int): Maximum number of lines. Default: 25

**Example:**
```python
key_points_output = KeyPointsOutputComponent(
    label="Meeting Summary",
    lines=20
)
```

---

### PRDOutputComponent

Text output component for displaying Product Requirements Documents.

#### Constructor

```python
PRDOutputComponent(label=None, placeholder=None, lines=20, max_lines=50)
```

**Parameters:**
- `label` (str, optional): Custom label. Default: "Product Requirements Document"
- `placeholder` (str, optional): Placeholder text. Default: "Generated PRD will appear here..."
- `lines` (int): Number of visible lines. Default: 20
- `max_lines` (int): Maximum number of lines. Default: 50

**Example:**
```python
prd_output = PRDOutputComponent(
    label="Generated PRD",
    lines=25,
    max_lines=60
)
```

---

### ActionButtonComponent

Customizable action button component.

#### Constructor

```python
ActionButtonComponent(text, variant="primary", size="lg", icon=None)
```

**Parameters:**
- `text` (str): Button text
- `variant` (str): Button variant. Options: "primary", "secondary", "stop"
- `size` (str): Button size. Options: "sm", "md", "lg"
- `icon` (str, optional): Icon for the button (currently not implemented)

**Example:**
```python
transcribe_btn = ActionButtonComponent(
    text="🎯 Transcribe Audio",
    variant="primary",
    size="lg"
)

generate_btn = ActionButtonComponent(
    text="Generate Key Points",
    variant="secondary"
)
```

---

### DownloadFileComponent

File download component for providing downloadable files.

#### Constructor

```python
DownloadFileComponent(label=None, visible=False)
```

**Parameters:**
- `label` (str, optional): Custom label. Default: "Download Transcription"
- `visible` (bool): Initial visibility state. Default: False

**Example:**
```python
download_file = DownloadFileComponent(
    label="Download PRD (.md)",
    visible=True
)
```

---

### HeaderComponent

Application header with title and description.

#### Constructor

```python
HeaderComponent(title=None, description=None)
```

**Parameters:**
- `title` (str, optional): Custom title. Default: From UI_LABELS["app_title"]
- `description` (str, optional): Custom description. Default: From settings

**Example:**
```python
header = HeaderComponent(
    title="# 🎵 My Custom Transcription Tool",
    description="Powered by OpenAI Whisper and GPT"
)
```

#### Methods

##### `create()`

Create and return header components.

**Returns:**
- `List[gr.Markdown]`: List of Markdown components for title and description

---

### InstructionsComponent

Dynamic user instructions component.

#### Constructor

```python
InstructionsComponent(title=None, instructions=None)
```

**Parameters:**
- `title` (str, optional): Instructions title. Default: "📝 Instructions:"
- `instructions` (str, optional): Custom instructions. Default: Auto-generated based on configuration

**Example:**
```python
instructions = InstructionsComponent(
    title="## How to Use",
    instructions="1. Upload audio\n2. Click transcribe\n3. Download results"
)
```

#### Methods

##### `create()`

Create and return instruction components.

**Returns:**
- `List[gr.Markdown]`: List of Markdown components for title and instructions

---

### StatusIndicatorComponent

Status display component for showing current operation status.

#### Constructor

```python
StatusIndicatorComponent(initial_status="Ready")
```

**Parameters:**
- `initial_status` (str): Initial status text. Default: "Ready"

**Example:**
```python
status = StatusIndicatorComponent(initial_status="Waiting for audio...")
```

---

### ProgressBarComponent

Progress indication component.

#### Constructor

```python
ProgressBarComponent(visible=False)
```

**Parameters:**
- `visible` (bool): Initial visibility state. Default: False

**Example:**
```python
progress = ProgressBarComponent(visible=True)
```

---

### SettingsDisplayComponent

Component for displaying current application settings.

#### Constructor

```python
SettingsDisplayComponent()
```

**Example:**
```python
settings_display = SettingsDisplayComponent()
```

#### Methods

##### `create()`

Create and return settings display component.

**Returns:**
- `gr.Markdown`: Markdown component with formatted settings information

**Settings Displayed:**
- Whisper model
- Max file size
- OpenAI configuration status
- Feature enablement status

---

### ThemeComponent

Theme management component.

#### Constructor

```python
ThemeComponent()
```

#### Methods

##### `get_theme()`

Get the configured Gradio theme.

**Returns:**
- `gr.Theme`: Configured Gradio theme object

**Available Themes:**
- `soft` (default)
- `default`
- `monochrome`
- `glass`
- `base`

**Example:**
```python
theme_component = ThemeComponent()
theme = theme_component.get_theme()
```

---

## ComponentFactory

Factory class for creating UI components with consistent configuration.

### Class: `ComponentFactory`

**Location**: `ui/components.py`

Static factory methods for creating all UI components.

#### Methods

##### `create_audio_input(**kwargs)`

Create audio input component.

**Parameters:**
- `**kwargs`: Parameters passed to AudioInputComponent constructor

**Returns:**
- `gr.Audio`: Configured audio input component

**Example:**
```python
from ui.components import ComponentFactory

audio_input = ComponentFactory.create_audio_input(
    label="Upload Meeting Recording",
    sources=["upload", "microphone"]
)
```

##### `create_transcription_output(**kwargs)`

Create transcription output component.

**Parameters:**
- `**kwargs`: Parameters passed to TranscriptionOutputComponent constructor

**Returns:**
- `gr.Textbox`: Configured transcription output component

**Example:**
```python
transcription_output = ComponentFactory.create_transcription_output(
    lines=20,
    max_lines=40
)
```

##### `create_key_points_output(**kwargs)`

Create key points output component.

**Parameters:**
- `**kwargs`: Parameters passed to KeyPointsOutputComponent constructor

**Returns:**
- `gr.Textbox`: Configured key points output component

##### `create_prd_output(**kwargs)`

Create PRD output component.

**Parameters:**
- `**kwargs`: Parameters passed to PRDOutputComponent constructor

**Returns:**
- `gr.Textbox`: Configured PRD output component

##### `create_action_button(text, **kwargs)`

Create action button component.

**Parameters:**
- `text` (str): Button text
- `**kwargs`: Additional parameters passed to ActionButtonComponent constructor

**Returns:**
- `gr.Button`: Configured action button component

**Example:**
```python
button = ComponentFactory.create_action_button(
    text="🎯 Start Processing",
    variant="primary",
    size="lg"
)
```

##### `create_download_file(**kwargs)`

Create download file component.

**Parameters:**
- `**kwargs`: Parameters passed to DownloadFileComponent constructor

**Returns:**
- `gr.File`: Configured download file component

##### `create_header(**kwargs)`

Create header components.

**Parameters:**
- `**kwargs`: Parameters passed to HeaderComponent constructor

**Returns:**
- `List[gr.Markdown]`: List of header components

##### `create_instructions(**kwargs)`

Create instruction components.

**Parameters:**
- `**kwargs`: Parameters passed to InstructionsComponent constructor

**Returns:**
- `List[gr.Markdown]`: List of instruction components

##### `create_status_indicator(**kwargs)`

Create status indicator component.

**Parameters:**
- `**kwargs`: Parameters passed to StatusIndicatorComponent constructor

**Returns:**
- `gr.Textbox`: Configured status indicator component

##### `create_progress_bar(**kwargs)`

Create progress bar component.

**Parameters:**
- `**kwargs`: Parameters passed to ProgressBarComponent constructor

**Returns:**
- `gr.Progress`: Configured progress bar component

##### `create_settings_display()`

Create settings display component.

**Returns:**
- `gr.Markdown`: Configured settings display component

##### `get_theme()`

Get configured theme.

**Returns:**
- `gr.Theme`: Configured Gradio theme

---

## Interface Classes

Complete interface implementations for different use cases.

### GradioInterface

Full-featured standard interface with all capabilities.

**Location**: `ui/gradio_interface.py`

#### Constructor

```python
GradioInterface()
```

Automatically loads configuration from settings.

**Example:**
```python
from ui.gradio_interface import GradioInterface

interface = GradioInterface()
```

#### Methods

##### `create_interface()`

Create and configure the complete Gradio interface.

**Returns:**
- `gr.Blocks`: Configured Gradio Blocks interface

**Features:**
- Audio transcription
- Key points generation (if enabled)
- PRD generation (if enabled)
- File downloads
- Settings display (debug mode)
- Dynamic instructions

**Example:**
```python
blocks = interface.create_interface()
```

##### `launch(**kwargs)`

Launch the Gradio interface.

**Parameters:**
- `**kwargs`: Additional launch parameters (override configuration)

**Returns:**
- Gradio app instance

**Example:**
```python
interface.launch(
    server_port=8080,
    share=True
)
```

---

### SimpleGradioInterface

Simplified interface for basic transcription use cases.

#### Constructor

```python
SimpleGradioInterface(enable_key_points=None)
```

**Parameters:**
- `enable_key_points` (bool, optional): Override key points setting

**Example:**
```python
simple_interface = SimpleGradioInterface(enable_key_points=False)
```

#### Methods

##### `create_interface()`

Create a simple Gradio interface.

**Returns:**
- `gr.Interface`: Simple Gradio Interface (not Blocks)

**Features:**
- Basic audio input
- Transcription output only
- Minimal UI

---

### CustomGradioInterface

Fully customizable interface for advanced use cases.

#### Constructor

```python
CustomGradioInterface(custom_components=None, custom_handlers=None)
```

**Parameters:**
- `custom_components` (dict, optional): Custom component configurations
- `custom_handlers` (dict, optional): Custom event handlers

**Example:**
```python
custom_interface = CustomGradioInterface(
    custom_components={
        "audio_input": {"label": "Upload Recording", "sources": ["upload"]},
        "transcription_output": {"lines": 25}
    },
    custom_handlers={
        "transcription_handler": my_custom_handler
    }
)
```

#### Methods

##### `create_interface()`

Create a customizable Gradio interface.

**Returns:**
- `gr.Blocks`: Customized Gradio Blocks interface

---

## Factory Functions

Convenience functions for creating interfaces.

### `create_gradio_interface(interface_type="standard", **kwargs)`

Factory function to create different types of interfaces.

**Parameters:**
- `interface_type` (str): Interface type ("standard", "simple", "custom")
- `**kwargs`: Additional configuration parameters

**Returns:**
- `gr.Blocks` or `gr.Interface`: Configured interface

**Example:**
```python
from ui.gradio_interface import create_gradio_interface

# Standard interface
standard = create_gradio_interface("standard")

# Simple interface
simple = create_gradio_interface("simple", enable_key_points=False)

# Custom interface
custom = create_gradio_interface("custom", 
    custom_components={"audio_input": {"label": "Custom Label"}}
)
```

---

## Usage Examples

### Basic Component Creation

```python
from ui.components import ComponentFactory

# Create individual components
audio_input = ComponentFactory.create_audio_input()
transcription_output = ComponentFactory.create_transcription_output()
transcribe_button = ComponentFactory.create_action_button("Transcribe")

# Use in Gradio interface
import gradio as gr

with gr.Blocks() as demo:
    audio_input
    transcribe_button
    transcription_output
```

### Custom Component Configuration

```python
# Customized components
audio_input = ComponentFactory.create_audio_input(
    label="📁 Upload Your Meeting Recording",
    sources=["upload", "microphone"]
)

transcription_output = ComponentFactory.create_transcription_output(
    label="📝 Transcription Results",
    lines=20,
    max_lines=50
)

prd_output = ComponentFactory.create_prd_output(
    label="📋 Generated PRD",
    lines=30
)
```

### Complete Interface Creation

```python
from ui.gradio_interface import GradioInterface

# Create and launch standard interface
interface = GradioInterface()
blocks = interface.create_interface()
interface.launch(server_port=7860, share=False)
```

### Custom Interface Building

```python
import gradio as gr
from ui.components import ComponentFactory

# Build custom interface
with gr.Blocks(theme=ComponentFactory.get_theme()) as custom_demo:
    # Header
    header_components = ComponentFactory.create_header(
        title="# My Custom Tool",
        description="Specialized transcription interface"
    )
    
    # Main components
    with gr.Row():
        with gr.Column():
            audio_input = ComponentFactory.create_audio_input()
            transcribe_btn = ComponentFactory.create_action_button(
                "🎯 Process Audio",
                variant="primary"
            )
    
    with gr.Row():
        transcription_output = ComponentFactory.create_transcription_output(
            lines=15
        )
    
    # Event handling
    transcribe_btn.click(
        fn=my_transcription_function,
        inputs=[audio_input],
        outputs=[transcription_output]
    )

custom_demo.launch()
```

### Theme Customization

```python
from ui.components import ComponentFactory

# Get configured theme
theme = ComponentFactory.get_theme()

# Use in interface
with gr.Blocks(theme=theme) as demo:
    # Interface components
    pass
```

### Dynamic Instructions

```python
# Instructions adapt to configuration
instructions = ComponentFactory.create_instructions()

# Custom instructions
custom_instructions = ComponentFactory.create_instructions(
    title="## Quick Start Guide",
    instructions="1. Upload audio\n2. Wait for processing\n3. Review results"
)
```

---

## Event Handling

### Standard Event Patterns

```python
# Transcription event
transcribe_button.click(
    fn=transcription_handler,
    inputs=[audio_input],
    outputs=[transcription_output, download_file]
)

# Key points event
key_points_button.click(
    fn=key_points_handler,
    inputs=[transcription_output],
    outputs=[key_points_output]
)

# PRD generation event
prd_button.click(
    fn=prd_handler,
    inputs=[key_points_output],
    outputs=[prd_output, prd_download_file]
)
```

### Custom Event Handlers

```python
def custom_transcription_handler(audio_file):
    """Custom transcription processing"""
    if not audio_file:
        return "Please upload an audio file", gr.File(visible=False)
    
    # Custom processing logic
    result = my_custom_transcription(audio_file)
    temp_file = create_download_file(result)
    
    return result, gr.File(value=temp_file, visible=True)
```

---

## Best Practices

### Component Creation

```python
# Use ComponentFactory for consistency
from ui.components import ComponentFactory

# Good
audio_input = ComponentFactory.create_audio_input()

# Avoid direct instantiation unless customizing
# audio_input = AudioInputComponent().create()
```

### Configuration Integration

```python
# Components automatically use configuration
from config.settings import settings

# Theme is automatically applied
theme = ComponentFactory.get_theme()

# Instructions adapt to enabled features
instructions = ComponentFactory.create_instructions()
```

### Interface Organization

```python
# Organize components logically
with gr.Blocks() as demo:
    # Header section
    ComponentFactory.create_header()
    
    # Input section
    with gr.Row():
        audio_input = ComponentFactory.create_audio_input()
        transcribe_btn = ComponentFactory.create_action_button("Transcribe")
    
    # Output section
    with gr.Row():
        transcription_output = ComponentFactory.create_transcription_output()
    
    # Instructions section
    ComponentFactory.create_instructions()
```

### Error Handling

```python
def safe_transcription_handler(audio_file):
    """Transcription handler with error handling"""
    try:
        if not audio_file:
            return "Please upload an audio file", gr.File(visible=False)
        
        result = process_audio(audio_file)
        return result, gr.File(value=result_file, visible=True)
        
    except Exception as e:
        error_msg = f"Error processing audio: {str(e)}"
        return error_msg, gr.File(visible=False)
```

---

## Legacy Functions

For backward compatibility, these functions are available:

```python
from ui.components import (
    create_audio_input,
    create_transcription_output,
    create_key_points_output,
    create_prd_output,
    create_action_button
)

# Legacy functions (use ComponentFactory instead)
audio_input = create_audio_input()
transcription_output = create_transcription_output()
```

---

**UI Components API Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Development Team
