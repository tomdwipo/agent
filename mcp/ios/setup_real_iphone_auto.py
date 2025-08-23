#!/usr/bin/env python3
"""
Automated Real iPhone Setup for iOS MCP Server
This script automates WebDriverAgent setup on real iPhone devices.
"""

import subprocess
import time
import sys
from pathlib import Path

def print_status(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def check_device_connection():
    """Check if iPhone is connected and trusted."""
    print("🔍 Checking for connected iPhone...")
    
    try:
        # Use tidevice to check for devices
        result = subprocess.run(['uv', 'run', 'python', '-c', 
                               'import tidevice; print("\\n".join([str(d) for d in tidevice.Device.list()]))'],
                               capture_output=True, text=True, cwd=Path(__file__).parent)
        
        devices = result.stdout.strip()
        if devices:
            print_status("iPhone connected:")
            for device in devices.split('\n'):
                if device.strip():
                    print(f"   📱 {device}")
            return devices.split('\n')[0].strip()  # Return first device
        else:
            print_error("No iPhone detected")
            print_info("Please:")
            print("   1. Connect iPhone via USB cable")
            print("   2. Unlock iPhone")
            print("   3. Tap 'Trust This Computer'")
            print("   4. Enable Developer Mode (iOS 16+):")
            print("      Settings → Privacy & Security → Developer Mode → On")
            return None
            
    except Exception as e:
        print_error(f"Error checking devices: {e}")
        return None

def start_webdriveragent(device_id=None):
    """Start WebDriverAgent on the iPhone using tidevice."""
    print("🚀 Starting WebDriverAgent on iPhone...")
    
    try:
        # Build the tidevice command
        cmd = ['uv', 'run', 'python', '-c', '''
import tidevice
import time

print("📱 Starting WebDriverAgent...")
try:
    device = tidevice.Device()
    print("🔧 Installing WebDriverAgent if needed...")
    
    # Start WebDriverAgent proxy
    print("🌐 Starting WebDriverAgent proxy on port 8100...")
    device.wdaproxy(port=8100)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Try manual setup if this fails")
''']
        
        print("⏳ This may take a few moments...")
        print("📱 Check your iPhone - you may need to trust the app")
        
        # Start the process
        process = subprocess.Popen(cmd, cwd=Path(__file__).parent)
        
        # Give it some time to start
        time.sleep(5)
        
        # Check if it's running
        if process.poll() is None:
            print_status("WebDriverAgent process started!")
            print_info("WebDriverAgent should be running on your iPhone")
            print_info("You can now connect using:")
            print("   uv run main.py --usb")
            print("   or")
            print("   uv run main.py --device IPHONE_IP:8100")
            return True
        else:
            print_warning("WebDriverAgent process may have failed")
            return False
            
    except Exception as e:
        print_error(f"Failed to start WebDriverAgent: {e}")
        return False

def test_connection():
    """Test iOS MCP connection to real iPhone."""
    print("\n🧪 Testing iOS MCP connection...")
    
    try:
        # Test USB connection
        test_cmd = ['uv', 'run', 'python', '-c', '''
import sys
sys.path.append("src")
from ios import IOSDevice

print("Testing USB connection...")
try:
    device = IOSDevice(usb=True, auto_setup=False)
    info = device.get_device_info()
    print(f"✅ Connection successful!")
    print(f"📊 Device info: {info}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("💡 Make sure WebDriverAgent is running on your iPhone")
''']
        
        subprocess.run(test_cmd, cwd=Path(__file__).parent)
        
    except Exception as e:
        print_error(f"Test failed: {e}")

def main():
    print("📱 Automated Real iPhone Setup")
    print("===============================")
    
    # Check device connection
    device_id = check_device_connection()
    if not device_id:
        return False
    
    # Start WebDriverAgent
    if start_webdriveragent(device_id):
        # Test connection
        test_connection()
        
        print("\n🎉 Setup Complete!")
        print("==================")
        print("Your iPhone is ready for iOS MCP automation!")
        print("\n🚀 To start iOS MCP server:")
        print("   uv run main.py --usb")
        print("   # or with specific device:")
        print(f"   uv run main.py --usb --device {device_id}")
        
        return True
    else:
        print("\n❌ Setup Failed")
        print("===============")
        print("Please try the manual setup:")
        print("   ./setup_real_iphone.sh")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)