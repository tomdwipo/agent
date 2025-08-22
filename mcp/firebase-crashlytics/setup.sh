#!/bin/bash

# Firebase Crashlytics MCP Server Setup Script

set -e

echo "🔥 Setting up Firebase Crashlytics MCP Server..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the mcp/firebase-crashlytics directory"
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

# Check for Firebase CLI (optional)
if ! command -v firebase &> /dev/null; then
    echo "⚠️  Warning: Firebase CLI is not installed."
    echo "   Install from: https://firebase.google.com/docs/cli"
    echo "   This is optional but recommended for easier setup."
else
    echo "✅ Firebase CLI found"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Firebase and OpenAI settings."
else
    echo "✅ .env file already exists"
fi

# Test the installation
echo "🧪 Testing installation..."
if uv run python -c "import firebase_admin; print('✅ Firebase Admin SDK imported successfully')"; then
    echo "✅ Firebase SDK test passed!"
else
    echo "❌ Firebase SDK test failed. Please check the error above."
    exit 1
fi

if uv run python -c "import openai; print('✅ OpenAI library imported successfully')"; then
    echo "✅ OpenAI library test passed!"
else
    echo "❌ OpenAI library test failed. Please check the error above."
    exit 1
fi

echo ""
echo "🎉 Firebase Crashlytics MCP Server setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure Firebase:"
echo "   - Set up Firebase project with Crashlytics enabled"
echo "   - Create service account and download credentials JSON"
echo "   - Update FIREBASE_PROJECT_ID and FIREBASE_CREDENTIALS_PATH in .env"
echo ""
echo "2. Configure OpenAI:"
echo "   - Get OpenAI API key from https://platform.openai.com/"
echo "   - Update OPENAI_API_KEY in .env"
echo ""
echo "3. Test the server:"
echo "   - uv run main.py --help"
echo "   - uv run main.py --firebase-project-id your-project"
echo ""
echo "4. Configure your MCP client to use this server"
echo ""
echo "📚 See README.md for detailed configuration and usage instructions"