"""
UI Components Demo Script

Demonstrates the new UI component system introduced in Phase 3.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from ui.components import ComponentFactory
from ui.gradio_interface import create_gradio_interface, GradioInterface, SimpleGradioInterface
from config.settings import settings


def demo_individual_components():
    """Demonstrate individual UI components"""
    
    print("🎨 UI Components Demo")
    print("=" * 50)
    
    print("\n📦 Available Components:")
    print("  - AudioInputComponent: Reusable audio input with customization")
    print("  - TranscriptionOutputComponent: Configurable text output")
    print("  - KeyPointsOutputComponent: Specialized key points display")
    print("  - ActionButtonComponent: Customizable buttons")
    print("  - DownloadFileComponent: File download handling")
    print("  - HeaderComponent: Dynamic header with title/description")
    print("  - InstructionsComponent: Context-aware instructions")
    print("  - StatusIndicatorComponent: Real-time status display")
    print("  - ProgressBarComponent: Progress indication")
    print("  - SettingsDisplayComponent: Configuration overview")
    print("  - ThemeComponent: Theme management")
    
    print("\n🏭 Component Factory:")
    print("  - ComponentFactory: Centralized component creation")
    print("  - Convenience functions for easy component access")
    print("  - Consistent styling and configuration")
    
    print("\n🎛️  Component Features:")
    print("  ✅ Configuration-driven: Uses settings and constants")
    print("  ✅ Reusable: Can be used across different interfaces")
    print("  ✅ Customizable: Accept parameters for customization")
    print("  ✅ Consistent: Uniform styling and behavior")
    print("  ✅ Maintainable: Centralized component logic")


def demo_interface_types():
    """Demonstrate different interface types"""
    
    print("\n🖥️  Interface Types:")
    print("=" * 30)
    
    print("\n1. Standard Interface (GradioInterface):")
    print("   - Full-featured interface with all components")
    print("   - Configuration-driven layout and behavior")
    print("   - Supports transcription and key points generation")
    print("   - Debug mode with settings display")
    
    print("\n2. Simple Interface (SimpleGradioInterface):")
    print("   - Minimal interface for basic transcription")
    print("   - Single input/output design")
    print("   - Lightweight and fast")
    
    print("\n3. Custom Interface (CustomGradioInterface):")
    print("   - Fully customizable interface")
    print("   - Custom components and handlers")
    print("   - Advanced use cases")
    
    print("\n🚀 Interface Factory:")
    print("   - create_gradio_interface() function")
    print("   - Support for different interface types")
    print("   - Easy switching between interface modes")


def demo_component_customization():
    """Demonstrate component customization"""
    
    print("\n🎨 Component Customization Examples:")
    print("=" * 40)
    
    print("\n# Audio Input Customization:")
    print("audio_input = ComponentFactory.create_audio_input(")
    print("    label='Upload Your Audio File',")
    print("    sources=['upload', 'microphone']")
    print(")")
    
    print("\n# Transcription Output Customization:")
    print("transcription_output = ComponentFactory.create_transcription_output(")
    print("    label='AI Transcription Result',")
    print("    placeholder='Your transcription will appear here...',")
    print("    lines=15,")
    print("    max_lines=30")
    print(")")
    
    print("\n# Button Customization:")
    print("custom_button = ComponentFactory.create_action_button(")
    print("    text='🎯 Start Transcription',")
    print("    variant='primary',")
    print("    size='lg'")
    print(")")
    
    print("\n# Header Customization:")
    print("header = ComponentFactory.create_header(")
    print("    title='# 🎵 My Custom Audio App',")
    print("    description='Custom description here'")
    print(")")


def demo_configuration_integration():
    """Demonstrate configuration integration"""
    
    print("\n⚙️  Configuration Integration:")
    print("=" * 35)
    
    print("\n🔧 Settings Integration:")
    print(f"   - Theme: {settings.get_gradio_config()['theme']}")
    print(f"   - Key Points Enabled: {settings.enable_key_points}")
    print(f"   - Debug Mode: {settings.get_gradio_config()['debug']}")
    print(f"   - Server Port: {settings.get_gradio_config()['server_port']}")
    
    print("\n📝 Dynamic Content:")
    print("   - Instructions adapt to enabled features")
    print("   - UI labels from configuration constants")
    print("   - Theme selection from settings")
    print("   - Feature toggles control component visibility")
    
    print("\n🎯 Benefits:")
    print("   ✅ No hardcoded UI text")
    print("   ✅ Consistent styling across components")
    print("   ✅ Easy customization without code changes")
    print("   ✅ Environment-specific UI behavior")


def create_demo_interface():
    """Create a demo interface showcasing components"""
    
    with gr.Blocks(title="UI Components Demo", theme=ComponentFactory.get_theme()) as demo:
        
        # Header
        header_components = ComponentFactory.create_header(
            title="# 🎨 UI Components Demo",
            description="Showcasing the modular UI component system"
        )
        for component in header_components:
            component.render()
        
        with gr.Tabs():
            
            # Standard Components Tab
            with gr.TabItem("Standard Components"):
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Audio Input Component")
                        audio_demo = ComponentFactory.create_audio_input()
                        
                        gr.Markdown("### Action Button Component")
                        button_demo = ComponentFactory.create_action_button(
                            "Demo Button", variant="secondary"
                        )
                    
                    with gr.Column():
                        gr.Markdown("### Transcription Output Component")
                        transcription_demo = ComponentFactory.create_transcription_output(
                            placeholder="Demo transcription output..."
                        )
                        
                        gr.Markdown("### TRD Output Component")
                        trd_demo = ComponentFactory.create_trd_output(
                            placeholder="Demo TRD output..."
                        )
            
            # Custom Components Tab
            with gr.TabItem("Custom Components"):
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Custom Audio Input")
                        custom_audio = ComponentFactory.create_audio_input(
                            label="🎤 Custom Audio Upload"
                        )
                        
                        gr.Markdown("### Custom Button")
                        custom_button = ComponentFactory.create_action_button(
                            "🚀 Custom Action", variant="primary"
                        )
                    
                    with gr.Column():
                        gr.Markdown("### Custom Output")
                        custom_output = ComponentFactory.create_transcription_output(
                            label="📝 Custom Results",
                            placeholder="Custom placeholder text...",
                            lines=8
                        )
            
            # Settings Tab
            with gr.TabItem("Settings Display"):
                settings_display = ComponentFactory.create_settings_display()
                settings_display.render()
        
        # Instructions
        instructions_components = ComponentFactory.create_instructions(
            title="### 📖 Demo Instructions",
            instructions="This demo showcases the modular UI component system. Each component is reusable and configurable."
        )
        for component in instructions_components:
            component.render()
    
    return demo


def main():
    """Main demo function"""
    
    demo_individual_components()
    demo_interface_types()
    demo_component_customization()
    demo_configuration_integration()
    
    print("\n🎉 UI Components Demo Complete!")
    print("\nThe new UI system provides:")
    print("  ✅ Modular, reusable components")
    print("  ✅ Configuration-driven behavior")
    print("  ✅ Multiple interface types")
    print("  ✅ Easy customization")
    print("  ✅ Consistent styling")
    print("  ✅ Better maintainability")
    
    print("\n🚀 Usage Examples:")
    print("  # Create standard interface")
    print("  interface = GradioInterface().create_interface()")
    print("")
    print("  # Create simple interface")
    print("  interface = create_gradio_interface('simple')")
    print("")
    print("  # Use individual components")
    print("  audio_input = ComponentFactory.create_audio_input()")
    print("  transcription_output = ComponentFactory.create_transcription_output()")
    
    # Optionally launch demo interface
    print("\n💡 To see the interactive demo, uncomment the lines below:")
    print("# demo_interface = create_demo_interface()")
    print("# demo_interface.launch()")


if __name__ == "__main__":
    main()
    
    # Uncomment to launch interactive demo
    # demo_interface = create_demo_interface()
    # demo_interface.launch(server_port=7861, share=False)
