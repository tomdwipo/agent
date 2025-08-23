#!/usr/bin/env python3
"""
iOS MCP Setup Verification Script

This script checks your iOS MCP setup and provides guidance for fixing issues.
"""

import sys
import os
import subprocess
import socket
import requests
import platform
from pathlib import Path


def print_status(message):
    print(f"✅ {message}")


def print_warning(message):
    print(f"⚠️  {message}")


def print_error(message):
    print(f"❌ {message}")


def print_info(message):
    print(f"ℹ️  {message}")


def check_system_requirements():
    """Check basic system requirements."""
    print("🔍 Checking system requirements...")
    
    # Check OS
    if platform.system() != "Darwin":
        print_error("This script requires macOS for iOS device automation")
        return False
    
    print_status("Running on macOS")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print_error(f"Python 3.10+ required, found {python_version.major}.{python_version.minor}")
        return False
    
    print_status(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} is compatible")
    
    return True


def check_xcode():
    """Check if Xcode and command line tools are installed."""
    print("\n🔍 Checking Xcode installation...")
    
    try:
        subprocess.run(["xcodebuild", "-version"], 
                      check=True, capture_output=True, text=True)
        print_status("Xcode and command line tools are installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Xcode is not installed or command line tools are missing")
        print_info("Please install Xcode from the App Store and run:")
        print_info("  xcode-select --install")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking Python dependencies...")
    
    required_modules = ['wda', 'tidevice', 'PIL', 'mcp']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print_status(f"{module} is installed")
        except ImportError:
            missing_modules.append(module)
            print_warning(f"{module} is missing")
    
    if missing_modules:
        print_info("To install missing dependencies:")
        print_info("  uv sync  # or pip install -r requirements.txt")
        return False
    
    return True


def check_devices():
    """Check for available iOS devices and simulators."""
    print("\n🔍 Checking for iOS devices...")
    
    devices_found = False
    
    # Check for physical devices using tidevice
    try:
        import tidevice
        devices = tidevice.Device.list()
        if devices:
            print_status("Physical iOS devices found:")
            for device in devices:
                print(f"  📱 {device}")
            devices_found = True
        else:
            print_warning("No physical iOS devices found")
    except Exception as e:
        print_warning(f"Could not check physical devices: {e}")
    
    # Check for iOS Simulators
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "--json"],
            capture_output=True, text=True, check=True
        )
        
        import json
        data = json.loads(result.stdout)
        
        booted_simulators = []
        for runtime, devices in data.get("devices", {}).items():
            for device in devices:
                if device.get("state") == "Booted":
                    booted_simulators.append(f"{device['name']} ({runtime})")
        
        if booted_simulators:
            print_status("Running iOS Simulators found:")
            for sim in booted_simulators:
                print(f"  📲 {sim}")
            devices_found = True
        else:
            print_warning("No running iOS Simulators found")
            print_info("You can start a simulator from Xcode or by running:")
            print_info("  open -a Simulator")
    
    except Exception as e:
        print_warning(f"Could not check simulators: {e}")
    
    return devices_found


def check_webdriveragent(ports=[8100, 4723, 8200, 9100]):
    """Check if WebDriverAgent is running on common ports."""
    print("\n🔍 Checking WebDriverAgent status...")
    
    for port in ports:
        try:
            response = requests.get(f"http://localhost:{port}/status", timeout=3)
            if response.status_code == 200:
                print_status(f"WebDriverAgent is running on port {port}")
                data = response.json()
                if 'ios' in data:
                    ios_info = data['ios']
                    print_info(f"  Device: {ios_info.get('name', 'Unknown')}")
                    print_info(f"  iOS Version: {ios_info.get('version', 'Unknown')}")
                return port
        except requests.exceptions.RequestException:
            continue
    
    print_warning("WebDriverAgent is not running on any common ports")
    return None


