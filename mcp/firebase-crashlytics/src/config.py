"""Configuration module for Firebase Crashlytics MCP Server."""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration management for Firebase Crashlytics MCP Server."""
    
    def __init__(self):
        load_dotenv()
        
        # Firebase configuration
        self.firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
        self.firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        self.firebase_app_id = os.getenv("FIREBASE_APP_ID")
        
        # OpenAI configuration for AI solutions
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        self.openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        
        # Crashlytics API configuration
        self.crashlytics_api_base = "https://firebase.googleapis.com/v1beta1"
        self.max_crashes_per_request = int(os.getenv("MAX_CRASHES_PER_REQUEST", "50"))
        
        # AI analysis configuration
        self.enable_ai_solutions = os.getenv("ENABLE_AI_SOLUTIONS", "true").lower() == "true"
        self.solution_detail_level = os.getenv("SOLUTION_DETAIL_LEVEL", "detailed")  # basic, detailed, expert
        self.include_code_examples = os.getenv("INCLUDE_CODE_EXAMPLES", "true").lower() == "true"
        
        # Cache configuration
        self.cache_crash_data = os.getenv("CACHE_CRASH_DATA", "true").lower() == "true"
        self.cache_duration_minutes = int(os.getenv("CACHE_DURATION_MINUTES", "30"))
        
    def is_firebase_configured(self) -> bool:
        """Check if Firebase is properly configured."""
        return bool(
            self.firebase_project_id and 
            (self.firebase_credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        )
    
    def is_openai_configured(self) -> bool:
        """Check if OpenAI is properly configured."""
        return bool(self.openai_api_key and self.openai_api_key.startswith("sk-"))
    
    def get_openai_config(self) -> dict:
        """Get OpenAI configuration."""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "max_tokens": self.openai_max_tokens,
            "temperature": self.openai_temperature
        }
    
    def validate_configuration(self) -> dict:
        """Validate configuration and return issues."""
        issues = {}
        
        if not self.is_firebase_configured():
            issues["firebase"] = "Firebase not configured. Set FIREBASE_PROJECT_ID and FIREBASE_CREDENTIALS_PATH"
        
        if self.enable_ai_solutions and not self.is_openai_configured():
            issues["openai"] = "OpenAI not configured but AI solutions are enabled. Set OPENAI_API_KEY"
        
        if self.solution_detail_level not in ["basic", "detailed", "expert"]:
            issues["solution_level"] = "Invalid solution detail level. Use: basic, detailed, or expert"
        
        return issues