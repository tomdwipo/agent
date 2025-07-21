"""
Configuration Demo Script

Demonstrates the new configuration management system introduced in Phase 2.
"""

from config.settings import settings, env_config
from config.constants import (
    APP_NAME, APP_VERSION, 
    WHISPER_MODELS, OPENAI_MODELS,
    get_version_string, get_supported_formats_string,
    is_supported_audio_format
)


def main():
    """Demonstrate the configuration management system"""
    
    print("🔧 Configuration Management Demo")
    print("=" * 60)
    
    # Application Information
    print(f"\n📱 Application Information:")
    print(f"   Name: {APP_NAME}")
    print(f"   Version: {get_version_string()}")
    print(f"   Environment: {env_config.get_environment()}")
    print(f"   Project Root: {env_config.get_project_root()}")
    
    # Settings Overview
    print(f"\n⚙️  Current Settings:")
    settings.print_settings_summary()
    
    # Configuration Details
    print(f"\n🎛️  Detailed Configuration:")
    
    # Whisper Configuration
    whisper_config = settings.get_whisper_config()
    print(f"   Whisper Model: {whisper_config['model']}")
    print(f"   FP16 Enabled: {whisper_config['fp16']}")
    
    # OpenAI Configuration
    if settings.is_openai_configured():
        openai_config = settings.get_openai_config()
        print(f"   OpenAI Model: {openai_config['model']}")
        print(f"   Max Tokens: {openai_config['max_tokens']}")
        print(f"   Temperature: {openai_config['temperature']}")
    else:
        print(f"   OpenAI: Not configured")
    
    # File Configuration
    file_config = settings.get_file_config()
    print(f"   Max File Size: {file_config['max_size_mb']}MB")
    print(f"   Temp File Prefix: {file_config['temp_prefix']}")
    
    # Gradio Configuration
    gradio_config = settings.get_gradio_config()
    print(f"   Gradio Port: {gradio_config['server_port']}")
    print(f"   Debug Mode: {gradio_config['debug']}")
    print(f"   Theme: {gradio_config['theme']}")
    
    # Available Models
    print(f"\n🤖 Available Models:")
    print(f"   Whisper Models:")
    for name, info in WHISPER_MODELS.items():
        print(f"     - {name}: {info['description']}")
    
    print(f"   OpenAI Models:")
    for name, info in OPENAI_MODELS.items():
        print(f"     - {name}: {info['description']}")
    
    # Supported Formats
    print(f"\n📁 Supported Audio Formats:")
    print(f"   {get_supported_formats_string()}")
    
    # Format Testing
    print(f"\n🧪 Format Validation Tests:")
    test_files = [".mp3", ".wav", ".txt", ".pdf", ".flac"]
    for ext in test_files:
        is_valid = is_supported_audio_format(ext)
        status = "✅" if is_valid else "❌"
        print(f"   {ext}: {status}")
    
    # Environment Variables
    print(f"\n🌍 Environment Detection:")
    print(f"   Is Development: {env_config.is_development()}")
    print(f"   Is Production: {env_config.is_production()}")
    print(f"   Is Testing: {env_config.is_testing()}")
    
    # Settings Validation
    print(f"\n✅ Settings Validation:")
    issues = settings.validate_settings()
    if issues:
        print(f"   Issues found:")
        for key, issue in issues.items():
            print(f"     - {key}: {issue}")
    else:
        print(f"   All settings are valid!")
    
    # Configuration Usage Examples
    print(f"\n💡 Usage Examples:")
    print(f"   # Get OpenAI configuration")
    print(f"   config = settings.get_openai_config()")
    print(f"   client = OpenAI(api_key=config['api_key'])")
    print(f"")
    print(f"   # Check if feature is enabled")
    print(f"   if settings.enable_key_points:")
    print(f"       # Show key points UI")
    print(f"")
    print(f"   # Validate audio file")
    print(f"   is_valid = is_supported_audio_format('.mp3')")
    print(f"")
    print(f"   # Get file size limit")
    print(f"   max_size = settings.max_file_size_mb")
    
    print(f"\n🎉 Configuration Demo Complete!")
    print(f"\nThe new configuration system provides:")
    print(f"  ✅ Centralized settings management")
    print(f"  ✅ Environment variable support")
    print(f"  ✅ Settings validation")
    print(f"  ✅ Easy configuration access")
    print(f"  ✅ Default value handling")
    print(f"  ✅ Type safety and validation")


if __name__ == "__main__":
    main()
