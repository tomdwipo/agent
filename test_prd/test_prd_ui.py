#!/usr/bin/env python3
"""
Test script for PRD UI integration

This script tests the PRD UI components and integration.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_prd_components():
    """Test PRD UI components creation"""
    print("Testing PRD UI Components...")
    
    try:
        from ui.components import ComponentFactory
        from config.settings import settings
        
        # Test PRD output component creation
        print("1. Testing PRD output component creation...")
        prd_output = ComponentFactory.create_prd_output()
        print("   ✅ PRD output component created successfully")
        
        # Test PRD settings
        print("2. Testing PRD configuration...")
        print(f"   - PRD Generation Enabled: {settings.enable_prd_generation}")
        print(f"   - PRD OpenAI Model: {settings.prd_openai_model}")
        print(f"   - PRD Max Tokens: {settings.prd_max_tokens}")
        print(f"   - PRD Temperature: {settings.prd_temperature}")
        print(f"   - PRD File Prefix: {settings.prd_file_prefix}")
        print("   ✅ PRD configuration loaded successfully")
        
        # Test PRD config method
        print("3. Testing PRD config method...")
        prd_config = settings.get_prd_config()
        print(f"   - PRD Config: {prd_config}")
        print("   ✅ PRD config method works correctly")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_prd_services():
    """Test PRD services integration"""
    print("\nTesting PRD Services Integration...")
    
    try:
        from services.openai_service import OpenAIService
        from services.file_service import FileService
        
        # Test OpenAI service PRD method
        print("1. Testing OpenAI service PRD method...")
        openai_service = OpenAIService()
        
        # Check if method exists
        if hasattr(openai_service, 'generate_prd_from_key_points'):
            print("   ✅ generate_prd_from_key_points method exists")
        else:
            print("   ❌ generate_prd_from_key_points method missing")
            return False
        
        # Test File service PRD methods
        print("2. Testing File service PRD methods...")
        file_service = FileService()
        
        if hasattr(file_service, 'create_prd_download_file'):
            print("   ✅ create_prd_download_file method exists")
        else:
            print("   ❌ create_prd_download_file method missing")
            return False
            
        if hasattr(file_service, 'validate_prd_content'):
            print("   ✅ validate_prd_content method exists")
        else:
            print("   ❌ validate_prd_content method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_prd_interface():
    """Test PRD interface integration"""
    print("\nTesting PRD Interface Integration...")
    
    try:
        from ui.gradio_interface import GradioInterface
        from config.settings import settings
        
        # Test interface creation with PRD enabled
        print("1. Testing interface creation with PRD enabled...")
        interface = GradioInterface()
        
        # Check if PRD components are initialized
        if hasattr(interface, 'prd_btn'):
            print("   ✅ PRD button component attribute exists")
        else:
            print("   ❌ PRD button component attribute missing")
            return False
            
        if hasattr(interface, 'prd_output'):
            print("   ✅ PRD output component attribute exists")
        else:
            print("   ❌ PRD output component attribute missing")
            return False
            
        if hasattr(interface, 'prd_download_file'):
            print("   ✅ PRD download file component attribute exists")
        else:
            print("   ❌ PRD download file component attribute missing")
            return False
        
        # Check if PRD processing method exists
        if hasattr(interface, '_process_prd_generation'):
            print("   ✅ _process_prd_generation method exists")
        else:
            print("   ❌ _process_prd_generation method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 PRD UI Integration Test Suite")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_prd_components,
        test_prd_services,
        test_prd_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PRD UI integration is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)