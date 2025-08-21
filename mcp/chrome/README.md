# Chrome MCP Server

A Model Context Protocol (MCP) server for Chrome browser automation and web testing. This server provides comprehensive web browser control capabilities, enabling automated web testing, scraping, and browser interaction through Selenium WebDriver with enhanced stealth capabilities.

## Features

- 🌐 **Complete Browser Control** - Navigate, click, type, and interact with web pages
- 🔍 **Advanced Element Detection** - Comprehensive element selection using multiple selectors
- 📸 **Visual Screenshots** - Capture and annotate screenshots with interactive elements
- 🎯 **Precise Element Targeting** - XPath, CSS selectors, and attribute-based selection
- 🕵️ **Stealth Mode** - Undetected browser automation to bypass anti-bot detection
- 📑 **Tab & Window Management** - Multi-tab and window control capabilities
- 🍪 **Cookie Management** - Complete cookie handling and session management
- 📥 **Download Handling** - File download management and control
- 🚨 **Alert Handling** - Automatic handling of browser alerts and dialogs
- 📝 **Form Automation** - Advanced form filling and submission

## Prerequisites

- **Python** >= 3.10
- **Chrome Browser** (latest version recommended)
- **ChromeDriver** (automatically managed)
- **uv** package manager (recommended)

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: using pip
pip install uv
```

### 2. Set up the project

```bash
# Navigate to the Chrome MCP directory
cd mcp/chrome

# Install dependencies
uv sync

# Activate virtual environment (optional)
source .venv/bin/activate
```

### 3. Verify Chrome installation

```bash
# Check Chrome version
google-chrome --version
# or
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

## Usage

### Running the Server

#### Basic Usage (GUI Mode):
```bash
uv run main.py
```

#### Headless Mode:
```bash
uv run main.py --headless
```

#### With Custom Profile:
```bash
uv run main.py --profile "Profile 1" --user-data-dir "/path/to/chrome/data"
```

#### Incognito Mode:
```bash
uv run main.py --incognito --disable-extensions
```

#### Custom Window Size:
```bash
uv run main.py --window-size 1280,720
```

## MCP Server Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "chrome-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/agent/mcp/chrome && source .venv/bin/activate && uv run main.py --headless"
      ],
      "alwaysAllow": [
        "Navigate-Tool",
        "State-Tool",
        "Element-Click-Tool",
        "Element-Type-Tool"
      ]
    }
  }
}
```

**Note**: Update the path according to your installation location.

## Available Tools

### Navigation & Basic Control

| Tool | Description | Parameters |
|------|-------------|------------|
| **Navigate-Tool** | Navigate to URL | `url: str` |
| **State-Tool** | Get page state with optional screenshot | `use_vision: bool = false` |
| **Back-Tool** | Navigate back in history | None |
| **Forward-Tool** | Navigate forward in history | None |
| **Refresh-Tool** | Refresh current page | None |

### Element Interaction

| Tool | Description | Parameters |
|------|-------------|------------|
| **Click-Tool** | Click on coordinates | `x: int, y: int` |
| **Element-Click-Tool** | Click element by selector | `selector: str, value: str, timeout: float = 10.0` |
| **Type-Tool** | Type text (coordinates optional) | `text: str, x: int = None, y: int = None, clear: bool = false` |
| **Element-Type-Tool** | Type in element by selector | `selector: str, value: str, text: str, clear: bool = true` |

#### Supported Selectors:
- `id` - Element ID
- `name` - Element name attribute
- `class` - CSS class name
- `tag` - HTML tag name
- `xpath` - XPath expression
- `css` - CSS selector
- `link_text` - Exact link text
- `partial_link_text` - Partial link text

### Page Interaction

| Tool | Description | Parameters |
|------|-------------|------------|
| **Scroll-Tool** | Scroll page | `direction: str, amount: int = 300` |
| **Wait-Tool** | Wait for duration | `duration: float` |
| **Element-Wait-Tool** | Wait for element | `selector: str, value: str, timeout: float = 10.0` |
| **Screenshot-Tool** | Take screenshot | `selector: str = None, value: str = None, save_path: str = None` |

#### Scroll Directions:
- `up`, `down`, `left`, `right` - Scroll by amount
- `top`, `bottom` - Scroll to page extremes

### Tab & Window Management

| Tool | Description | Parameters |
|------|-------------|------------|
| **Tab-Control-Tool** | Control browser tabs | `action: str, tab_index: int = None, url: str = None` |
| **Window-Control-Tool** | Control browser window | `action: str, width: int = None, height: int = None` |

#### Tab Actions:
- `new` - Open new tab (with optional URL)
- `close` - Close current tab
- `switch` - Switch to tab by index
- `list` - List all tabs

#### Window Actions:
- `maximize`, `minimize`, `fullscreen` - Window states
- `resize` - Resize to width×height
- `position` - Move to x,y coordinates

### Advanced Features

| Tool | Description | Parameters |
|------|-------------|------------|
| **Execute-Script-Tool** | Execute JavaScript | `script: str, *args` |
| **Get-Attribute-Tool** | Get element attribute | `selector: str, value: str, attribute: str` |
| **Get-Text-Tool** | Get element text | `selector: str, value: str` |
| **Cookie-Tool** | Manage cookies | `action: str, name: str = None, value: str = None` |
| **Alert-Tool** | Handle alerts | `action: str, text: str = None` |
| **Form-Tool** | Form interaction | `action: str, selector: str = None, form_data: dict = None` |
| **Download-Tool** | Handle downloads | `action: str, url: str = None, path: str = None` |

## Usage Examples

### Basic Web Navigation

```bash
# Navigate to a website
Navigate-Tool --url "https://example.com"

