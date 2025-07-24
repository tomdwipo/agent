# Figma Developer MCP

A Model Context Protocol (MCP) server that provides AI assistants with comprehensive access to Figma design files. This server enables seamless integration between AI tools and Figma's design data, allowing for automated design analysis, content extraction, and workflow automation.

## Features

- 🎨 **Comprehensive Design Data Extraction** - Extract layout, content, visuals, and component information from Figma files
- 🔧 **Flexible Extractor System** - Modular architecture for different types of design data extraction
- 📊 **Multiple Output Formats** - Support for both JSON and YAML output formats
- 🖼️ **Image Processing** - Download and process images from Figma designs
- 🚀 **Dual Operation Modes** - Run as MCP server (stdio) or standalone HTTP server
- 🔌 **MCP Protocol Compliance** - Full compatibility with Model Context Protocol standards

## Prerequisites

- **Node.js** >= 18.0.0
- **pnpm** (recommended package manager)
- **Figma API Access Token** - Get yours from [Figma Developer Settings](https://www.figma.com/developers/api#access-tokens)

## Installation

### Option 1: Install from npm (Recommended)

```bash
npm install -g figma-mcp
```

### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/tomdwipo/agent.git
cd agent/figma-mcp

# Install dependencies
pnpm install

# Build the project
pnpm build
```

## Configuration

1. **Create Environment File**
   
   Copy the example environment file and configure your settings:
   ```bash
   cp .env.example .env
   ```

2. **Configure Environment Variables**
   
   Edit the `.env` file with your Figma credentials:
   ```env
   # Required: Your Figma API access token
   FIGMA_API_KEY=your_figma_api_key_here
   
   # Optional: Default file key for testing
   FIGMA_FILE_KEY=your_figma_file_key_here
   
   # Optional: Default node ID for testing
   FIGMA_NODE_ID=your_figma_node_id_here
   
   # Optional: Server port (default: 3333)
   PORT=3333
   
   # Optional: Output format - "yaml" (default) or "json"
   OUTPUT_FORMAT=yaml
   ```

3. **Get Your Figma API Token**
   - Go to [Figma Account Settings](https://www.figma.com/developers/api#access-tokens)
   - Generate a new personal access token
   - Copy the token to your `.env` file

## Usage

### As MCP Server (Recommended)

Run the server in stdio mode for MCP client integration:

```bash
# Using the global installation
figma-developer-mcp --stdio

# Or using pnpm (from source)
pnpm start:cli
```

### As HTTP Server

Run as a standalone HTTP server:

```bash
# Using the global installation
figma-developer-mcp

# Or using pnpm (from source)
pnpm start:http
```

The server will start on `http://localhost:3333` (or your configured port).

### Development Mode

For development with hot reloading:

```bash
pnpm dev
```

## MCP Tools

The server provides the following MCP tools:

### `get_figma_data`

Extracts comprehensive design data from Figma files.

**Parameters:**
- `fileKey` (required): The Figma file key from the URL (e.g., from `figma.com/file/{fileKey}/...`)
- `nodeId` (optional): Specific node ID to extract (from URL parameter `node-id={nodeId}`)
- `depth` (optional): Maximum traversal depth for nested elements

**Example:**
```json
{
  "fileKey": "abc123def456",
  "nodeId": "1:23",
  "depth": 3
}
```

### `download_figma_images`

Downloads and processes images from Figma designs.

**Parameters:**
- `fileKey` (required): The Figma file key
- `nodeIds` (optional): Array of specific node IDs to download images for
- `format` (optional): Image format (png, jpg, svg, pdf)
- `scale` (optional): Image scale factor

## Integration Examples

### With MCP-Compatible AI Tools

1. **Configure your MCP client** to connect to the Figma MCP server
2. **Use the tools** in your AI conversations:
   ```
   Please analyze the design in this Figma file: https://www.figma.com/file/abc123def456/My-Design
   ```

### Extracting Specific Components

```
Get the button components from node 1:23 in file abc123def456
```

### Design System Analysis

```
Extract all text styles and color variables from the design system file
```

## Output Formats

### YAML (Default)
Compact, human-readable format ideal for AI processing:
```yaml
metadata:
  name: "My Design File"
  lastModified: "2024-01-15T10:30:00Z"
nodes:
  - id: "1:23"
    name: "Button Component"
    type: "COMPONENT"
```

### JSON
Standard JSON format for programmatic processing:
```json
{
  "metadata": {
    "name": "My Design File",
    "lastModified": "2024-01-15T10:30:00Z"
  },
  "nodes": [
    {
      "id": "1:23",
      "name": "Button Component",
      "type": "COMPONENT"
    }
  ]
}
```

## Development

### Project Structure

```
src/
├── cli.ts              # CLI entry point and server startup
├── config.ts           # Configuration management
├── index.ts            # Main exports
├── server.ts           # HTTP server implementation
├── extractors/         # Design data extraction logic
├── mcp/               # MCP protocol implementation
├── services/          # External service integrations
├── transformers/      # Data transformation utilities
└── utils/             # Common utilities
```

### Available Scripts

```bash
# Development
pnpm dev                # Start development server with hot reload
pnpm dev:cli           # Start CLI development mode

# Building
pnpm build             # Build for production
pnpm type-check        # Run TypeScript type checking

# Testing
pnpm test              # Run test suite
pnpm lint              # Run ESLint
pnpm format            # Format code with Prettier

# Debugging
pnpm inspect           # Run MCP inspector for debugging
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `pnpm test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Troubleshooting

### Common Issues

**"Invalid API token" Error**
- Verify your `FIGMA_API_KEY` in the `.env` file
- Ensure the token has the necessary permissions
- Check that the token hasn't expired

**"File not found" Error**
- Verify the `fileKey` parameter is correct
- Ensure you have access to the Figma file
- Check that the file URL is properly formatted

**Connection Issues**
- Verify your internet connection
- Check if Figma's API is accessible from your network
- Ensure no firewall is blocking the requests

**MCP Client Connection Issues**
- Verify the server is running in stdio mode (`--stdio` flag)
- Check that your MCP client is properly configured
- Ensure the server path is correct in your client configuration

### Debug Mode

Enable detailed logging by setting the environment variable:
```bash
NODE_ENV=development figma-developer-mcp
```

### Getting Help

- Check the [Issues](https://github.com/tomdwipo/agent/issues) page for known problems
- Review the [Figma API Documentation](https://www.figma.com/developers/api)
- Consult the [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the [Model Context Protocol SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- Powered by the [Figma REST API](https://www.figma.com/developers/api)
- Inspired by the need for better AI-design tool integration

---

**Homepage:** [https://www.framelink.ai](https://www.framelink.ai)  
**Repository:** [https://github.com/tomdwipo/agent](https://github.com/tomdwipo/agent)
