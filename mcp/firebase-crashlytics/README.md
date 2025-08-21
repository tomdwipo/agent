# Firebase Crashlytics MCP Server

A Model Context Protocol (MCP) server for Firebase Crashlytics integration with AI-powered crash analysis and solution generation. This server provides comprehensive crash data retrieval, pattern analysis, and intelligent solution suggestions to streamline your mobile app debugging workflow.

## Features

- 🔥 **Firebase Crashlytics Integration** - Complete crash data retrieval and analysis
- 🤖 **AI-Powered Solutions** - OpenAI GPT-4 powered crash analysis and fix suggestions  
- 📊 **Crash Pattern Analysis** - Identify similarities, frequency patterns, and impact analysis
- 👥 **User Impact Analysis** - Understand how crashes affect your users
- 📈 **Trend Analysis** - Track crash trends over time with detailed statistics
- 📋 **Comprehensive Reporting** - Generate detailed crash reports in multiple formats
- 🛡️ **Preventive Measures** - AI-suggested proactive development practices
- ⚡ **Async Operations** - Non-blocking operations for better performance

## Prerequisites

- **Python** >= 3.10
- **Firebase Project** with Crashlytics enabled
- **Firebase Service Account** with Crashlytics access
- **OpenAI API Key** (for AI solution generation)
- **uv** package manager (recommended)

## Installation

1. **Navigate to the Firebase Crashlytics MCP directory**
   ```bash
   cd mcp/firebase-crashlytics
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

## Configuration

1. **Set up Firebase credentials**
   
   Option A: Service account key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```
   
   Option B: Use Firebase CLI:
   ```bash
   firebase login
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   # Firebase Configuration
   FIREBASE_PROJECT_ID=your-firebase-project-id
   FIREBASE_CREDENTIALS_PATH=/path/to/service-account-key.json
   FIREBASE_APP_ID=1:123456789:android:abcdef123456
   
   # OpenAI Configuration (for AI solutions)
   OPENAI_API_KEY=sk-your-openai-api-key
   OPENAI_MODEL=gpt-4
   OPENAI_MAX_TOKENS=2000
   OPENAI_TEMPERATURE=0.3
   
   # Feature Configuration
   ENABLE_AI_SOLUTIONS=true
   SOLUTION_DETAIL_LEVEL=detailed
   INCLUDE_CODE_EXAMPLES=true
   
   # Performance Configuration
   MAX_CRASHES_PER_REQUEST=50
   CACHE_CRASH_DATA=true
   CACHE_DURATION_MINUTES=30
   ```

## Usage

### As MCP Server (Recommended)

Run the server in stdio mode for MCP client integration:

```bash
uv run main.py
```

### With Custom Configuration

```bash
uv run main.py --firebase-project-id my-project --enable-ai
```

## Available Tools

### Crash Data Retrieval

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `list-crashes` | List recent crashes | `app_id`, optional: `limit`, `severity`, `platform` |
| `get-crash-details` | Get detailed crash info | `app_id`, `crash_id`, optional: `include_stacktrace` |
| `get-crash-trends` | Get crash statistics | `app_id`, optional: `time_period`, `group_by` |

### Crash Analysis

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `analyze-crash-pattern` | Analyze crash patterns | `app_id`, `crash_ids`, optional: `analysis_type` |
| `get-affected-users` | Get user impact data | `app_id`, `crash_id`, optional: `time_range` |

### AI-Powered Solutions

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `generate-solution` | AI crash solution | `app_id`, `crash_id`, optional: `detail_level`, `include_code` |
| `bulk-solution-analysis` | Bulk crash analysis | `app_id`, `crash_ids`, optional: `priority_order` |
| `suggest-preventive-measures` | Prevention suggestions | `app_id`, optional: `time_period`, `focus_area` |

### Reporting

| Tool | Description | Required Parameters |
|------|-------------|-------------------|
| `generate-crash-report` | Comprehensive report | `app_id`, optional: `time_period`, `include_solutions`, `format` |

## MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "firebase-crashlytics-mcp": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/agent/mcp/firebase-crashlytics && uv run main.py"
      ],
      "alwaysAllow": [
        "list-crashes",
        "get-crash-trends",
        "generate-solution"
      ]
    }
  }
}
```

## AI Solution Features

### Solution Detail Levels
- **Basic**: Quick fix suggestions and root cause
- **Detailed**: Comprehensive analysis with code examples
- **Expert**: Advanced architectural recommendations and monitoring

### AI Capabilities
- **Root Cause Analysis** - Deep understanding of crash origins
- **Code Fix Suggestions** - Specific code changes with examples
- **Prevention Strategies** - Proactive measures to avoid similar issues
- **Testing Recommendations** - How to validate fixes
- **Architecture Improvements** - Long-term code quality enhancements

## Examples

### Basic Crash Analysis
```
List recent crashes for app com.myapp.android
Get details for crash crash_123 with stack trace
Generate AI solution for crash crash_123 with detailed level
```

### Advanced Analysis
```
Analyze crash pattern for crashes [crash_123, crash_124, crash_125] using similarity analysis
Get affected users for crash crash_123 in the last 24 hours
Generate bulk solution analysis for crashes with priority ordering
```

### Reporting
```
Generate comprehensive crash report for last 7 days including AI solutions
Suggest preventive measures focusing on memory management
```

## Integration with SDLC Workflow

This MCP server perfectly integrates with your existing SDLC automation:

1. **Crash Detection** → Firebase Crashlytics MCP retrieves crash data
2. **AI Analysis** → Generate intelligent solutions and recommendations  
3. **Documentation** → Auto-generate crash reports and action plans
4. **Development** → Implement fixes using provided code examples
5. **Testing** → Follow AI-suggested testing strategies
6. **Deployment** → Use Docker MCP for deployment automation
7. **Monitoring** → Track improvements and prevent regressions

## Development

### Project Structure

```
src/
├── config.py          # Configuration management
├── firebase/          # Firebase service modules
│   ├── crashlytics.py # Crash data retrieval
│   └── analysis.py    # Pattern analysis & reporting
├── ai/               # AI solution modules
│   └── solutions.py  # OpenAI-powered solution generation
└── main.py           # MCP server entry point
```

### Running Tests

```bash
# Install test dependencies
uv sync --dev

# Run tests
uv run pytest
```

## Firebase Setup

1. **Enable Crashlytics in Firebase Console**
2. **Create Service Account**:
   - Go to Firebase Console → Project Settings → Service Accounts
   - Generate new private key
   - Download JSON file

3. **Set Permissions**:
   - Firebase Crashlytics Viewer
   - Firebase Analytics Viewer

## Troubleshooting

### Authentication Issues
- Verify Firebase credentials path
- Check service account permissions
- Ensure project ID is correct

### AI Solution Issues
- Verify OpenAI API key is valid
- Check API quota limits
- Ensure sufficient tokens for complex analysis

### Data Access Issues
- Confirm Crashlytics is enabled for your app
- Check app ID configuration
- Verify crash data exists for the specified time period

## Security Considerations

- Store Firebase credentials securely
- Use environment variables for sensitive data
- Limit service account permissions to minimum required
- Monitor OpenAI API usage to control costs

## Performance Tips

- Enable caching for frequently accessed crash data
- Use bulk analysis for multiple related crashes
- Adjust AI detail level based on needs
- Set appropriate request limits for large datasets

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request