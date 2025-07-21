# PRD Generation Feature

## Overview

The PRD (Product Requirements Document) Generation feature is a powerful addition to the Audio Transcription Tool that transforms meeting key points into structured product requirements documents. This feature leverages AI to analyze meeting discussions and automatically generate comprehensive PRDs following industry-standard templates.

## Feature Workflow

```
Audio File → Transcription → Key Points → PRD Generation → Download PRD
```

### Step-by-Step Process:
1. **Upload Audio**: User uploads meeting recording
2. **Generate Transcription**: AI transcribes the audio content
3. **Extract Key Points**: AI identifies and summarizes key meeting points
4. **Generate PRD**: **NEW** - AI transforms key points into structured PRD
5. **Download PRD**: User can download the PRD as a markdown (.md) file

## PRD Template Structure

The generated PRD follows a comprehensive 8-section template:

### 1. Executive Summary
- High-level overview of the product/feature
- Key value propositions
- Strategic alignment

### 2. Problem Statement
- Clear definition of the problem being solved
- Current pain points and challenges
- Market opportunity

### 3. Goals & Objectives
- Primary and secondary objectives
- Success criteria
- Business goals alignment

### 4. User Stories/Requirements
- Functional requirements
- User personas and use cases
- Acceptance criteria

### 5. Success Metrics
- Key Performance Indicators (KPIs)
- Measurable outcomes
- Success benchmarks

### 6. Timeline/Milestones
- Development phases
- Key deliverables
- Timeline estimates

### 7. Technical Requirements
- System requirements
- Technical constraints
- Integration needs

### 8. Risk Assessment
- Potential risks and challenges
- Mitigation strategies
- Contingency plans

## Usage Instructions

### Basic Usage

1. **Start the Application**
   ```bash
   uv run transcribe_gradio.py
   ```

2. **Upload Audio File**
   - Click "Upload Audio File" 
   - Select your meeting recording (MP3, WAV, M4A, etc.)

3. **Generate Transcription**
   - Click "🎯 Transcribe Audio"
   - Wait for transcription to complete

4. **Generate Key Points**
   - Click "🔑 Generate Key Points"
   - Review the extracted meeting key points

5. **Generate PRD** *(NEW)*
   - Click "📋 Generate PRD" (appears after key points)
   - Wait for AI to process and structure the PRD
   - Review the generated PRD in markdown format

6. **Download PRD**
   - Click the download button to save as `.md` file
   - File naming: `PRD_YYYY-MM-DD_HH-MM.md`

### Advanced Usage

#### Using Services Independently

```python
from services.openai_service import OpenAIService
from services.file_service import FileService

# Initialize services
openai_service = OpenAIService()
file_service = FileService()

# Generate PRD from key points
key_points = "Your meeting key points here..."
prd_content = openai_service.generate_prd_from_key_points(key_points)

# Create downloadable file
prd_file = file_service.create_prd_download_file(prd_content)
print(f"PRD saved to: {prd_file}")
```

## Configuration Options

### Environment Variables

Add to your `.env` file:

```env
# PRD Feature Configuration
ENABLE_PRD_GENERATION=true          # Enable/disable PRD feature
PRD_OPENAI_MODEL=gpt-4              # OpenAI model for PRD generation
PRD_MAX_TOKENS=2000                 # Maximum tokens for PRD generation
PRD_TEMPERATURE=0.3                 # Temperature for PRD generation (more structured)
PRD_FILE_PREFIX=PRD_                # Prefix for downloaded PRD files
```

### Feature Toggle

The PRD generation feature can be enabled/disabled via configuration:

```python
from config.settings import settings

if settings.enable_prd_generation:
    # PRD feature is available
    prd_button.visible = True
else:
    # PRD feature is disabled
    prd_button.visible = False
```

## Technical Implementation

### Service Layer Enhancements

#### OpenAIService Extensions

**New Method: `generate_prd_from_key_points()`**

```python
def generate_prd_from_key_points(self, key_points_text: str, model: str = None) -> str:
    """
    Generate a Product Requirements Document from meeting key points.
    
    Args:
        key_points_text (str): The meeting key points text
        model (str, optional): OpenAI model to use
        
    Returns:
        str: Generated PRD in markdown format
        
    Raises:
        Exception: If OpenAI API call fails
    """
```

