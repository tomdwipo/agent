"""
OpenAI Service Module

Handles OpenAI API integration for generating meeting key points and other AI-powered features.
"""

import os
from openai import OpenAI
from config.settings import settings
from config.constants import (
    DEFAULT_OPENAI_MODEL,
    DEFAULT_OPENAI_MAX_TOKENS,
    DEFAULT_OPENAI_TEMPERATURE,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    TRD_SECTIONS
)

OPENAI_AVAILABLE = True


class OpenAIService:
    """Service class for handling OpenAI API operations"""
    
    def __init__(self):
        """Initialize OpenAIService"""
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client if API key is available"""
        if settings.is_openai_configured():
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def is_available(self):
        """
        Check if OpenAI service is available
        
        Returns:
            bool: True if OpenAI is available and configured
        """
        return OPENAI_AVAILABLE and self.client is not None
    
    def get_availability_status(self):
        """
        Get detailed availability status
        
        Returns:
            str: Status message explaining availability
        """
        if not OPENAI_AVAILABLE:
            return "❌ OpenAI library not installed. Please install it with: pip install openai"
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-openai-api-key-here":
            return "❌ OpenAI API key not configured. Please add your API key to the .env file."
        
        if not self.client:
            return "❌ OpenAI client initialization failed. Please check your API key."
        
        return "✅ OpenAI service is available and configured."
    
    def generate_meeting_key_points(self, transcription_text, model=None):
        """
        Generate key meeting points from transcription using OpenAI GPT
        
        Args:
            transcription_text (str): The transcription text to analyze
            model (str): OpenAI model to use (if None, uses configuration setting)
            
        Returns:
            str: Generated key meeting points or error message
        """
        if not transcription_text or transcription_text.strip() == "":
            return ERROR_MESSAGES["no_transcription"]
        
        # Check availability
        if not self.is_available():
            return self.get_availability_status()
        
        # Use configured model if not specified
        model = model or settings.openai_model
        
        try:
            # Create prompt for key meeting points extraction
            prompt = f"""
Please analyze the following meeting transcription and extract key information in a structured format:

TRANSCRIPTION:
{transcription_text}

Please provide the analysis in the following format:

## 📋 Meeting Summary
[2-3 sentence summary of the meeting]

## 🎯 Key Topics Discussed
• [Topic 1]
• [Topic 2]
• [Topic 3]

## ✅ Action Items
• [Action item 1 - Person responsible if mentioned]
• [Action item 2 - Person responsible if mentioned]

## 🔑 Decisions Made
• [Decision 1]
• [Decision 2]

## 🚀 Next Steps
• [Next step 1]
• [Next step 2]

## 👥 Participants (if mentioned)
• [Participant names if clearly mentioned]

Focus on extracting concrete, actionable information. If certain sections don't apply or aren't clear from the transcription, you can omit them or note "Not specified in the transcription."
"""

            # Call OpenAI API with configured settings
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that extracts key meeting points from transcriptions. Provide clear, structured summaries."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return ERROR_MESSAGES["openai_request_failed"].format(error=str(e))
    
    def generate_custom_analysis(self, transcription_text, custom_prompt, model="gpt-3.5-turbo"):
        """
        Generate custom analysis from transcription using a custom prompt
        
        Args:
            transcription_text (str): The transcription text to analyze
            custom_prompt (str): Custom prompt for analysis
            model (str): OpenAI model to use (default: gpt-3.5-turbo)
            
        Returns:
            str: Generated analysis or error message
        """
        if not transcription_text or transcription_text.strip() == "":
            return "No transcription text provided."
        
        if not custom_prompt or custom_prompt.strip() == "":
            return "No custom prompt provided."
        
        # Check availability
        if not self.is_available():
            return self.get_availability_status()
        
        try:
            full_prompt = f"{custom_prompt}\n\nTRANSCRIPTION:\n{transcription_text}"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that analyzes transcriptions based on user requirements."
                    },
                    {
                        "role": "user", 
                        "content": full_prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ Error generating custom analysis: {str(e)}\n\nPlease check your OpenAI API key and internet connection."
    
    def generate_prd_from_key_points(self, key_points_text, model=None):
        """
        Generate a Product Requirements Document from meeting key points
        
        Args:
            key_points_text (str): The meeting key points text to analyze
            model (str): OpenAI model to use (if None, uses configuration setting)
            
        Returns:
            str: Generated PRD in markdown format or error message
        """
        if not key_points_text or key_points_text.strip() == "":
            return ERROR_MESSAGES.get("no_key_points", "No key points provided for PRD generation.")
        
        # Check availability
        if not self.is_available():
            return self.get_availability_status()
        
        # Use configured model if not specified
        model = model or settings.openai_model
        
        try:
            # Create comprehensive PRD generation prompt
            prompt = f"""
