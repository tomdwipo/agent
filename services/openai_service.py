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
    SUCCESS_MESSAGES,
    TRD_SECTIONS
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
    
    def generate_prd_from_key_points(self, key_points_text, model=None):
        """
        Generate a Product Requirements Document from meeting key points
        
        Args:
            key_points_text (str): The meeting key points text to analyze
            model (str): OpenAI model to use (if None, uses configuration setting)
            
        Returns:
            str: Generated PRD in markdown format or error message
        """
        if not key_points_text or key_points_text.strip() == "":
            return ERROR_MESSAGES.get("no_key_points", "No key points provided for PRD generation.")
        
        # Check availability
        if not self.is_available():
            return self.get_availability_status()
        
        # Use configured model if not specified
        model = model or settings.openai_model
        
        try:
            # Create comprehensive PRD generation prompt
            prompt = f"""
Based on the following meeting key points, generate a comprehensive Product Requirements Document (PRD) in markdown format.

MEETING KEY POINTS:
{key_points_text}

Please create a structured PRD with the following sections:

# Product Requirements Document
*Generated from meeting analysis on [current date]*

## Executive Summary
[Provide a high-level overview of the product/feature, key value propositions, and strategic alignment based on the meeting discussion]

## Problem Statement
[Define the problem being solved, current pain points, challenges, and market opportunity mentioned in the meeting]

## Goals & Objectives
[List primary and secondary objectives, success criteria, and business goals alignment from the discussion]

## User Stories/Requirements
[Extract and format functional requirements, user personas, use cases, and acceptance criteria mentioned]

## Success Metrics
[Identify Key Performance Indicators (KPIs), measurable outcomes, and success benchmarks discussed]

## Timeline/Milestones
[Outline development phases, key deliverables, and timeline estimates if mentioned in the meeting]

## Technical Requirements
[List system requirements, technical constraints, and integration needs discussed]

## Risk Assessment
[Identify potential risks, challenges, mitigation strategies, and contingency plans mentioned or implied]

IMPORTANT GUIDELINES:
- Base the PRD content strictly on information from the meeting key points
- If specific information is not available in the key points, note "To be determined" or "Not specified in meeting"
- Use professional product management language and formatting
- Make reasonable inferences where appropriate but clearly distinguish between explicit and inferred information
- Ensure each section is substantive and actionable
- Use bullet points, numbered lists, and clear formatting for readability
"""

            # Call OpenAI API with PRD-specific settings
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert product manager who creates comprehensive Product Requirements Documents. Generate well-structured, professional PRDs based on meeting discussions."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=getattr(settings, 'prd_max_tokens', 2000),
                temperature=getattr(settings, 'prd_temperature', 0.3)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return ERROR_MESSAGES.get("openai_request_failed", "❌ Error generating PRD: {error}").format(error=str(e))

    def generate_android_trd_from_prd(self, prd_content: str) -> str:
        """
        Generate Android TRD from PRD content using OpenAI GPT.
        
        Args:
            prd_content (str): Complete PRD markdown content
            
        Returns:
            str: Generated Android TRD in markdown format
        """
        if not prd_content or prd_content.strip() == "":
            return ERROR_MESSAGES["no_prd_content"]

        if not settings.enable_trd_generation:
            return ERROR_MESSAGES["trd_feature_disabled"]

        if not self.is_available():
            return self.get_availability_status()

        try:
            TRD_SECTIONS_STR = "\n- ".join(TRD_SECTIONS)
            prompt = f"""
You are an expert technical writer specializing in Android development. Your task is to generate a comprehensive Technical Requirements Document (TRD) for an Android application based on the provided Product Requirements Document (PRD).

The TRD must follow this exact 7-section structure:
1.  **Architecture Overview**: High-level system architecture, core components, data flow, and libraries.
2.  **UI/UX Specifications**: Screen hierarchy, UI components, user interactions, and design principles.
3.  **API Requirements**: Backend integration, REST endpoints, data models, and error handling.
4.  **Database Schema**: Local data storage, entities, DAOs, and caching strategies.
5.  **Security Requirements**: Data encryption, authentication, and permission handling.
6.  **Performance Requirements**: Response times, memory usage, and optimization strategies.
7.  **Testing Strategy**: Unit, integration, UI, and performance testing approaches.

Here are the required sections for the TRD:
- {TRD_SECTIONS_STR}

Based on the PRD below, generate a detailed, actionable TRD in markdown format.

---
**PRODUCT REQUIREMENTS DOCUMENT (PRD):**

{prd_content}
---

**IMPORTANT GUIDELINES:**
-   **Strict Adherence**: Generate content for all 7 sections listed above. Do not add, remove, or rename sections.
-   **Technical Depth**: Provide moderate technical detail. Suggest specific patterns (MVVM, Clean Architecture), libraries (Retrofit, Room, Hilt), and implementation strategies.
-   **Actionable Content**: The output should be a practical guide for the development team.
-   **Infer and Specify**: Where the PRD is high-level, make reasonable technical inferences. For example, if the PRD mentions "user login," the TRD should specify OAuth 2.0, token storage, and session management.
-   **Placeholder for Ambiguity**: If a requirement is too vague to detail, use placeholders like "[To be defined: specific algorithm]" or "[Requires clarification: ...]".
-   **Formatting**: Use markdown for clear, structured formatting with headings, subheadings, bullet points, and code blocks.
"""

            response = self.client.chat.completions.create(
                model=settings.trd_openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical writer creating detailed Android Technical Requirements Documents (TRDs) from Product Requirements Documents (PRDs)."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=settings.trd_max_tokens,
                temperature=settings.trd_temperature
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return ERROR_MESSAGES["trd_generation_failed"].format(error=str(e))


# Global instance for backward compatibility
_openai_service = OpenAIService()

def generate_meeting_key_points(transcription_text):
    """
    Legacy function for backward compatibility
    Generate key meeting points from transcription using OpenAI GPT
    """
    return _openai_service.generate_meeting_key_points(transcription_text)

def generate_prd_from_key_points(key_points_text):
    """
    Legacy function for backward compatibility
    Generate PRD from meeting key points using OpenAI GPT
    """
    return _openai_service.generate_prd_from_key_points(key_points_text)
