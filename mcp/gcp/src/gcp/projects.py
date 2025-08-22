"""Google Cloud Projects tools for GCP MCP Server."""

import asyncio
from google.cloud import resourcemanager_v1
from ..config import Config


class ProjectTools:
    """Tools for Google Cloud Project operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = resourcemanager_v1.ProjectsClient(credentials=self.config.credentials)
        return self._client
    
    async def list_projects(self) -> str:
        """List all accessible GCP projects."""
        try:
            request = resourcemanager_v1.ListProjectsRequest()
            projects = await asyncio.to_thread(self.client.list_projects, request=request)
            
            result = "Accessible GCP Projects:\n"
            for project in projects:
                display_name = project.display_name or project.project_id
                result += f"• {display_name} ({project.project_id}) - {project.state.name}\n"
            return result or "No projects found"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def get_project(self, project_id: str) -> str:
        """Get details of a specific project."""
        try:
            request = resourcemanager_v1.GetProjectRequest(name=f"projects/{project_id}")
            project = await asyncio.to_thread(self.client.get_project, request=request)
            
            result = f"Project: {project.display_name or project.project_id}\n"
            result += f"ID: {project.project_id}\n"
            result += f"Number: {project.name.split('/')[-1]}\n"
            result += f"State: {project.state.name}\n"
            
            if hasattr(project, 'labels') and project.labels:
                result += f"Labels: {dict(project.labels)}\n"
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"