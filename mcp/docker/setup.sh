#!/bin/bash

# Docker MCP Server Setup Script

set -e

echo "🐳 Setting up Docker MCP Server..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the mcp/docker directory"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

echo "✅ Dependencies installed successfully!"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed."
    echo "   Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
else
    echo "✅ Docker found"
fi

# Check if Docker daemon is running
if ! docker ps &> /dev/null; then
    echo "❌ Error: Docker daemon is not running."
    echo "   Please start Docker and try again."
    exit 1
else
    echo "✅ Docker daemon is running"
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Warning: Docker Compose is not installed."
    echo "   Compose operations will not be available."
    echo "   Install from: https://docs.docker.com/compose/install/"
else
    echo "✅ Docker Compose found"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Docker settings."
else
    echo "✅ .env file already exists"
fi

# Test the installation
echo "🧪 Testing installation..."
if uv run python -c "import docker; print('✅ Docker library imported successfully')"; then
    echo "✅ Installation test passed!"
else
    echo "❌ Installation test failed. Please check the error above."
    exit 1
fi

# Test Docker connectivity
echo "🔗 Testing Docker connectivity..."
if uv run python -c "import docker; client = docker.from_env(); client.ping(); print('✅ Docker connection successful')"; then
    echo "✅ Docker connectivity test passed!"
else
    echo "❌ Docker connectivity test failed. Please check Docker daemon."
    exit 1
fi

echo ""
echo "🎉 Docker MCP Server setup complete!"
echo ""
echo "Next steps:"
echo "1. Review .env file for any custom configuration"
echo "2. Test the server: uv run main.py --help"
echo "3. Run the server: uv run main.py"
echo "4. Try Docker operations:"
echo "   - List containers: docker ps"
echo "   - Pull test image: docker pull hello-world"
echo ""
echo "📚 See README.md for detailed usage instructions"