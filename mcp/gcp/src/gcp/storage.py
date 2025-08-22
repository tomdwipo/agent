"""Google Cloud Storage tools for GCP MCP Server."""

import asyncio
import os
from google.cloud import storage
from ..config import Config


class StorageTools:
    """Tools for Google Cloud Storage operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = storage.Client(
                credentials=self.config.credentials,
                project=self.config.project_id
            )
        return self._client
    
    async def list_buckets(self, project_id: str) -> str:
        """List Cloud Storage buckets."""
        try:
            buckets = await asyncio.to_thread(list, self.client.list_buckets())
            result = f"Buckets in {project_id}:\n"
            for bucket in buckets:
                result += f"• {bucket.name} ({bucket.location})\n"
            return result or "No buckets found"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def create_bucket(self, project_id: str, bucket_name: str, location: str = "US") -> str:
        """Create a Cloud Storage bucket."""
        try:
            await asyncio.to_thread(
                self.client.create_bucket, bucket_name, location=location
            )
            return f"Bucket {bucket_name} created in {location}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def list_objects(self, bucket_name: str, prefix: str = None) -> str:
        """List objects in a bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            blobs = await asyncio.to_thread(list, bucket.list_blobs(prefix=prefix))
            
            result = f"Objects in {bucket_name}:\n"
            for blob in blobs:
                result += f"• {blob.name} ({blob.size} bytes)\n"
            return result or "No objects found"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def upload_object(self, bucket_name: str, object_name: str, file_path: str, **kwargs) -> str:
        """Upload a file to Cloud Storage."""
        try:
            if not os.path.exists(file_path):
                return f"File {file_path} not found"
            
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(object_name)
            
            await asyncio.to_thread(blob.upload_from_filename, file_path)
            return f"Uploaded {file_path} to {bucket_name}/{object_name}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def download_object(self, bucket_name: str, object_name: str, destination_path: str) -> str:
        """Download a file from Cloud Storage."""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(object_name)
            
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            await asyncio.to_thread(blob.download_to_filename, destination_path)
            return f"Downloaded {bucket_name}/{object_name} to {destination_path}"
        except Exception as e:
            return f"Error: {str(e)}"