def test_ios_connection():
    """Test the iOS MCP connection."""
    print("\n🔍 Testing iOS MCP connection...")
    
    # Add src to path for imports
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir / "src"))
    
    try:
        # Direct import to avoid circular dependencies
        from ios import IOSDevice
        
        connection_methods = [
            ("simulator", {"simulator": True, "auto_setup": False}),
            ("usb", {"usb": True, "auto_setup": False}),
            ("localhost", {"auto_setup": False}),
        ]
        
        for method_name, kwargs in connection_methods:
            try:
                print_info(f"Trying {method_name} connection...")
                
                # Create device instance with timeout handling
                device = IOSDevice(**kwargs)
                info = device.get_device_info()
                
                if info.get('connected'):
                    print_status(f"SUCCESS: Connected via {method_name}")
                    print_info(f"Connection URL: {info.get('connection_url')}")
                    wda_status = info.get('wda_status', {})
                    if isinstance(wda_status, dict):
                        print_info(f"WDA Status: {wda_status.get('message', 'Ready')}")
                    return True
                    
            except Exception as e:
                print_warning(f"{method_name} connection failed: {e}")
        
        print_error("All connection methods failed")
        return False
        
    except ImportError as e:
        print_error(f"Could not import iOS module: {e}")
        print_info("Make sure you're running this script from the iOS MCP directory")
        return False
    except Exception as e:
        print_error(f"Unexpected error during connection test: {e}")
        return False


def print_setup_instructions():
    """Print setup instructions based on the findings."""
    print("\n📋 Setup Instructions")
    print("====================")
    
    print("\n1️⃣  Start WebDriverAgent:")
    print("   For physical devices:")
    print("     uv run python -c \"import tidevice; tidevice.Device().wdaproxy()\"")
    print("\n   For simulators:")
    print("     # Option A: Using Appium (Recommended)")
    print("     npm install -g appium")
    print("     appium driver install xcuitest")
    print("     appium --port 4723")
    print("\n     # Option B: Manual WebDriverAgent")
    print("     git clone https://github.com/appium/WebDriverAgent.git")
    print("     cd WebDriverAgent")
    print("     # Open WebDriverAgent.xcodeproj in Xcode")
    print("     # Set development team and build WebDriverAgentRunner target")
    
    print("\n2️⃣  Start iOS MCP Server:")
    print("     # For simulator:")
    print("     uv run main.py --simulator")
    print("\n     # For USB device:")
    print("     uv run main.py --usb")
    print("\n     # For network device:")
    print("     uv run main.py --device 192.168.1.100:8100")
    
    print("\n3️⃣  Troubleshooting:")
    print("     • Ensure device is unlocked and trusted")
    print("     • Check Developer Mode is enabled (iOS 16+)")
    print("     • Verify WebDriverAgent app is installed on device")
    print("     • See README.md for detailed instructions")


def main():
    """Main verification function."""
    print("🚀 iOS MCP Setup Verification")
    print("=============================")
    
    all_good = True
    
    # Check system requirements
    if not check_system_requirements():
        all_good = False
    
    # Check Xcode
    if not check_xcode():
        all_good = False
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
    
    # Check devices
    devices_available = check_devices()
    if not devices_available:
        print_warning("No iOS devices or simulators found, but this is not blocking")
    
    # Check WebDriverAgent
    wda_port = check_webdriveragent()
    if not wda_port:
        all_good = False
    
    # Test connection if everything looks good
    if all_good and wda_port:
        connection_success = test_ios_connection()
        if connection_success:
            print("\n🎉 iOS MCP setup verification completed successfully!")
            print_status("Your iOS MCP server should work correctly")
        else:
            print_warning("Connection test failed, but basic setup looks correct")
    else:
        print_warning("Setup verification found issues")
    
    # Always print instructions
    print_setup_instructions()
    
    print(f"\n✅ Verification complete!")
    return all_good


if __name__ == "__main__":
    sys.exit(0 if main() else 1)