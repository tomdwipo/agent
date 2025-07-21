"""
Whisper Service Module

Handles OpenAI Whisper model loading, caching, and audio transcription functionality.
"""

import whisper
import tempfile
from pathlib import Path
from config.settings import settings
from config.constants import (
    DEFAULT_WHISPER_MODEL, 
    WHISPER_MODEL_NAMES,
    TEMP_FILE_SETTINGS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)


class WhisperService:
    """Service class for handling Whisper model operations"""
    
    def __init__(self, model_name=None):
        """
        Initialize WhisperService
        
        Args:
            model_name (str): Whisper model name (tiny, base, small, medium, large)
                             If None, uses configuration setting
        """
        self.model_name = model_name or settings.whisper_model
        self.model = None
        
        # Validate model name
        if self.model_name not in WHISPER_MODEL_NAMES:
            print(f"Warning: Invalid model name '{self.model_name}'. Using default '{DEFAULT_WHISPER_MODEL}'")
            self.model_name = DEFAULT_WHISPER_MODEL
    
    def load_model(self):
        """
        Load the Whisper model once and cache it
        
        Returns:
            whisper.Whisper: Loaded Whisper model
        """
        if self.model is None:
            print(f"Loading Whisper model ({self.model_name})...")
            self.model = whisper.load_model(self.model_name)
            print("Model loaded successfully.")
        return self.model
    
    def transcribe_audio(self, audio_path):
        """
        Transcribe an audio file using the loaded Whisper model
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            tuple: (transcription_text, temp_file_path) or (error_message, None)
        """
        if not audio_path:
            return "Please provide an audio file path.", None
        
        try:
            # Load model if not already loaded
            whisper_model = self.load_model()
            
            print(f"Starting transcription for '{audio_path}'...")
            
            # Transcribe the audio
            result = whisper_model.transcribe(audio_path, fp16=False)
            transcription_text = result["text"].strip()
            
            # Create a temporary text file for download
            temp_file = tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.txt', 
                delete=False, 
                encoding='utf-8'
            )
            temp_file.write(transcription_text)
            temp_file.close()
            
            return transcription_text, temp_file.name
            
        except Exception as e:
            error_msg = f"An error occurred during transcription: {str(e)}"
            print(error_msg)
            return error_msg, None
    
    def transcribe_for_gradio(self, audio_file):
        """
        Transcribe audio specifically for Gradio interface
        
        Args:
            audio_file: Gradio audio file object or path
            
        Returns:
            tuple: (transcription_text, temp_file_path) or (error_message, None)
        """
        if audio_file is None:
            return "Please upload an audio file.", None
        
        # Get the file path from the uploaded file
        audio_path = audio_file.name if hasattr(audio_file, 'name') else audio_file
        
        return self.transcribe_audio(audio_path)


# Global instance for backward compatibility
_whisper_service = WhisperService()

def load_whisper_model():
    """
    Legacy function for backward compatibility
    Load the Whisper model once and cache it
    """
    return _whisper_service.load_model()

def transcribe_audio_gradio(audio_file):
    """
    Legacy function for backward compatibility
    Transcribes an audio file using OpenAI's Whisper model for Gradio interface.
    """
    return _whisper_service.transcribe_for_gradio(audio_file)
