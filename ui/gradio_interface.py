"""
Gradio Interface Module

Contains the main Gradio interface implementation using reusable UI components.
"""

import gradio as gr
from typing import Tuple, Optional
from config.settings import settings
from config.constants import UI_LABELS
from ui.components import ComponentFactory
from services.whisper_service import transcribe_audio_gradio
from services.openai_service import generate_meeting_key_points


class GradioInterface:
    """Main Gradio interface class"""
    
    def __init__(self):
        """Initialize the Gradio interface"""
        self.gradio_config = settings.get_gradio_config()
        self.interface = None
        
        # UI components
        self.audio_input = None
        self.transcribe_btn = None
        self.transcription_output = None
        self.download_file = None
        self.key_points_btn = None
        self.key_points_output = None
    
    def create_interface(self) -> gr.Blocks:
        """Create and configure the complete Gradio interface"""
        
        with gr.Blocks(
            title=self.gradio_config["title"], 
            theme=ComponentFactory.get_theme()
        ) as interface:
            
            # Header section
            self._create_header()
            
            # Main transcription section
            self._create_transcription_section()
            
            # Key points section (if enabled)
            if settings.enable_key_points:
                self._create_key_points_section()
            
            # Instructions section
            self._create_instructions_section()
            
            # Settings display (if in debug mode)
            if self.gradio_config["debug"]:
                self._create_settings_section()
            
            # Set up event handlers
            self._setup_event_handlers()
        
        self.interface = interface
        return interface
    
    def _create_header(self):
        """Create the header section"""
        header_components = ComponentFactory.create_header()
        # Components are automatically rendered when created in Gradio context
        # No need to call render() explicitly
    
    def _create_transcription_section(self):
        """Create the main transcription section"""
        with gr.Row():
            with gr.Column():
                # Audio input
                self.audio_input = ComponentFactory.create_audio_input()
                
                # Transcribe button
                self.transcribe_btn = ComponentFactory.create_action_button(
                    text=UI_LABELS["transcribe_button"],
                    variant="primary"
                )
        
        with gr.Row():
            with gr.Column():
                # Transcription output
                self.transcription_output = ComponentFactory.create_transcription_output()
                
                # Download file
                self.download_file = ComponentFactory.create_download_file()
    
    def _create_key_points_section(self):
        """Create the key points section"""
        with gr.Row():
            with gr.Column():
                # Key points button
                self.key_points_btn = ComponentFactory.create_action_button(
                    text=UI_LABELS["key_points_button"],
                    variant="secondary"
                )
                
                # Key points output
                self.key_points_output = ComponentFactory.create_key_points_output()
    
    def _create_instructions_section(self):
        """Create the instructions section"""
        instructions_components = ComponentFactory.create_instructions()
        # Components are automatically rendered when created in Gradio context
    
    def _create_settings_section(self):
        """Create the settings display section (debug mode only)"""
        with gr.Accordion("Current Settings", open=False):
            settings_display = ComponentFactory.create_settings_display()
            # Component is automatically rendered when created in Gradio context
    
    def _setup_event_handlers(self):
        """Set up event handlers for UI components"""
        
        # Transcription event handler
        self.transcribe_btn.click(
            fn=self._process_transcription,
            inputs=[self.audio_input],
            outputs=[self.transcription_output, self.download_file]
        )
        
        # Key points event handler (if enabled)
        if settings.enable_key_points and self.key_points_btn:
            self.key_points_btn.click(
                fn=self._process_key_points,
                inputs=[self.transcription_output],
                outputs=[self.key_points_output]
            )
    
    def _process_transcription(self, audio) -> Tuple[str, gr.File]:
        """
        Process audio transcription
        
        Args:
            audio: Audio file from Gradio input
            
        Returns:
            Tuple of (transcription_text, download_file)
        """
        if audio is None:
            return "Please upload an audio file first.", gr.File(visible=False)
        
        transcription, temp_file_path = transcribe_audio_gradio(audio)
        
        if temp_file_path:
            return transcription, gr.File(value=temp_file_path, visible=True)
        else:
            return transcription, gr.File(visible=False)
    
    def _process_key_points(self, transcription: str) -> str:
        """
        Process key points generation
        
        Args:
            transcription: Transcription text
            
        Returns:
            Generated key points or error message
        """
        if not transcription or transcription.strip() == "":
            return "Please transcribe audio first before generating key meeting points."
        
        return generate_meeting_key_points(transcription)
    
    def launch(self, **kwargs):
        """
        Launch the Gradio interface
        
        Args:
            **kwargs: Additional launch parameters
        """
        if not self.interface:
            self.create_interface()
        
        # Merge configuration with any provided kwargs
        launch_config = {
            "server_name": self.gradio_config["server_name"],
            "server_port": self.gradio_config["server_port"],
            "share": self.gradio_config["share"],
            "debug": self.gradio_config["debug"]
        }
        launch_config.update(kwargs)
        
        return self.interface.launch(**launch_config)