**PRD Generation Prompt Template:**
- Structured prompt for consistent PRD format
- Includes all 8 required sections
- Optimized for product management context

#### FileService Extensions

**New Method: `create_prd_download_file()`**

```python
def create_prd_download_file(self, prd_content: str, filename: str = None) -> str:
    """
    Create a downloadable PRD file in markdown format.
    
    Args:
        prd_content (str): The PRD content in markdown
        filename (str, optional): Custom filename
        
    Returns:
        str: Path to the created file
    """
```

### UI Component Additions

#### New Components

**PRDOutputComponent**
- Displays generated PRD with markdown formatting
- Syntax highlighting for better readability
- Copy-to-clipboard functionality

**PRDActionButtonComponent**
- "Generate PRD" button with loading states
- Only visible when key points are available
- Integrated error handling

#### Updated Interface Flow

```python
# Enhanced GradioInterface workflow
class GradioInterface:
    def _create_prd_section(self):
        """Create PRD generation section"""
        
    def _setup_prd_handlers(self):
        """Setup PRD generation event handlers"""
        
    def _process_prd_generation(self, key_points: str) -> Tuple[str, gr.File]:
        """Process PRD generation from key points"""
```

### Configuration Updates

#### Constants Addition

```python
# PRD-related constants
PRD_TEMPLATE_SECTIONS = [
    "Executive Summary",
    "Problem Statement", 
    "Goals & Objectives",
    "User Stories/Requirements",
    "Success Metrics",
    "Timeline/Milestones",
    "Technical Requirements",
    "Risk Assessment"
]

PRD_UI_LABELS = {
    "generate_prd_button": "📋 Generate PRD",
    "prd_output_label": "Product Requirements Document",
    "prd_download_label": "Download PRD (.md)",
    "prd_generating": "Generating PRD...",
    "prd_error": "Error generating PRD"
}
```

## Example Output

### Sample PRD Generated from Meeting

```markdown
# Product Requirements Document
*Generated from meeting analysis on 2025-01-21*

## Executive Summary
Based on the meeting discussion, we are developing a new user dashboard feature that will provide real-time analytics and customizable widgets for improved user engagement and data visibility.

## Problem Statement
Current users struggle with accessing key metrics quickly, leading to decreased productivity and poor decision-making due to scattered information across multiple interfaces.

## Goals & Objectives
- **Primary**: Increase user engagement by 40% through improved dashboard experience
- **Secondary**: Reduce time-to-insight by 60% with real-time analytics
- **Business Goal**: Drive user retention and reduce churn rate

## User Stories/Requirements
- As a user, I want to see real-time metrics on my dashboard
- As an admin, I need customizable widgets for different user roles
- As a manager, I require exportable reports from dashboard data

## Success Metrics
- User engagement increase: 40%
- Time-to-insight reduction: 60%
- Dashboard adoption rate: 80%
- User satisfaction score: >4.5/5

## Timeline/Milestones
- **Phase 1** (Weeks 1-2): Design and wireframes
- **Phase 2** (Weeks 3-6): Core dashboard development
- **Phase 3** (Weeks 7-8): Widget customization features
- **Phase 4** (Weeks 9-10): Testing and deployment

## Technical Requirements
- React.js frontend with responsive design
- Real-time data streaming via WebSocket
- RESTful API for dashboard configuration
- Database optimization for analytics queries

## Risk Assessment
- **Risk**: API performance under high load
  - **Mitigation**: Implement caching and rate limiting
- **Risk**: Complex widget customization UX
  - **Mitigation**: User testing and iterative design
```

## API Reference

### OpenAIService Methods

#### `generate_prd_from_key_points(key_points_text, model=None)`

Generates a structured PRD from meeting key points.

**Parameters:**
- `key_points_text` (str): The meeting key points to analyze
- `model` (str, optional): OpenAI model to use (defaults to configured model)

**Returns:**
- `str`: Generated PRD in markdown format

**Example:**
```python
openai_service = OpenAIService()
prd = openai_service.generate_prd_from_key_points(key_points)
```

### FileService Methods

#### `create_prd_download_file(prd_content, filename=None)`

