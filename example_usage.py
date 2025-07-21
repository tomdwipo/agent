"""
Example Usage of Refactored Services

This script demonstrates how to use the individual services independently
without the Gradio interface.
"""

from services.whisper_service import WhisperService
from services.openai_service import OpenAIService
from services.file_service import FileService


def main():
    """Demonstrate usage of the refactored services"""
    
    print("🎵 Audio Transcription Services Demo")
    print("=" * 50)
    
    # Initialize services
    whisper_service = WhisperService(model_name="base")
    openai_service = OpenAIService()
    file_service = FileService()
    
    # Example 1: Check service availability
    print("\n1. Service Status Check:")
    print(f"   OpenAI Service: {openai_service.get_availability_status()}")
    
    # Example 2: File validation
    print("\n2. File Validation Example:")
    audio_file = "denver_extract.mp3"  # Your existing audio file
    is_valid, message = file_service.validate_audio_file(audio_file)
    print(f"   File '{audio_file}' validation: {message}")
    
    if is_valid:
        # Get file info
        file_info = file_service.get_file_info(audio_file)
        if file_info:
            print(f"   File size: {file_info['size_mb']} MB")
            print(f"   Extension: {file_info['extension']}")
    
    # Example 3: Transcription (if file exists)
    if is_valid:
        print(f"\n3. Transcription Example:")
        print("   Starting transcription...")
        
        transcription, temp_file = whisper_service.transcribe_audio(audio_file)
        
        if temp_file:
            print("   ✅ Transcription completed successfully!")
            print(f"   Preview: {transcription[:100]}...")
            print(f"   Saved to: {temp_file}")
            
            # Example 4: Generate key points (if OpenAI is available)
            if openai_service.is_available():
                print(f"\n4. Key Points Generation:")
                print("   Generating meeting key points...")
                
                key_points = openai_service.generate_meeting_key_points(transcription)
                print("   ✅ Key points generated!")
                print(f"   Preview: {key_points[:200]}...")
                
                # Save key points to file
                key_points_file = file_service.create_temp_text_file(
                    key_points, 
                    suffix='_keypoints.txt'
                )
                if key_points_file:
                    print(f"   Key points saved to: {key_points_file}")
            else:
                print(f"\n4. Key Points Generation:")
                print("   ❌ OpenAI service not available")
                print(f"   Status: {openai_service.get_availability_status()}")
        else:
            print("   ❌ Transcription failed")
            print(f"   Error: {transcription}")
    
    # Example 5: Custom analysis (if OpenAI is available and we have transcription)
    if is_valid and openai_service.is_available() and 'transcription' in locals():
        print(f"\n5. Custom Analysis Example:")
        custom_prompt = "Summarize this transcription in 3 bullet points focusing on the main topics discussed."
        
        custom_analysis = openai_service.generate_custom_analysis(
            transcription, 
            custom_prompt
        )
        print("   ✅ Custom analysis completed!")
        print(f"   Result: {custom_analysis[:200]}...")
    
    print(f"\n🎉 Demo completed!")
    print("\nYou can now use these services in your own applications:")
    print("- WhisperService: For audio transcription")
    print("- OpenAIService: For AI-powered analysis")
    print("- FileService: For file operations")


if __name__ == "__main__":
    main()
