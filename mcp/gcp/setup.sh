#!/bin/bash

# GCP MCP Server Setup Script

set -e

echo "🚀 Setting up GCP MCP Server..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the mcp/gcp directory"
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

# Check for Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "⚠️  Warning: Google Cloud SDK (gcloud) is not installed."
    echo "   Please install it from: https://cloud.google.com/sdk/docs/install"
    echo "   Then run: gcloud auth application-default login"
else
    echo "✅ Google Cloud SDK found"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your GCP settings."
else
    echo "✅ .env file already exists"
fi

# Test the installation
echo "🧪 Testing installation..."
if uv run python -c "import google.cloud.compute_v1; print('✅ Google Cloud libraries imported successfully')"; then
    echo "✅ Installation test passed!"
else
    echo "❌ Installation test failed. Please check the error above."
    exit 1
fi

echo ""
echo "🎉 GCP MCP Server setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your GCP credentials:"
echo "   - Option A: gcloud auth application-default login"
echo "   - Option B: Set GOOGLE_APPLICATION_CREDENTIALS in .env"
echo "2. Edit .env file with your default project ID"
echo "3. Test the server: uv run main.py --help"
echo "4. Run the server: uv run main.py"
echo ""
echo "📚 See README.md for detailed usage instructions"