# Take screenshot to see page elements
State-Tool --use_vision true

# Click on specific coordinates
Click-Tool --x 300 --y 200
```

### Element-Based Interaction

```bash
# Click on element by ID
Element-Click-Tool --selector id --value "submit-button"

# Type in search box
Element-Type-Tool --selector name --value "q" --text "Python automation"

# Wait for element to load
Element-Wait-Tool --selector class --value "search-results" --timeout 15.0
```

### Advanced Web Automation

```bash
# Fill out a login form
Element-Type-Tool --selector id --value "username" --text "myuser"
Element-Type-Tool --selector id --value "password" --text "mypass"
Element-Click-Tool --selector xpath --value "//button[@type='submit']"

# Handle JavaScript alert
Alert-Tool --action get_text
Alert-Tool --action accept

# Execute custom JavaScript
Execute-Script-Tool --script "return document.title;"
```

### Tab Management Workflow

```bash
# Open multiple tabs
Tab-Control-Tool --action new --url "https://google.com"
Tab-Control-Tool --action new --url "https://github.com"

# List all tabs
Tab-Control-Tool --action list

# Switch between tabs
Tab-Control-Tool --action switch --tab_index 0
```

### Form Automation

```bash
# Fill entire form at once
Form-Tool --action fill --form_data '{"username": "testuser", "email": "test@example.com", "message": "Hello World"}'

# Submit form
Form-Tool --action submit --selector id --value "contact-form"
```

### Cookie Management

```bash
# Set authentication cookie
Cookie-Tool --action set --name "session_id" --value "abc123def456"

# Get all cookies
Cookie-Tool --action list

# Clear all cookies
Cookie-Tool --action clear
```

## Configuration Options

### Environment Variables

Create a `.env` file for configuration:

```env
# Chrome Configuration
CHROME_HEADLESS=false
CHROME_WINDOW_SIZE=1920,1080
CHROME_DEBUG_PORT=9222

# Download Settings
DOWNLOAD_DIRECTORY=~/Downloads
DOWNLOAD_TIMEOUT=30

# Automation Settings
DEFAULT_TIMEOUT=10.0
ELEMENT_HIGHLIGHT_COLOR=red
SCREENSHOT_SCALE=1.0

