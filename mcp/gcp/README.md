# GCP MCP Server

A Model Context Protocol (MCP) server for Google Cloud Platform integration. This server provides AI assistants with comprehensive access to GCP resources including Compute Engine, Cloud Storage, IAM, and project management.

## Features

- 🖥️ **Compute Engine Management** - Create, start, stop, delete, and list VM instances
- 📦 **Cloud Storage Operations** - Manage buckets and objects with upload/download capabilities
- 🔐 **IAM Management** - Handle service accounts and IAM policies
- 📋 **Project Management** - List and manage GCP projects
- 🔧 **Flexible Configuration** - Environment-based configuration with credential management

## Prerequisites

- **Python** >= 3.10
- **Google Cloud SDK** (gcloud) installed and configured
- **GCP Service Account** with appropriate permissions
- **uv** package manager (recommended)

## Installation

1. **Navigate to the GCP MCP directory**
   ```bash
   cd mcp/gcp
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

## Configuration

1. **Set up GCP credentials**
   
   Option A: Use service account key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```
   
   Option B: Use gcloud CLI:
   ```bash
   gcloud auth application-default login
   ```

2. **Create environment file** (optional)
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   GCP_PROJECT_ID=your-default-project-id
   GCP_DEFAULT_ZONE=us-central1-a
   GCP_DEFAULT_REGION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   ```

## Usage

### As MCP Server (Recommended)

Run the server in stdio mode for MCP client integration:

```bash
uv run main.py
```

### With Custom Configuration

```bash
uv run main.py --credentials-path /path/to/credentials.json --project-id my-project
```

## Available Tools

### Compute Engine Tools

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-instances` | List VM instances | `project_id`, optional: `zone` |
| `create-instance` | Create VM instance | `project_id`, `zone`, `instance_name` |
| `start-instance` | Start VM instance | `project_id`, `zone`, `instance_name` |
| `stop-instance` | Stop VM instance | `project_id`, `zone`, `instance_name` |
| `delete-instance` | Delete VM instance | `project_id`, `zone`, `instance_name` |

### Cloud Storage Tools

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-buckets` | List storage buckets | `project_id` |
| `create-bucket` | Create storage bucket | `project_id`, `bucket_name` |
| `list-objects` | List objects in bucket | `bucket_name` |
| `upload-object` | Upload file to bucket | `bucket_name`, `object_name`, `file_path` |
| `download-object` | Download file from bucket | `bucket_name`, `object_name`, `destination_path` |

### IAM Tools

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-service-accounts` | List service accounts | `project_id` |
| `create-service-account` | Create service account | `project_id`, `account_id`, `display_name` |
| `get-iam-policy` | Get project IAM policy | `project_id` |

### Project Tools

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-projects` | List accessible projects | None |
| `get-project` | Get project details | `project_id` |

## MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "gcp-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/agent/mcp/gcp && uv run main.py"
      ],
      "alwaysAllow": [
        "list-instances",
        "list-buckets", 
        "list-projects",
        "get-project"
      ]
    }
  }
}
```

## Required GCP Permissions

Your service account needs the following IAM roles:

- **Compute Engine**: `roles/compute.instanceAdmin.v1`
- **Cloud Storage**: `roles/storage.admin`
- **IAM**: `roles/iam.serviceAccountAdmin`
- **Projects**: `roles/browser` or `roles/viewer`

## Examples

### List Compute Instances
```
List all instances in my-project
```

### Create a VM Instance
```
Create a new e2-micro instance named "test-vm" in us-central1-a zone for project my-project
```

### Upload File to Storage
```
Upload the file /local/path/file.txt to my-bucket as uploaded-file.txt
```

## Development

### Project Structure

```
src/
├── config.py           # Configuration management
├── gcp/               # GCP service modules
│   ├── compute.py     # Compute Engine operations
│   ├── storage.py     # Cloud Storage operations
│   ├── iam.py         # IAM operations
│   └── projects.py    # Project management
└── main.py            # MCP server entry point
```

### Running Tests

```bash
# Install test dependencies
uv sync --dev

# Run tests
uv run pytest
```

## Troubleshooting

### Authentication Issues
- Verify `GOOGLE_APPLICATION_CREDENTIALS` points to valid service account key
- Ensure service account has required permissions
- Try `gcloud auth application-default login`

### Permission Denied
- Check IAM roles assigned to your service account
- Verify project ID is correct
- Ensure APIs are enabled (Compute Engine API, Cloud Storage API, etc.)

### Module Import Issues
- Ensure you're running from the correct directory
- Check that all dependencies are installed with `uv sync`

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request