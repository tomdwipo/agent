#!/bin/bash

# Chrome MCP Server Setup Script
# Automates the installation and configuration of the Chrome MCP server

set -e

echo "🌐 Chrome MCP Server Setup"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check for required tools
print_step "Checking prerequisites..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
print_success "Python $python_version found ✓"

# Check for uv
if ! command -v uv &> /dev/null; then
    print_warning "uv package manager not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    
    if command -v uv &> /dev/null; then
        print_success "uv installed successfully ✓"
    else
        print_error "Failed to install uv"
        exit 1
    fi
else
    print_success "uv package manager found ✓"
fi

# Check for Chrome browser
print_step "Checking for Chrome browser..."

chrome_found=false

# Check common Chrome installation paths
if command -v google-chrome &> /dev/null; then
    chrome_version=$(google-chrome --version 2>/dev/null || echo "Unknown version")
    print_success "Chrome found: $chrome_version ✓"
    chrome_found=true
elif command -v chromium-browser &> /dev/null; then
    chrome_version=$(chromium-browser --version 2>/dev/null || echo "Unknown version")
    print_success "Chromium found: $chrome_version ✓"
    chrome_found=true
elif [[ "$OSTYPE" == "darwin"* ]] && [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    chrome_version=$("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version 2>/dev/null || echo "Unknown version")
    print_success "Chrome found on macOS: $chrome_version ✓"
    chrome_found=true
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows paths
    if [ -f "/c/Program Files/Google/Chrome/Application/chrome.exe" ] || [ -f "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" ]; then
        print_success "Chrome found on Windows ✓"
        chrome_found=true
    fi
fi

if [ "$chrome_found" = false ]; then
    print_warning "Chrome browser not found"
    print_warning "Please install Google Chrome from https://www.google.com/chrome/"
    read -p "Continue without Chrome? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "Chrome browser detected ✓"
fi

# Install Python dependencies
print_step "Installing Python dependencies..."
uv sync

if [ $? -eq 0 ]; then
    print_success "Dependencies installed ✓"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Test Chrome automation
print_step "Testing Chrome automation..."

# Test basic Chrome automation
if uv run python -c "
import undetected_chromedriver as uc
import sys
try:
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    driver.get('https://www.google.com')
    title = driver.title
    driver.quit()
    print(f'Chrome automation test successful: {title}')
except Exception as e:
    print(f'Chrome automation test failed: {e}')
    sys.exit(1)
" 2>/dev/null; then
    print_success "Chrome automation test passed ✓"
else
    print_warning "Chrome automation test failed"
    print_warning "This might be due to missing dependencies or Chrome version mismatch"
fi

# Test MCP server import
print_step "Testing Chrome MCP server modules..."

if uv run python -c "from src.chrome import ChromeBrowser; print('Import successful')" 2>/dev/null; then
    print_success "Chrome MCP server modules loaded successfully ✓"
else
    print_error "Failed to load Chrome MCP server modules"
    exit 1
fi

# Create example environment file
if [ ! -f ".env" ]; then
    print_step "Creating example .env file..."
    cat > .env << EOF
# Chrome MCP Server Configuration

# Chrome Browser Settings
CHROME_HEADLESS=false
CHROME_WINDOW_SIZE=1920,1080
CHROME_DEBUG_PORT=9222
CHROME_USER_DATA_DIR=

# Download Settings
DOWNLOAD_DIRECTORY=~/Downloads
DOWNLOAD_TIMEOUT=30

# Automation Settings
DEFAULT_TIMEOUT=10.0
ELEMENT_HIGHLIGHT_COLOR=red
SCREENSHOT_SCALE=1.0

# Performance Settings
DISABLE_IMAGES=false
DISABLE_CSS=false
DISABLE_JAVASCRIPT=false

# Security Settings
INCOGNITO_MODE=false
DISABLE_EXTENSIONS=false
USER_AGENT_OVERRIDE=
EOF
    print_success "Created .env configuration file ✓"
fi

# Test different Chrome modes
print_step "Testing Chrome startup modes..."

echo "Testing headless mode..."
if timeout 10 uv run python -c "
from src.chrome import ChromeBrowser
browser = ChromeBrowser(headless=True)
browser.navigate('https://example.com')
info = browser.get_page_info()
print(f'Headless test: {info.get(\"title\", \"Unknown\")}')
browser.close()
" 2>/dev/null; then
    print_success "Headless mode test passed ✓"
else
    print_warning "Headless mode test failed or timed out"
fi

# Check for common issues and provide solutions
print_step "Checking for common issues..."

# Check disk space
available_space=$(df . | tail -1 | awk '{print $4}')
if [ "$available_space" -lt 1000000 ]; then  # Less than 1GB
    print_warning "Low disk space detected. Chrome may have issues running."
fi

# Check memory
if command -v free &> /dev/null; then
    available_memory=$(free -m | grep '^Mem:' | awk '{print $7}')
    if [ "$available_memory" -lt 512 ]; then  # Less than 512MB
        print_warning "Low available memory. Consider running in headless mode."
    fi
fi

# Final instructions
echo
echo "🎉 Chrome MCP Server Setup Complete!"
echo "===================================="
echo
echo "Next steps:"
echo "1. Test the server:"
echo "   ${BLUE}uv run main.py${NC}                    # GUI mode"
echo "   ${BLUE}uv run main.py --headless${NC}         # Headless mode"
echo
echo "2. Common usage patterns:"
echo "   ${BLUE}uv run main.py --incognito${NC}        # Private browsing"
echo "   ${BLUE}uv run main.py --window-size 1280,720${NC}  # Custom size"
echo
echo "3. For MCP client integration, add this to your configuration:"
echo "${YELLOW}"
cat << 'EOF'
{
  "mcpServers": {
    "chrome-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c", 
        "cd /path/to/agent/mcp/chrome && uv run main.py --headless"
      ]
    }
  }
}
EOF
echo "${NC}"
echo
echo "📖 For detailed usage instructions, see README.md"
echo "🐛 For troubleshooting, check the Common Issues section in README.md"

# Performance recommendations
echo
echo "💡 Performance Tips:"
echo "• Use --headless for better performance"
echo "• Use --disable-extensions to reduce memory usage"
echo "• Set smaller --window-size for faster rendering"
echo "• Use incognito mode for clean sessions"

print_success "Setup completed successfully! 🚀"

# Offer to run a quick demo
echo
read -p "Would you like to run a quick demo? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Running quick demo..."
    
    echo "Opening Google in headless mode and taking screenshot..."
    if uv run python -c "
from src.chrome import ChromeBrowser
import time

browser = ChromeBrowser(headless=True)
try:
    browser.navigate('https://www.google.com')
    time.sleep(2)
    info = browser.get_page_info()
    print(f'Successfully loaded: {info.get(\"title\", \"Unknown\")}')
    print(f'URL: {info.get(\"url\", \"Unknown\")}')
    browser.take_screenshot(save_path='demo_screenshot.png')
    print('Screenshot saved as demo_screenshot.png')
finally:
    browser.close()
    print('Demo completed successfully!')
" 2>/dev/null; then
        print_success "Demo completed successfully! Check demo_screenshot.png"
    else
        print_warning "Demo failed - check your setup"
    fi
fi