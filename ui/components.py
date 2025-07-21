"""
UI Components Module

Contains reusable Gradio UI components for the audio transcription application.
"""

import gradio as gr
from typing import Optional, Dict, Any, List
from config.settings import settings
from config.constants import UI_LABELS, UI_PLACEHOLDERS, get_supported_formats_string


class AudioInputComponent:
    """Reusable audio input component"""
    
    def __init__(self, label: Optional[str] = None, sources: Optional[List[str]] = None):
        """
        Initialize audio input component
        
        Args:
            label: Custom label for the audio input
            sources: List of input sources (default: ["upload"])
        """
        self.label = label or UI_LABELS["upload_label"]
        self.sources = sources or ["upload"]
    
    def create(self) -> gr.Audio:
        """Create and return the audio input component"""
        return gr.Audio(
            label=self.label,
            type="filepath",
            sources=self.sources
        )


class TranscriptionOutputComponent:
    """Reusable transcription output component"""
    
    def __init__(self, 
                 label: Optional[str] = None, 
                 placeholder: Optional[str] = None,
                 lines: int = 10,
                 max_lines: int = 20):
        """
        Initialize transcription output component
        
        Args:
            label: Custom label for the output
            placeholder: Custom placeholder text
            lines: Number of visible lines
            max_lines: Maximum number of lines
        """
        self.label = label or UI_LABELS["transcription_label"]
        self.placeholder = placeholder or UI_PLACEHOLDERS["transcription"]
        self.lines = lines
        self.max_lines = max_lines
    
    def create(self) -> gr.Textbox:
        """Create and return the transcription output component"""
        return gr.Textbox(
            label=self.label,
            placeholder=self.placeholder,
            lines=self.lines,
            max_lines=self.max_lines,
            show_copy_button=True
        )


class KeyPointsOutputComponent:
    """Reusable key points output component"""
    
    def __init__(self, 
                 label: Optional[str] = None, 
                 placeholder: Optional[str] = None,
                 lines: int = 15,
                 max_lines: int = 25):
        """
        Initialize key points output component
        
        Args:
            label: Custom label for the output
            placeholder: Custom placeholder text
            lines: Number of visible lines
            max_lines: Maximum number of lines
        """
        self.label = label or UI_LABELS["key_points_label"]
        self.placeholder = placeholder or UI_PLACEHOLDERS["key_points"]
        self.lines = lines
        self.max_lines = max_lines
    
    def create(self) -> gr.Textbox:
        """Create and return the key points output component"""
        return gr.Textbox(
            label=self.label,
            placeholder=self.placeholder,
            lines=self.lines,
            max_lines=self.max_lines,
            show_copy_button=True
        )


class ActionButtonComponent:
    """Reusable action button component"""
    
    def __init__(self, 
                 text: str,
                 variant: str = "primary",
                 size: str = "lg",
                 icon: Optional[str] = None):
        """
        Initialize action button component
        
        Args:
            text: Button text
            variant: Button variant (primary, secondary, etc.)
            size: Button size (sm, md, lg)
            icon: Optional icon for the button
        """
        self.text = text
        self.variant = variant
        self.size = size
        self.icon = icon
    
    def create(self) -> gr.Button:
        """Create and return the action button component"""
        return gr.Button(
            self.text,
            variant=self.variant,
            size=self.size
        )


class DownloadFileComponent:
    """Reusable download file component"""
    
    def __init__(self, label: Optional[str] = None, visible: bool = False):
        """
        Initialize download file component
        
        Args:
            label: Custom label for the file component
            visible: Initial visibility state
        """
        self.label = label or UI_LABELS["download_label"]
        self.visible = visible
    
    def create(self) -> gr.File:
        """Create and return the download file component"""
        return gr.File(
            label=self.label,
            visible=self.visible
        )