# Stealth Settings
DISABLE_IMAGES=false
DISABLE_CSS=false
USER_AGENT_OVERRIDE=false
```

### Advanced Chrome Options

The server automatically sets these Chrome options for optimal automation:

- **Stealth Mode**: Removes automation detection
- **No Sandbox**: For compatibility in containers
- **Disable Web Security**: For cross-origin requests
- **Custom User Agent**: Appears as regular browser

## Troubleshooting

### Common Issues

1. **ChromeDriver Issues**:
   ```bash
   # Update ChromeDriver automatically
   pip install --upgrade undetected-chromedriver
   ```

2. **Element Not Found**:
   - Use `State-Tool` with vision to see available elements
   - Try different selectors (id, name, xpath, css)
   - Increase timeout values
   - Wait for page to load completely

3. **Headless Mode Problems**:
   ```bash
   # Test in GUI mode first
   uv run main.py
   
   # Then switch to headless
   uv run main.py --headless
   ```

4. **Permission Denied**:
   - Check Chrome browser permissions
   - Ensure user data directory is writable
   - Run without custom profile first

### Anti-Bot Detection

The server uses `undetected-chromedriver` to bypass common detection:

- Removes `webdriver` property
- Uses realistic browser fingerprints
- Mimics human-like behavior
- Handles challenge pages automatically

### Performance Optimization

```bash
# Disable images for faster loading
uv run main.py --headless --disable-extensions

# Use smaller window size
uv run main.py --window-size 1280,720

# Custom user data directory for isolation
uv run main.py --user-data-dir "/tmp/chrome-automation"
```

## Development

### Project Structure

```
mcp/chrome/
├── README.md
├── pyproject.toml
├── main.py                 # MCP server entry point
├── src/
│   ├── chrome/             # Chrome browser management
│   │   ├── __init__.py     # Main ChromeBrowser class
│   │   └── views.py        # State representation
│   └── page/               # Web page parsing
│       └── __init__.py     # Page element parsing
└── .venv/                  # Virtual environment
```

### Dependencies

- **mcp**: Model Context Protocol framework
- **selenium**: WebDriver automation framework
- **undetected-chromedriver**: Stealth Chrome automation
- **webdriver-manager**: Automatic ChromeDriver management
- **pillow**: Image processing for screenshots
- **beautifulsoup4**: HTML parsing utilities

### Testing Your Changes

```bash
# Basic functionality test
uv run python -c "
from src.chrome import ChromeBrowser
browser = ChromeBrowser(headless=True)
browser.navigate('https://example.com')
print('Navigation successful!')
print(browser.get_page_info())
browser.close()
"

# Test MCP tools
uv run main.py --headless
```

## Integration with SDLC Workflow

This Chrome MCP server perfectly complements your existing SDLC automation platform:

1. **Meeting Transcription** → Requirements for web features
2. **PRD/TRD Generation** → Web application specifications
3. **Figma MCP** → Design implementation verification
4. **Chrome MCP** → **🆕 Web application testing and automation**
5. **Android/iOS MCP** → Cross-platform testing coordination
6. **Firebase Crashlytics MCP** → Web error tracking
7. **Docker/GCP MCP** → Web application deployment

## Advanced Use Cases

### E2E Testing Automation

```bash
# Complete user journey testing
Navigate-Tool --url "https://myapp.com/login"
Element-Type-Tool --selector id --value "email" --text "test@example.com"
Element-Type-Tool --selector id --value "password" --text "password123"
Element-Click-Tool --selector id --value "login-button"
Element-Wait-Tool --selector class --value "dashboard" --timeout 10.0
Screenshot-Tool --save_path "test_results/login_success.png"
```

### Data Extraction

```bash
# Extract data from web pages
Navigate-Tool --url "https://example.com/data"
Execute-Script-Tool --script "return Array.from(document.querySelectorAll('.data-item')).map(el => el.textContent);"
```

### Performance Monitoring

```bash
# Measure page load performance
Execute-Script-Tool --script "return performance.timing.loadEventEnd - performance.timing.navigationStart;"
```

## Security Considerations

- **Headless Mode**: Recommended for production environments
- **User Data Isolation**: Use temporary profiles for sensitive operations
- **Cookie Management**: Clear cookies between sessions
- **Download Safety**: Monitor download directory for security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Add appropriate documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Selenium WebDriver](https://selenium.dev/) for browser automation
- Enhanced with [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) for stealth capabilities
- Inspired by the need for comprehensive web automation in SDLC workflows

---

**Repository:** [https://github.com/tomdwipo/agent](https://github.com/tomdwipo/agent)