"""Google Compute Engine tools for GCP MCP Server."""

import asyncio
from google.cloud import compute_v1
from .config import Config


class ComputeTools:
    """Tools for Google Compute Engine operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = compute_v1.InstancesClient(credentials=self.config.credentials)
        return self._client
    
    async def list_instances(self, project_id: str, zone: str = None) -> str:
        """List Compute Engine instances."""
        try:
            zone = zone or self.config.default_zone
            request = compute_v1.ListInstancesRequest(project=project_id, zone=zone)
            instances = await asyncio.to_thread(self.client.list, request=request)
            
            result = f"Instances in {project_id}/{zone}:\n"
            for instance in instances:
                result += f"• {instance.name} ({instance.status})\n"
            return result or "No instances found"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def create_instance(self, project_id: str, zone: str, instance_name: str, **kwargs) -> str:
        """Create a Compute Engine instance."""
        try:
            machine_type = kwargs.get("machine_type", "e2-micro")
            
            instance = compute_v1.Instance()
            instance.name = instance_name
            instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"
            
            # Basic configuration
            boot_disk = compute_v1.AttachedDisk()
            initialize_params = compute_v1.AttachedDiskInitializeParams()
            initialize_params.source_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
            boot_disk.initialize_params = initialize_params
            boot_disk.auto_delete = True
            boot_disk.boot = True
            instance.disks = [boot_disk]
            
            # Network
            network_interface = compute_v1.NetworkInterface()
            network_interface.network = f"projects/{project_id}/global/networks/default"
            instance.network_interfaces = [network_interface]
            
            request = compute_v1.InsertInstanceRequest(
                project=project_id, zone=zone, instance_resource=instance
            )
            operation = await asyncio.to_thread(self.client.insert, request=request)
            return f"Instance {instance_name} creation initiated: {operation.name}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def stop_instance(self, project_id: str, zone: str, instance_name: str) -> str:
        """Stop an instance."""
        try:
            request = compute_v1.StopInstanceRequest(
                project=project_id, zone=zone, instance=instance_name
            )
            operation = await asyncio.to_thread(self.client.stop, request=request)
            return f"Instance {instance_name} stop initiated: {operation.name}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def start_instance(self, project_id: str, zone: str, instance_name: str) -> str:
        """Start an instance."""
        try:
            request = compute_v1.StartInstanceRequest(
                project=project_id, zone=zone, instance=instance_name
            )
            operation = await asyncio.to_thread(self.client.start, request=request)
            return f"Instance {instance_name} start initiated: {operation.name}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def delete_instance(self, project_id: str, zone: str, instance_name: str) -> str:
        """Delete an instance."""
        try:
            request = compute_v1.DeleteInstanceRequest(
                project=project_id, zone=zone, instance=instance_name
            )
            operation = await asyncio.to_thread(self.client.delete, request=request)
            return f"Instance {instance_name} deletion initiated: {operation.name}"
        except Exception as e:
            return f"Error: {str(e)}"