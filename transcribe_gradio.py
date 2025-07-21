# -*- coding: utf-8 -*-
"""
Main Audio Transcription Application

This is the main entry point for the audio transcription application.
Now uses the modular UI components for better maintainability.
"""

# Import UI interface
from ui.gradio_interface import launch_interface

if __name__ == "__main__":
    # Launch the interface using the new UI module
    launch_interface()