class HeaderComponent:
    """Reusable header component"""
    
    def __init__(self, title: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize header component
        
        Args:
            title: Custom title
            description: Custom description
        """
        gradio_config = settings.get_gradio_config()
        self.title = title or UI_LABELS["app_title"]
        self.description = description or gradio_config["description"]
    
    def create(self) -> List[gr.Markdown]:
        """Create and return header components"""
        return [
            gr.Markdown(self.title),
            gr.Markdown(self.description)
        ]


class InstructionsComponent:
    """Reusable instructions component"""
    
    def __init__(self, 
                 title: Optional[str] = None, 
                 instructions: Optional[str] = None):
        """
        Initialize instructions component
        
        Args:
            title: Custom instructions title
            instructions: Custom instructions text
        """
        self.title = title or UI_LABELS["instructions_title"]
        self.instructions = instructions or self._get_dynamic_instructions()
    
    def _get_dynamic_instructions(self) -> str:
        """Generate dynamic instructions based on configuration"""
        supported_formats = get_supported_formats_string()
        
        base_instructions = f"""
1. Click on the audio upload area above to select your audio file
2. Supported formats: {supported_formats}
3. Click 'Transcribe Audio' to start the process
4. The transcription will appear in the text area below"""
        
        if settings.enable_key_points:
            base_instructions += """
5. Click 'Generate Key Meeting Points' to get AI-powered meeting summary
6. You can copy both the transcription and key points, or download the transcription as a .txt file

**Note:** To use the key meeting points feature, you need to add your OpenAI API key to the .env file."""
        else:
            base_instructions += """
5. You can copy the transcription or download it as a .txt file"""
        
        return base_instructions
    
    def create(self) -> List[gr.Markdown]:
        """Create and return instructions components"""
        return [
            gr.Markdown(self.title),
            gr.Markdown(self.instructions)
        ]


class StatusIndicatorComponent:
    """Reusable status indicator component"""
    
    def __init__(self, initial_status: str = "Ready"):
        """
        Initialize status indicator component
        
        Args:
            initial_status: Initial status text
        """
        self.initial_status = initial_status
    
    def create(self) -> gr.Textbox:
        """Create and return status indicator component"""
        return gr.Textbox(
            label="Status",
            value=self.initial_status,
            interactive=False,
            max_lines=1
        )


class ProgressBarComponent:
    """Reusable progress bar component"""
    
    def __init__(self, visible: bool = False):
        """
        Initialize progress bar component
        
        Args:
            visible: Initial visibility state
        """
        self.visible = visible
    
    def create(self) -> gr.Progress:
        """Create and return progress bar component"""
        return gr.Progress(visible=self.visible)


class SettingsDisplayComponent:
    """Component to display current settings"""
    
    def __init__(self):
        """Initialize settings display component"""
        pass
    
    def create(self) -> gr.Markdown:
        """Create and return settings display component"""
        settings_info = self._get_settings_info()
        return gr.Markdown(f"**Current Settings:**\n{settings_info}")
    
    def _get_settings_info(self) -> str:
        """Get formatted settings information"""
        info_lines = [
            f"- Whisper Model: {settings.whisper_model}",
            f"- Max File Size: {settings.max_file_size_mb}MB",
            f"- OpenAI Configured: {'✅' if settings.is_openai_configured() else '❌'}",
            f"- Key Points: {'Enabled' if settings.enable_key_points else 'Disabled'}"
        ]
        return "\n".join(info_lines)


class ThemeComponent:
    """Component for theme management"""
    
    def __init__(self):
        """Initialize theme component"""
        self.gradio_config = settings.get_gradio_config()
    
    def get_theme(self):
        """Get the configured Gradio theme"""
        theme_name = self.gradio_config["theme"]
        try:
            return getattr(gr.themes, theme_name.capitalize())()
        except AttributeError:
            # Fallback to default theme if configured theme doesn't exist
            return gr.themes.Soft()


class ComponentFactory:
    """Factory class for creating UI components"""
    
    @staticmethod
    def create_audio_input(**kwargs) -> gr.Audio:
        """Create audio input component"""
        return AudioInputComponent(**kwargs).create()
    
    @staticmethod
    def create_transcription_output(**kwargs) -> gr.Textbox:
        """Create transcription output component"""
        return TranscriptionOutputComponent(**kwargs).create()
    
    @staticmethod
    def create_key_points_output(**kwargs) -> gr.Textbox:
        """Create key points output component"""
        return KeyPointsOutputComponent(**kwargs).create()
    
    @staticmethod
    def create_action_button(text: str, **kwargs) -> gr.Button:
        """Create action button component"""
        return ActionButtonComponent(text, **kwargs).create()
    
    @staticmethod
    def create_download_file(**kwargs) -> gr.File:
        """Create download file component"""
        return DownloadFileComponent(**kwargs).create()
    
    @staticmethod
    def create_header(**kwargs) -> List[gr.Markdown]:
        """Create header components"""
        return HeaderComponent(**kwargs).create()
    
    @staticmethod
    def create_instructions(**kwargs) -> List[gr.Markdown]:
        """Create instructions components"""
        return InstructionsComponent(**kwargs).create()
    
    @staticmethod
    def create_status_indicator(**kwargs) -> gr.Textbox:
        """Create status indicator component"""
        return StatusIndicatorComponent(**kwargs).create()
    
    @staticmethod
    def create_progress_bar(**kwargs) -> gr.Progress:
        """Create progress bar component"""
        return ProgressBarComponent(**kwargs).create()
    
    @staticmethod
    def create_settings_display() -> gr.Markdown:
        """Create settings display component"""
        return SettingsDisplayComponent().create()
    
    @staticmethod
    def get_theme():
        """Get configured theme"""
        return ThemeComponent().get_theme()


# Convenience functions for backward compatibility
def create_audio_input(**kwargs):
    """Create audio input component"""
    return ComponentFactory.create_audio_input(**kwargs)

def create_transcription_output(**kwargs):
    """Create transcription output component"""
    return ComponentFactory.create_transcription_output(**kwargs)

def create_key_points_output(**kwargs):
    """Create key points output component"""
    return ComponentFactory.create_key_points_output(**kwargs)

def create_action_button(text: str, **kwargs):
    """Create action button component"""
    return ComponentFactory.create_action_button(text, **kwargs)