class SimpleGradioInterface:
    """Simplified Gradio interface for basic use cases"""
    
    def __init__(self, enable_key_points: Optional[bool] = None):
        """
        Initialize simplified interface
        
        Args:
            enable_key_points: Override key points setting
        """
        self.enable_key_points = enable_key_points if enable_key_points is not None else settings.enable_key_points
    
    def create_interface(self) -> gr.Interface:
        """Create a simple Gradio interface"""
        
        def process_audio(audio):
            """Simple audio processing function"""
            if audio is None:
                return "Please upload an audio file."
            
            transcription, _ = transcribe_audio_gradio(audio)
            return transcription
        
        # Create simple interface
        interface = gr.Interface(
            fn=process_audio,
            inputs=gr.Audio(type="filepath", sources=["upload"]),
            outputs=gr.Textbox(label="Transcription", lines=10),
            title=settings.app_title,
            description="Upload an audio file to get transcription"
        )
        
        return interface


class CustomGradioInterface:
    """Customizable Gradio interface for advanced use cases"""
    
    def __init__(self, 
                 custom_components: Optional[dict] = None,
                 custom_handlers: Optional[dict] = None):
        """
        Initialize custom interface
        
        Args:
            custom_components: Custom component configurations
            custom_handlers: Custom event handlers
        """
        self.custom_components = custom_components or {}
        self.custom_handlers = custom_handlers or {}
    
    def create_interface(self) -> gr.Blocks:
        """Create a customizable Gradio interface"""
        
        with gr.Blocks(theme=ComponentFactory.get_theme()) as interface:
            
            # Use custom or default components
            if "header" in self.custom_components:
                self.custom_components["header"]()
            else:
                header_components = ComponentFactory.create_header()
                for component in header_components:
                    component.render()
            
            # Audio input section
            audio_input = ComponentFactory.create_audio_input(
                **self.custom_components.get("audio_input", {})
            )
            
            # Transcription output
            transcription_output = ComponentFactory.create_transcription_output(
                **self.custom_components.get("transcription_output", {})
            )
            
            # Custom event handlers
            if "transcription_handler" in self.custom_handlers:
                # Use custom handler
                pass
            else:
                # Use default handler
                pass
        
        return interface


# Factory function for creating interfaces
def create_gradio_interface(interface_type: str = "standard", **kwargs) -> gr.Blocks:
    """
    Factory function to create different types of Gradio interfaces
    
    Args:
        interface_type: Type of interface ("standard", "simple", "custom")
        **kwargs: Additional configuration parameters
        
    Returns:
        Configured Gradio interface
    """
    if interface_type == "simple":
        return SimpleGradioInterface(**kwargs).create_interface()
    elif interface_type == "custom":
        return CustomGradioInterface(**kwargs).create_interface()
    else:  # standard
        return GradioInterface().create_interface()


# Convenience function for backward compatibility
def create_interface() -> gr.Blocks:
    """Create the standard Gradio interface"""
    return GradioInterface().create_interface()


# Main interface launcher
def launch_interface(**kwargs):
    """
    Launch the Gradio interface with configuration
    
    Args:
        **kwargs: Launch configuration parameters
    """
    # Print settings summary
    settings.print_settings_summary()
    
    # Create and launch interface
    gradio_interface = GradioInterface()
    return gradio_interface.launch(**kwargs)
