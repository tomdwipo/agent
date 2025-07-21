"""
File Service Module

Handles file operations including temporary file creation, downloads, and file management.
"""

import tempfile
import os
from pathlib import Path
from config.settings import settings
from config.constants import (
    SUPPORTED_AUDIO_EXTENSIONS,
    SUPPORTED_AUDIO_FORMATS,
    DEFAULT_MAX_FILE_SIZE_MB,
    TEMP_FILE_SETTINGS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    get_supported_formats_string,
    is_supported_audio_format
)


class FileService:
    """Service class for handling file operations"""
    
    def __init__(self):
        """Initialize FileService"""
        pass
    
    def create_temp_text_file(self, content, suffix=None, prefix=None):
        """
        Create a temporary text file with the given content
        
        Args:
            content (str): Content to write to the file
            suffix (str): File suffix (if None, uses configuration setting)
            prefix (str): File prefix (if None, uses configuration setting)
            
        Returns:
            str: Path to the created temporary file, or None if failed
        """
        # Use configured values if not specified
        suffix = suffix or settings.download_file_suffix
        prefix = prefix or settings.temp_file_prefix
        
        try:
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix=suffix,
                prefix=prefix,
                delete=False,
                encoding=TEMP_FILE_SETTINGS["encoding"]
            )
            temp_file.write(content)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            print(ERROR_MESSAGES["file_creation_failed"].format(error=str(e)))
            return None
    
    def create_download_file(self, content, filename=None):
        """
        Create a file for download with the given content
        
        Args:
            content (str): Content to write to the file
            filename (str): Optional filename, if None creates temp file
            
        Returns:
            str: Path to the created file, or None if failed
        """
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                return filename
            except Exception as e:
                print(f"Error creating download file: {e}")
                return None
        else:
            return self.create_temp_text_file(content)
    
    def validate_audio_file(self, file_path):
        """
        Validate if the file is a supported audio format
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file_path:
            return False, ERROR_MESSAGES["no_file"]
        
        if not os.path.exists(file_path):
            return False, ERROR_MESSAGES["file_not_found"].format(file_path=file_path)
        
        # Check file extension using configuration constants
        file_extension = Path(file_path).suffix.lower()
        
        if not is_supported_audio_format(file_extension):
            return False, ERROR_MESSAGES["invalid_format"].format(formats=get_supported_formats_string())
        
        # Check file size using configuration setting
        try:
            file_size = os.path.getsize(file_path)
            max_size_bytes = settings.max_file_size_mb * 1024 * 1024
            if file_size > max_size_bytes:
                return False, ERROR_MESSAGES["file_too_large"].format(max_size=settings.max_file_size_mb)
        except Exception as e:
            return False, f"Error checking file size: {e}"
        
        return True, "File is valid"
    
    def get_file_info(self, file_path):
        """
        Get information about a file
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: File information or None if error
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            path_obj = Path(file_path)
            
            return {
                'name': path_obj.name,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'extension': path_obj.suffix.lower(),
                'modified': stat.st_mtime,
                'path': file_path
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    def cleanup_temp_file(self, file_path):
        """
        Clean up a temporary file
        
        Args:
            file_path (str): Path to the temporary file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error cleaning up temporary file: {e}")
            return False
    
    def save_transcription(self, transcription_text, output_path):
        """
        Save transcription to a specific file path
        
        Args:
            transcription_text (str): The transcription text
            output_path (str): Path where to save the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcription_text)
            
            return True
        except Exception as e:
            print(f"Error saving transcription: {e}")
            return False


# Global instance for easy access
_file_service = FileService()

def create_temp_text_file(content, suffix='.txt'):
    """
    Legacy function for backward compatibility
    Create a temporary text file with the given content
    """
    return _file_service.create_temp_text_file(content, suffix)

def validate_audio_file(file_path):
    """
    Legacy function for backward compatibility
    Validate if the file is a supported audio format
    """
    return _file_service.validate_audio_file(file_path)
