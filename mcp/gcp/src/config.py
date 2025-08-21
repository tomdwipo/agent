"""Configuration module for GCP MCP Server."""

import os
from typing import Optional
from dotenv import load_dotenv
from google.auth import default


class Config:
    """Configuration management for GCP MCP Server."""
    
    def __init__(self):
        load_dotenv()
        self.default_project_id = os.getenv("GCP_PROJECT_ID")
        self.default_zone = os.getenv("GCP_DEFAULT_ZONE", "us-central1-a")
        self._credentials = None
        self._project_id = None
        
    @property
    def credentials(self):
        if self._credentials is None:
            self._credentials, self._project_id = default()
        return self._credentials
    
    @property 
    def project_id(self):
        if self._project_id is None:
            _, self._project_id = default()
        return self._project_id or self.default_project_id