Based on the following meeting key points, generate a comprehensive Product Requirements Document (PRD) in markdown format.

MEETING KEY POINTS:
{key_points_text}

Please create a structured PRD with the following sections:

# Product Requirements Document
*Generated from meeting analysis on [current date]*

## Executive Summary
[Provide a high-level overview of the product/feature, key value propositions, and strategic alignment based on the meeting discussion]

## Problem Statement
[Define the problem being solved, current pain points, challenges, and market opportunity mentioned in the meeting]

## Goals & Objectives
[List primary and secondary objectives, success criteria, and business goals alignment from the discussion]

## User Stories/Requirements
[Extract and format functional requirements, user personas, use cases, and acceptance criteria mentioned]

## Success Metrics
[Identify Key Performance Indicators (KPIs), measurable outcomes, and success benchmarks discussed]

## Timeline/Milestones
[Outline development phases, key deliverables, and timeline estimates if mentioned in the meeting]

## Technical Requirements
[List system requirements, technical constraints, and integration needs discussed]

## Risk Assessment
[Identify potential risks, challenges, mitigation strategies, and contingency plans mentioned or implied]

IMPORTANT GUIDELINES:
- Base the PRD content strictly on information from the meeting key points
- If specific information is not available in the key points, note "To be determined" or "Not specified in meeting"
- Use professional product management language and formatting
- Make reasonable inferences where appropriate but clearly distinguish between explicit and inferred information
- Ensure each section is substantive and actionable
- Use bullet points, numbered lists, and clear formatting for readability
"""

            # Call OpenAI API with PRD-specific settings
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert product manager who creates comprehensive Product Requirements Documents. Generate well-structured, professional PRDs based on meeting discussions."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=getattr(settings, 'prd_max_tokens', 2000),
                temperature=getattr(settings, 'prd_temperature', 0.3)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return ERROR_MESSAGES.get("openai_request_failed", "❌ Error generating PRD: {error}").format(error=str(e))

    def generate_android_trd_from_prd(self, prd_content: str) -> str:
        """
        Generate comprehensive Android TRD from PRD content using OpenAI GPT.
        
        Args:
            prd_content (str): Complete PRD markdown content
            
        Returns:
            str: Generated comprehensive Android TRD in markdown format
        """
        if not prd_content or prd_content.strip() == "":
            return ERROR_MESSAGES["no_prd_content"]

        if not settings.enable_trd_generation:
            return ERROR_MESSAGES["trd_feature_disabled"]

        if not self.is_available():
            return self.get_availability_status()

        try:
            prompt = f"""
You are an expert technical writer and Android architect. Generate a comprehensive Technical Requirements Document (TRD) for an Android application based on the provided Product Requirements Document (PRD).

The TRD must follow this EXACT comprehensive structure with ALL sections included:

# [App Name] - Technical Requirements Document

**Feature Version**: v1.0 (Planned)  
**Status**: 🔄 IN DEVELOPMENT  
**Priority**: [High/Medium/Low based on PRD]  
**Target Platform**: Android  

## 📋 Feature Overview
[2-3 paragraph overview of the application and its technical approach]

### Development Workflow
```
PRD Analysis → Technical Design → **Android Implementation** → Testing → Deployment
```

## 🎯 Feature Requirements

### Functional Requirements
- **FR-1**: [Primary functional requirement]
- **FR-2**: [Secondary functional requirement]
- **FR-3**: [Additional requirements...]

### Non-Functional Requirements
- **NFR-1**: [Performance requirement]
- **NFR-2**: [Scalability requirement]
- **NFR-3**: [Reliability requirement]
- **NFR-4**: [Security requirement]

## 🏗️ Technical Architecture

### System Architecture Overview
[Describe the overall architecture approach]

