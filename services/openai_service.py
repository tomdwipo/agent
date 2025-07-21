"""
OpenAI Service Module

Handles OpenAI API integration for generating meeting key points and other AI-powered features.
"""

import os
from openai import OpenAI
from config.settings import settings
from config.constants import (
    DEFAULT_OPENAI_MODEL,
    DEFAULT_OPENAI_MAX_TOKENS,
    DEFAULT_OPENAI_TEMPERATURE,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)

OPENAI_AVAILABLE = True


class OpenAIService:
    """Service class for handling OpenAI API operations"""
    
    def __init__(self):
        """Initialize OpenAIService"""
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client if API key is available"""
        if settings.is_openai_configured():
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def is_available(self):
        """
        Check if OpenAI service is available
        
        Returns:
            bool: True if OpenAI is available and configured
        """
        return OPENAI_AVAILABLE and self.client is not None
    
    def get_availability_status(self):
        """
        Get detailed availability status
        
        Returns:
            str: Status message explaining availability
        """
        if not OPENAI_AVAILABLE:
            return "❌ OpenAI library not installed. Please install it with: pip install openai"
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-openai-api-key-here":
            return "❌ OpenAI API key not configured. Please add your API key to the .env file."
        
        if not self.client:
            return "❌ OpenAI client initialization failed. Please check your API key."
        
        return "✅ OpenAI service is available and configured."
    
    def generate_meeting_key_points(self, transcription_text, model=None):
        """
        Generate key meeting points from transcription using OpenAI GPT
        
        Args:
            transcription_text (str): The transcription text to analyze
            model (str): OpenAI model to use (if None, uses configuration setting)
            
        Returns:
            str: Generated key meeting points or error message
        """
        if not transcription_text or transcription_text.strip() == "":
            return ERROR_MESSAGES["no_transcription"]
        
        # Check availability
        if not self.is_available():
            return self.get_availability_status()
        
        # Use configured model if not specified
        model = model or settings.openai_model
        
        try:
            # Create prompt for key meeting points extraction
            prompt = f"""
Please analyze the following meeting transcription and extract key information in a structured format:

TRANSCRIPTION:
{transcription_text}

Please provide the analysis in the following format:

## 📋 Meeting Summary
[2-3 sentence summary of the meeting]

## 🎯 Key Topics Discussed
• [Topic 1]
• [Topic 2]
• [Topic 3]

## ✅ Action Items
• [Action item 1 - Person responsible if mentioned]
• [Action item 2 - Person responsible if mentioned]

## 🔑 Decisions Made
• [Decision 1]
• [Decision 2]

## 🚀 Next Steps
• [Next step 1]
• [Next step 2]

## 👥 Participants (if mentioned)
• [Participant names if clearly mentioned]

Focus on extracting concrete, actionable information. If certain sections don't apply or aren't clear from the transcription, you can omit them or note "Not specified in the transcription."
"""

            # Call OpenAI API with configured settings
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that extracts key meeting points from transcriptions. Provide clear, structured summaries."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return ERROR_MESSAGES["openai_request_failed"].format(error=str(e))
    
    def generate_custom_analysis(self, transcription_text, custom_prompt, model="gpt-3.5-turbo"):
        """
        Generate custom analysis from transcription using a custom prompt
        
        Args:
            transcription_text (str): The transcription text to analyze
            custom_prompt (str): Custom prompt for analysis
            model (str): OpenAI model to use (default: gpt-3.5-turbo)
            
        Returns:
            str: Generated analysis or error message
        """
        if not transcription_text or transcription_text.strip() == "":
            return "No transcription text provided."
        
        if not custom_prompt or custom_prompt.strip() == "":
            return "No custom prompt provided."
        
        # Check availability
        if not self.is_available():
            return self.get_availability_status()
        
        try:
            full_prompt = f"{custom_prompt}\n\nTRANSCRIPTION:\n{transcription_text}"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that analyzes transcriptions based on user requirements."
                    },
                    {
                        "role": "user", 
                        "content": full_prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ Error generating custom analysis: {str(e)}\n\nPlease check your OpenAI API key and internet connection."


# Global instance for backward compatibility
_openai_service = OpenAIService()

def generate_meeting_key_points(transcription_text):
    """
    Legacy function for backward compatibility
    Generate key meeting points from transcription using OpenAI GPT
    """
    return _openai_service.generate_meeting_key_points(transcription_text)