Creates a downloadable PRD file.

**Parameters:**
- `prd_content` (str): PRD content in markdown format
- `filename` (str, optional): Custom filename (auto-generated if not provided)

**Returns:**
- `str`: Path to the created file

**Example:**
```python
file_service = FileService()
file_path = file_service.create_prd_download_file(prd_content)
```

### UI Components

#### `PRDOutputComponent`

Displays generated PRD with formatting.

**Parameters:**
- `label` (str): Component label
- `lines` (int): Number of visible lines
- `max_lines` (int): Maximum expandable lines

#### `ComponentFactory.create_prd_output(**kwargs)`

Factory method for creating PRD output components.

**Example:**
```python
from ui.components import ComponentFactory

prd_output = ComponentFactory.create_prd_output(
    label="Generated PRD",
    lines=20,
    max_lines=50
)
```

## Development Roadmap

### Phase 1: Core Implementation ✅ (Complete)
- [x] Extend OpenAIService with PRD generation
- [x] Add PRD file handling to FileService
- [x] Update configuration for PRD settings
- [ ] Create basic PRD UI components

### Phase 2: UI Integration ✅ (Planned)
- [ ] Integrate PRD section into main interface
- [ ] Add PRD generation workflow
- [ ] Implement download functionality
- [ ] Add error handling and validation

### Phase 3: Testing & Documentation ✅ (Planned)
- [ ] Update example_usage.py with PRD examples
- [ ] Add PRD components to ui_demo.py
- [ ] Create comprehensive tests
- [ ] Update main README.md

### Phase 4: Future Enhancements 🔮 (Future)
- [ ] Multiple PRD templates (Feature PRD, Technical PRD, etc.)
- [ ] PRD template customization
- [ ] Export to other formats (PDF, DOCX)
- [ ] PRD version management
- [ ] Collaborative PRD editing
- [ ] Integration with project management tools

## Installation & Setup

### Prerequisites
- Existing Audio Transcription Tool setup
- OpenAI API key configured
- Python 3.8+ with required dependencies

### Enable PRD Feature

1. **Update Environment Variables**
   ```bash
   echo "ENABLE_PRD_GENERATION=true" >> .env
   echo "PRD_OPENAI_MODEL=gpt-4" >> .env
   ```

2. **Restart Application**
   ```bash
   uv run transcribe_gradio.py
   ```

3. **Verify Feature**
   - Upload audio and generate key points
   - Look for "📋 Generate PRD" button
   - Test PRD generation and download

## Troubleshooting

### Common Issues

**PRD Generation Button Not Visible**
- Check `ENABLE_PRD_GENERATION=true` in .env
- Ensure key points are generated first
- Verify OpenAI API key is configured

**PRD Generation Fails**
- Check OpenAI API key validity
- Verify internet connection
- Check API rate limits
- Review error logs for specific issues

**Download Not Working**
- Check file permissions
- Verify temporary directory access
- Clear browser cache

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "PRD feature disabled" | Feature not enabled | Set `ENABLE_PRD_GENERATION=true` |
| "No key points available" | PRD requested before key points | Generate key points first |
| "OpenAI API error" | API call failed | Check API key and connection |
| "File creation failed" | File system error | Check permissions and disk space |

## Contributing

### Adding New PRD Templates

1. **Define Template Structure**
   ```python
   NEW_PRD_TEMPLATE = {
       "sections": [...],
       "prompt": "...",
       "format": "markdown"
   }
   ```

2. **Update Constants**
   ```python
   PRD_TEMPLATES = {
       "standard": STANDARD_PRD_TEMPLATE,
       "technical": TECHNICAL_PRD_TEMPLATE,
       "new_template": NEW_PRD_TEMPLATE
   }
   ```

3. **Add UI Selection**
   - Add template selector to UI
   - Update generation logic
   - Test with various inputs

### Code Style

Follow existing project patterns:
- Service-oriented architecture
- Configuration-driven behavior
- Component-based UI
- Comprehensive error handling
- Backward compatibility

## License

This feature follows the same license as the main Audio Transcription Tool project.

---

**Built with ❤️ as an extension to the Audio Transcription Tool**
*Transforming meeting discussions into actionable product requirements*
