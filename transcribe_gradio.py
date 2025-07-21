# -*- coding: utf-8 -*-
import gradio as gr
import os
from pathlib import Path

# Import configuration
from config.settings import settings
from config.constants import UI_LABELS, UI_PLACEHOLDERS, UI_INSTRUCTIONS

# Import services
from services.whisper_service import WhisperService, transcribe_audio_gradio, load_whisper_model
from services.openai_service import OpenAIService, generate_meeting_key_points
from services.file_service import FileService

# Initialize services with configuration
whisper_service = WhisperService()
openai_service = OpenAIService()
file_service = FileService()

def create_gradio_interface():
    """Create and configure the Gradio interface"""
    
    # Get Gradio configuration
    gradio_config = settings.get_gradio_config()
    
    with gr.Blocks(title=gradio_config["title"], theme=getattr(gr.themes, gradio_config["theme"].capitalize())()) as interface:
        gr.Markdown(UI_LABELS["app_title"])
        gr.Markdown(gradio_config["description"])
        
        with gr.Row():
            with gr.Column():
                # Audio input
                audio_input = gr.Audio(
                    label=UI_LABELS["upload_label"],
                    type="filepath",
                    sources=["upload"]
                )
                
                # Transcribe button
                transcribe_btn = gr.Button(UI_LABELS["transcribe_button"], variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                # Output text area
                transcription_output = gr.Textbox(
                    label=UI_LABELS["transcription_label"],
                    placeholder=UI_PLACEHOLDERS["transcription"],
                    lines=10,
                    max_lines=20,
                    show_copy_button=True
                )
                
                # Download file
                download_file = gr.File(
                    label=UI_LABELS["download_label"],
                    visible=False
                )
        
        # Key Meeting Points Section (only show if enabled)
        if settings.enable_key_points:
            with gr.Row():
                with gr.Column():
                    # Generate key points button
                    key_points_btn = gr.Button(UI_LABELS["key_points_button"], variant="secondary", size="lg")
                    
                    # Key points output
                    key_points_output = gr.Textbox(
                        label=UI_LABELS["key_points_label"],
                        placeholder=UI_PLACEHOLDERS["key_points"],
                        lines=15,
                        max_lines=25,
                        show_copy_button=True
                    )
        
        # Event handlers
        def process_transcription(audio):
            if audio is None:
                return "Please upload an audio file first.", gr.File(visible=False)
            
            transcription, temp_file_path = transcribe_audio_gradio(audio)
            
            if temp_file_path:
                return transcription, gr.File(value=temp_file_path, visible=True)
            else:
                return transcription, gr.File(visible=False)
        
        transcribe_btn.click(
            fn=process_transcription,
            inputs=[audio_input],
            outputs=[transcription_output, download_file]
        )
        
        # Key points event handler (only if enabled)
        if settings.enable_key_points:
            def process_key_points(transcription):
                if not transcription or transcription.strip() == "":
                    return "Please transcribe audio first before generating key meeting points."
                
                return generate_meeting_key_points(transcription)
            
            key_points_btn.click(
                fn=process_key_points,
                inputs=[transcription_output],
                outputs=[key_points_output]
            )
        
        # Instructions section
        gr.Markdown(UI_LABELS["instructions_title"])
        gr.Markdown(UI_INSTRUCTIONS)
    
    return interface

if __name__ == "__main__":
    # Print settings summary
    settings.print_settings_summary()
    
    # Create and launch the interface
    interface = create_gradio_interface()
    
    # Get Gradio configuration
    gradio_config = settings.get_gradio_config()
    
    # Launch with configuration settings
    interface.launch(
        server_name=gradio_config["server_name"],
        server_port=gradio_config["server_port"],
        share=gradio_config["share"],
        debug=gradio_config["debug"]
    )