#### Core Architecture Components
```kotlin
// Example architecture structure
class MainActivity : AppCompatActivity() {{
    // Main entry point
}}

class [Feature]ViewModel : ViewModel() {{
    // Business logic layer
}}

class [Feature]Repository {{
    // Data access layer
}}
```

## 📋 Android Technical Implementation

### 1. Architecture Overview
**Purpose**: Define the high-level system architecture and core components.

**Implementation Details**:
- **App Architecture Pattern**: [MVVM/MVP/Clean Architecture with specific rationale]
- **Core Components**: [Detailed component breakdown]
- **Data Flow**: [Complete user interaction flow]
- **Third-party Libraries**: [Specific libraries with versions]
- **Module Structure**: [Feature and shared modules]

### 2. UI/UX Specifications
**Purpose**: Define user interface components and user experience flows.

**Implementation Details**:
- **Screen Hierarchy**: [Navigation structure and flow]
- **UI Components**: [Custom views and reusable components]
- **User Interactions**: [Touch events and input handling]
- **Responsive Design**: [Screen adaptation strategies]
- **Material Design**: [Design system implementation]

### 3. API Requirements
**Purpose**: Specify backend integration and network communication.

**Implementation Details**:
- **REST Endpoints**: [Complete API specification]
- **Data Models**: [Request/Response structures]
- **Network Layer**: [HTTP client and error handling]
- **Authentication**: [Token management and security]
- **Error Handling**: [Network failure strategies]

### 4. Database Schema
**Purpose**: Define local data storage and management.

**Implementation Details**:
- **Local Database**: [Room entities and DAOs]
- **Data Relationships**: [Entity relationships and indexing]
- **Caching Strategy**: [Offline support and synchronization]
- **Migration Strategy**: [Database versioning]
- **Data Models**: [Entity definitions and converters]

### 5. Security Requirements
**Purpose**: Specify security measures and data protection.

**Implementation Details**:
- **Data Encryption**: [Local and network security]
- **Authentication Flow**: [Login and session management]
- **Permission Handling**: [Runtime permissions]
- **Code Obfuscation**: [ProGuard/R8 configuration]
- **API Security**: [Token validation and signing]

### 6. Performance Requirements
**Purpose**: Define performance targets and optimization strategies.

**Implementation Details**:
- **Response Times**: [Specific performance targets]
- **Memory Management**: [Optimization strategies]
- **Battery Optimization**: [Background task management]
- **Network Efficiency**: [Caching and batching]
- **UI Performance**: [60fps targets and animations]

### 7. Testing Strategy
**Purpose**: Define comprehensive testing approach.

**Implementation Details**:
- **Unit Testing**: [Business logic coverage]
- **Integration Testing**: [API and database testing]
- **UI Testing**: [Espresso test specifications]
- **Performance Testing**: [Memory and ANR testing]
- **Test Coverage**: [Coverage requirements and quality gates]

## 🔧 Implementation Plan

### Phase 1: Core Architecture Setup (Week 1-2)
- [ ] Project structure and module setup
- [ ] Core architecture implementation
- [ ] Basic navigation framework
- [ ] Development environment configuration

### Phase 2: Feature Development (Week 3-6)
- [ ] Core feature implementation
- [ ] UI/UX development
- [ ] API integration
- [ ] Database implementation

### Phase 3: Integration & Testing (Week 7-8)
- [ ] Feature integration
- [ ] Comprehensive testing
- [ ] Performance optimization
- [ ] Security implementation

### Phase 4: Deployment & Launch (Week 9-10)
- [ ] Production build configuration
- [ ] App store preparation
- [ ] Launch and monitoring setup
- [ ] Post-launch support

## 🎯 Success Criteria

### Technical Success Criteria
- [ ] **SC-1**: All core features implemented and functional
- [ ] **SC-2**: Performance targets met (startup < 3s, smooth 60fps UI)
- [ ] **SC-3**: Security requirements fully implemented
- [ ] **SC-4**: Test coverage > 80% with all critical paths covered
- [ ] **SC-5**: Production-ready build with proper obfuscation

### User Experience Success Criteria
- [ ] **SC-6**: Intuitive navigation and user flows
- [ ] **SC-7**: Responsive design across all target devices
- [ ] **SC-8**: Accessibility compliance (WCAG 2.1 AA)
- [ ] **SC-9**: Offline functionality where applicable
- [ ] **SC-10**: Fast and reliable performance

