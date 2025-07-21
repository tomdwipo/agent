"""
Demo Scripts Registry

Centralized access to all demonstration scripts for the Audio Transcription Tool.
"""

from .config_demo import main as config_demo
from .services_demo import main as services_demo
from .ui_demo import main as ui_demo
from .test_runner import main as test_runner

__all__ = ['config_demo', 'services_demo', 'ui_demo', 'test_runner']

AVAILABLE_DEMOS = {
    'config': {
        'name': 'Configuration Demo',
        'description': 'Demonstrates the configuration management system',
        'function': config_demo,
        'file': 'config_demo.py'
    },
    'services': {
        'name': 'Services Demo',
        'description': 'Shows how to use the refactored services independently',
        'function': services_demo,
        'file': 'services_demo.py'
    },
    'ui': {
        'name': 'UI Components Demo',
        'description': 'Demonstrates the UI component system',
        'function': ui_demo,
        'file': 'ui_demo.py'
    },
    'test': {
        'name': 'Test Runner',
        'description': 'Runs all tests for the application including PRD functionality',
        'function': test_runner,
        'file': 'test_runner.py'
    }
}


def list_available_demos():
    """List all available demo scripts with descriptions"""
    print("🎯 Available Demo Scripts")
    print("=" * 50)
    
    for key, demo in AVAILABLE_DEMOS.items():
        print(f"\n📁 {demo['name']} ({demo['file']})")
        print(f"   {demo['description']}")
        print(f"   Usage: uv run demos/{demo['file']}")
    
    print(f"\n💡 You can also run demos programmatically:")
    print(f"   from demos import config_demo, services_demo, ui_demo, test_runner")
    print(f"   config_demo()  # Run configuration demo")


def run_all_demos():
    """Run all available demos sequentially"""
    print("🚀 Running All Demo Scripts")
    print("=" * 60)
    
    for key, demo in AVAILABLE_DEMOS.items():
        print(f"\n▶️  Starting {demo['name']}...")
        print("-" * 40)
        
        try:
            demo['function']()
            print(f"✅ {demo['name']} completed successfully")
        except Exception as e:
            print(f"❌ {demo['name']} failed: {e}")
        
        print("-" * 40)
    
    print(f"\n🎉 All demos completed!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_key = sys.argv[1].lower()
        
        if demo_key == 'list':
            list_available_demos()
        elif demo_key == 'all':
            run_all_demos()
        elif demo_key in AVAILABLE_DEMOS:
            print(f"🎯 Running {AVAILABLE_DEMOS[demo_key]['name']}...")
            AVAILABLE_DEMOS[demo_key]['function']()
        else:
            print(f"❌ Unknown demo: {demo_key}")
            print(f"Available demos: {', '.join(AVAILABLE_DEMOS.keys())}")
            list_available_demos()
    else:
        list_available_demos()
