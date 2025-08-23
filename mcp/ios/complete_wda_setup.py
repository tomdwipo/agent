#!/usr/bin/env python3
"""
Complete WebDriverAgent Setup for Real iPhone
Following project specifications for iOS device configuration workflow
"""

import subprocess
import time
import sys
from pathlib import Path
import json

def print_status(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def check_device_connection():
    """Check if iPhone is connected via USB."""
    print("🔍 Checking for connected iPhone...")
    
    try:
        # Use Apple's devicectl (more reliable than tidevice for detection)
        result = subprocess.run(['xcrun', 'devicectl', 'list', 'devices'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            devices = []
            
            for line in lines[2:]:  # Skip header lines
                if 'iPhone' in line and 'connected' in line:
                    parts = line.split()
                    device_name = parts[0] + ' ' + parts[1] if len(parts) > 1 else parts[0]
                    device_id = None
                    
                    # Extract device ID
                    for part in parts:
                        if '-' in part and len(part) > 30:  # UUID format
                            device_id = part
                            break
                    
                    if device_id:
                        devices.append({
                            'name': device_name,
                            'id': device_id
                        })
            
            return devices
        else:
            print_error("Failed to check devices")
            return []
            
    except Exception as e:
        print_error(f"Error checking devices: {e}")
        return []

def check_webdriveragent_built():
    """Check if WebDriverAgent is already built and ready."""
    wda_path = Path("WebDriverAgent")
    
    if not wda_path.exists():
        return False, "WebDriverAgent not found"
    
    # Check if there are built products
    derived_data_paths = [
        Path.home() / "Library/Developer/Xcode/DerivedData",
        wda_path / "DerivedData"
    ]
    
    for path in derived_data_paths:
        if path.exists():
            wda_folders = list(path.glob("WebDriverAgent-*"))
            if wda_folders:
                return True, f"WebDriverAgent built at {wda_folders[0]}"
    
    return False, "WebDriverAgent not built yet"

def start_webdriveragent_usb():
    """Start WebDriverAgent via USB using tidevice."""
    print("🚀 Starting WebDriverAgent via USB...")
    
    try:
        # Method 1: Use tidevice
        print("📱 Starting WebDriverAgent with tidevice...")
        cmd = ['uv', 'run', 'tidevice', 'wdaproxy', '-B', 'com.facebook.WebDriverAgentRunner.xctrunner']
        
        print("⏳ Starting WebDriverAgent proxy...")
        print("💡 Keep this terminal open while using iOS MCP!")
        print("")
        
        # Start the process in background but show output
        process = subprocess.Popen(cmd, cwd=Path(__file__).parent)
        
        # Give it time to start
        time.sleep(3)
        
        # Check if it's running
        try:
            test_result = subprocess.run(['curl', '-s', 'http://localhost:8100/status'], 
                                       capture_output=True, text=True, timeout=5)
            
            if test_result.returncode == 0:
                print_status("WebDriverAgent is running!")
                print_info("WebDriverAgent available at: http://localhost:8100")
                return True, process
            else:
                print_warning("WebDriverAgent may still be starting...")
                return True, process
                
        except subprocess.TimeoutExpired:
            print_warning("Connection test timed out, but WebDriverAgent may be starting")
            return True, process
            
    except Exception as e:
        print_error(f"Failed to start WebDriverAgent: {e}")
        return False, None

def build_webdriveragent_xcode(device_id):
    """Build WebDriverAgent using Xcode command line."""
    print("🔨 Building WebDriverAgent with Xcode...")
    
    wda_path = Path("WebDriverAgent")
    if not wda_path.exists():
        print_error("WebDriverAgent directory not found")
        return False
    
    try:
        # Build command
        cmd = [
            'xcodebuild', 'build-for-testing',
            '-project', 'WebDriverAgent.xcodeproj',
            '-scheme', 'WebDriverAgentRunner',
            '-destination', f'id={device_id}',
            '-allowProvisioningUpdates'
        ]
        
        print(f"⏳ Building for device {device_id}...")
        print("💡 This may take a few minutes...")
        
        result = subprocess.run(cmd, cwd=wda_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("WebDriverAgent built successfully!")
            return True
        else:
            print_error("Build failed!")
            print("Build output:")
            print(result.stderr)
            
            if "Signing for" in result.stderr and "requires a development team" in result.stderr:
                print("")
                print_warning("Signing issue detected!")
                print("📝 Please configure signing in Xcode:")
                print("1. Open WebDriverAgent.xcodeproj in Xcode")
                print("2. Select WebDriverAgentRunner target")
                print("3. Go to Signing & Capabilities")
                print("4. Select your Apple Developer Team")
                print("5. Change Bundle Identifier to: com.yourname.WebDriverAgentRunner")
            
            return False
            
    except Exception as e:
        print_error(f"Build error: {e}")
        return False

def run_webdriveragent_test(device_id):
    """Run WebDriverAgent test to start the server."""
    print("🧪 Running WebDriverAgent test to start server...")
    
    wda_path = Path("WebDriverAgent")
    
    try:
        cmd = [
            'xcodebuild', 'test-without-building',
            '-project', 'WebDriverAgent.xcodeproj',
            '-scheme', 'WebDriverAgentRunner',
            '-destination', f'id={device_id}',
            '-allowProvisioningUpdates'
        ]
        
        print("🚀 Starting WebDriverAgent server on device...")
        print("💡 Keep this terminal open!")
        print("")
        
        # Run the test (this keeps WebDriverAgent running)
        subprocess.run(cmd, cwd=wda_path)
        
    except KeyboardInterrupt:
        print("\n⏹️  WebDriverAgent stopped by user")
    except Exception as e:
        print_error(f"Error running WebDriverAgent: {e}")

def test_ios_mcp_connection():
    """Test iOS MCP connection to WebDriverAgent."""
    print("\n🧪 Testing iOS MCP connection...")
    
    try:
        # Test the connection
        test_cmd = ['uv', 'run', 'python', '-c', '''
import sys
sys.path.append("src")
from ios import IOSDevice

print("Testing USB connection...")
try:
    device = IOSDevice(usb=True, auto_setup=False)
    info = device.get_device_info()
    print("✅ iOS MCP connection successful!")
    print(f"📊 Device info: {info}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("💡 Make sure WebDriverAgent is running on your iPhone")
''']
        
        subprocess.run(test_cmd, cwd=Path(__file__).parent)
        
    except Exception as e:
        print_error(f"Test failed: {e}")

def main():
    print("📱 Complete WebDriverAgent Setup for Real iPhone")
    print("===============================================")
    print("Following project specifications for iOS device configuration")
    print("")
    
    # Step 1: Check device connection
    devices = check_device_connection()
    if not devices:
        print_error("No iPhone found!")
        print("📋 Please ensure:")
        print("1. iPhone is connected via USB")
        print("2. iPhone is unlocked and trusted")
        print("3. Developer Mode is enabled (iOS 16+)")
        return False
    
    device = devices[0]
    print_status(f"iPhone found: {device['name']}")
    print_info(f"Device ID: {device['id']}")
    
    # Step 2: Check if WebDriverAgent exists
    if not Path("WebDriverAgent").exists():
        print_warning("WebDriverAgent not found. Please run first:")
        print("git clone https://github.com/appium/WebDriverAgent.git")
        return False
    
    # Step 3: Try USB connection first (easiest method)
    print("\n🔄 Method 1: USB Connection via tidevice")
    print("=" * 50)
    
    success, process = start_webdriveragent_usb()
    if success:
        print_status("WebDriverAgent started via USB!")
        print("\n🚀 Ready to use iOS MCP:")
        print(f"   uv run main.py --usb --device {device['id']}")
        print("   or")
        print("   uv run main.py --usb")
        print("")
        
        # Test connection
        time.sleep(2)
        test_ios_mcp_connection()
        
        print("\n💡 WebDriverAgent is running. Keep this terminal open!")
        print("🔗 WebDriverAgent URL: http://localhost:8100")
        
        # Keep running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n⏹️  Stopped by user")
        
        return True
    
    # Step 4: Fallback to Xcode build method
    print("\n🔄 Method 2: Xcode Build & Run")
    print("=" * 50)
    
    # Check if WebDriverAgent is built
    built, build_info = check_webdriveragent_built()
    if not built:
        print_warning("WebDriverAgent needs to be built")
        
        # Try to build it
        if not build_webdriveragent_xcode(device['id']):
            print_error("Failed to build WebDriverAgent")
            print("\n📝 Manual steps:")
            print("1. Open WebDriverAgent.xcodeproj in Xcode")
            print("2. Configure signing (select development team)")
            print("3. Build and run WebDriverAgentRunner target")
            return False
    else:
        print_status(f"WebDriverAgent already built: {build_info}")
    
    # Run WebDriverAgent test
    print_info("Starting WebDriverAgent server...")
    run_webdriveragent_test(device['id'])
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)