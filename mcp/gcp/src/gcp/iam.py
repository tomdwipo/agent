"""Google Cloud IAM tools for GCP MCP Server."""

import asyncio
from google.cloud import iam_admin_v1, resourcemanager_v1
from ..config import Config


class IAMTools:
    """Tools for Google Cloud IAM operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._iam_client = None
        self._rm_client = None
    
    @property
    def iam_client(self):
        if self._iam_client is None:
            self._iam_client = iam_admin_v1.IAMClient(credentials=self.config.credentials)
        return self._iam_client
    
    @property
    def rm_client(self):
        if self._rm_client is None:
            self._rm_client = resourcemanager_v1.ProjectsClient(credentials=self.config.credentials)
        return self._rm_client
    
    async def list_service_accounts(self, project_id: str) -> str:
        """List service accounts in a project."""
        try:
            request = iam_admin_v1.ListServiceAccountsRequest(name=f"projects/{project_id}")
            response = await asyncio.to_thread(self.iam_client.list_service_accounts, request=request)
            
            result = f"Service accounts in {project_id}:\n"
            for sa in response.accounts:
                result += f"• {sa.display_name or sa.email}\n  {sa.email}\n"
            return result or "No service accounts found"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def create_service_account(self, project_id: str, account_id: str, display_name: str, **kwargs) -> str:
        """Create a service account."""
        try:
            service_account = iam_admin_v1.ServiceAccount(
                display_name=display_name,
                description=kwargs.get("description", f"Service account {account_id}")
            )
            
            request = iam_admin_v1.CreateServiceAccountRequest(
                name=f"projects/{project_id}",
                account_id=account_id,
                service_account=service_account
            )
            
            created_sa = await asyncio.to_thread(self.iam_client.create_service_account, request=request)
            return f"Created service account: {created_sa.email}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def get_iam_policy(self, project_id: str) -> str:
        """Get IAM policy for a project."""
        try:
            request = resourcemanager_v1.GetIamPolicyRequest(resource=f"projects/{project_id}")
            policy = await asyncio.to_thread(self.rm_client.get_iam_policy, request=request)
            
            result = f"IAM policy for {project_id}:\n"
            for binding in policy.bindings:
                result += f"• {binding.role}: {len(binding.members)} members\n"
            return result or "No policy bindings found"
        except Exception as e:
            return f"Error: {str(e)}"