## 🔍 Quality Assurance

### Testing Strategy
1. **Unit Testing**: JUnit and Mockito for business logic
2. **Integration Testing**: Room database and API integration
3. **UI Testing**: Espresso for user interface validation
4. **Performance Testing**: Memory profiling and ANR detection
5. **Security Testing**: Penetration testing and code analysis

### Code Quality Standards
- Kotlin coding standards and best practices
- SOLID principles and clean architecture
- Comprehensive documentation and comments
- Code review process and quality gates
- Automated testing and CI/CD integration

## 📊 Metrics & Monitoring

### Key Performance Indicators
- **App Performance**: Startup time, memory usage, battery consumption
- **User Engagement**: Session duration, feature adoption, retention rates
- **Technical Metrics**: Crash rate, ANR rate, API response times
- **Quality Metrics**: Test coverage, code quality scores, bug density

### Monitoring Implementation
- Firebase Analytics for user behavior tracking
- Crashlytics for crash reporting and analysis
- Performance monitoring for app vitals
- Custom metrics for business-specific KPIs

## 🚀 Future Enhancements (v2.0+)

### Potential Extensions
- **Advanced Features**: [Feature-specific enhancements]
- **Platform Expansion**: Tablet optimization, Android TV support
- **Integration Capabilities**: Third-party service integrations
- **Performance Optimizations**: Advanced caching, background processing
- **User Experience**: Personalization, advanced UI components

### Scalability Considerations
- Modular architecture for feature expansion
- Microservices integration capabilities
- Advanced caching and offline strategies
- Multi-language and localization support

## 📝 Notes & Considerations

### Technical Considerations
- **Android Version Support**: Minimum API level and target SDK
- **Device Compatibility**: Screen sizes, hardware requirements
- **Performance Constraints**: Memory limits, battery optimization
- **Security Compliance**: Data protection regulations
- **Maintenance Strategy**: Update cycles and backward compatibility

### Business Considerations
- **Development Timeline**: Resource allocation and milestone planning
- **Cost Implications**: Development, testing, and maintenance costs
- **Risk Assessment**: Technical risks and mitigation strategies
- **Market Considerations**: Competition analysis and differentiation

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: After Phase 1 completion  
**Owner**: Development Team

---

**PRODUCT REQUIREMENTS DOCUMENT (PRD) ANALYSIS:**

{prd_content}

---

**GENERATION GUIDELINES:**
1. **Comprehensive Structure**: Include ALL sections above - header, overview, requirements, architecture, implementation, plan, criteria, QA, metrics, future, and notes
2. **Technical Depth**: Provide specific Android implementation details, library recommendations, and code examples where appropriate
3. **Actionable Content**: Each section should provide concrete, implementable guidance for the development team
4. **PRD Integration**: Base all technical decisions on the provided PRD content, making reasonable technical inferences
5. **Professional Format**: Use consistent markdown formatting with emojis, checkboxes, and clear structure
6. **Realistic Planning**: Provide achievable timelines and milestones based on typical Android development cycles
7. **Quality Focus**: Emphasize testing, security, performance, and maintainability throughout
8. **Future-Proof**: Consider scalability and extensibility in all technical recommendations

Generate a complete, professional TRD that serves as a comprehensive technical specification for the Android development team.
"""

            response = self.client.chat.completions.create(
                model=settings.trd_openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Android architect and technical writer creating comprehensive Technical Requirements Documents. Generate detailed, professional TRDs that serve as complete technical specifications for development teams."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=settings.trd_max_tokens,
                temperature=settings.trd_temperature
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return ERROR_MESSAGES["trd_generation_failed"].format(error=str(e))


# Global instance for backward compatibility
_openai_service = OpenAIService()

def generate_meeting_key_points(transcription_text):
    """
    Legacy function for backward compatibility
    Generate key meeting points from transcription using OpenAI GPT
    """
    return _openai_service.generate_meeting_key_points(transcription_text)

def generate_prd_from_key_points(key_points_text):
    """
    Legacy function for backward compatibility
    Generate PRD from meeting key points using OpenAI GPT
    """
    return _openai_service.generate_prd_from_key_points(key_points_text)
