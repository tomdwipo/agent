#!/usr/bin/env python3
"""
WiFi Debugging Setup for iPhone
This script helps you set up WiFi debugging for your iPhone with tidevice
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

def check_usb_devices():
    """Check for USB connected devices."""
    print("🔍 Checking for USB connected iPhone...")
    
    try:
        result = subprocess.run(['uv', 'run', 'tidevice', 'list'], 
                               capture_output=True, text=True, cwd=Path(__file__).parent)
        
        lines = result.stdout.strip().split('\n')
        devices = []
        
        for line in lines[1:]:  # Skip header
            if line.strip() and 'UDID' not in line:
                parts = line.split()
                if len(parts) >= 4:
                    devices.append({
                        'udid': parts[0],
                        'name': parts[2] if len(parts) > 2 else 'Unknown',
                        'version': parts[4] if len(parts) > 4 else 'Unknown',
                        'conn_type': parts[5] if len(parts) > 5 else 'USB'
                    })
        
        return devices
        
    except Exception as e:
        print_error(f"Error checking devices: {e}")
        return []

def enable_wifi_debugging(device_udid):
    """Enable WiFi debugging for the device."""
    print(f"🔧 Enabling WiFi debugging for device {device_udid}...")
    
    try:
        # Try to enable wireless debugging using tidevice
        result = subprocess.run(['uv', 'run', 'tidevice', '-u', device_udid, 'pair'], 
                               capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print_status("WiFi debugging pairing initiated")
            return True
        else:
            print_warning("Pairing command completed with warnings")
            print("Output:", result.stdout)
            print("Errors:", result.stderr)
            return True  # Continue anyway
            
    except Exception as e:
        print_error(f"Error enabling WiFi debugging: {e}")
        return False

def get_device_ip():
    """Help user find their iPhone's IP address."""
    print("\n📱 Finding Your iPhone's IP Address")
    print("=" * 50)
    
    print("Method 1: Check iPhone Settings")
    print("1. Open Settings app on iPhone")
    print("2. Go to: Wi-Fi")
    print("3. Tap the (i) next to your WiFi network")
    print("4. Look for 'IP Address'")
    print("")
    
    print("Method 2: Use Network Scanner")
    print("We can scan your network for the iPhone...")
    
    try:
        # Use our existing IP finder
        print("🔍 Scanning network for iPhone...")
        result = subprocess.run(['python3', 'find_iphone_ip.py'], 
                               capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("Scan results:")
            print(result.stdout)
        else:
            print_warning("Network scan not available")
            
    except FileNotFoundError:
        print_warning("Network scanner not found")
    except Exception as e:
        print_warning(f"Network scan failed: {e}")
    
    # Ask user for IP
    print("\n📝 Enter Your iPhone's IP Address:")
    ip = input("iPhone IP (e.g., 192.168.1.100): ").strip()
    
    if ip:
        return ip
    else:
        print_warning("No IP provided")
        return None

def test_wifi_connection(device_ip):
    """Test WiFi connection to the iPhone."""
    print(f"\n🧪 Testing WiFi connection to {device_ip}...")
    
    try:
        # First, try to detect the device
        result = subprocess.run(['uv', 'run', 'tidevice', '-u', device_ip, 'info'], 
                               capture_output=True, text=True, timeout=10,
                               cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print_status(f"WiFi connection to {device_ip} successful!")
            print("Device info:")
            print(result.stdout)
            return True
        else:
            print_error("WiFi connection failed")
            print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Connection timeout - device not reachable via WiFi")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False

def start_wifi_wdaproxy(device_ip):
    """Start WebDriverAgent proxy via WiFi."""
    print(f"\n🚀 Starting WebDriverAgent via WiFi ({device_ip})...")
    
    try:
        cmd = ['uv', 'run', 'tidevice', '-u', device_ip, 'wdaproxy', 
               '-B', 'com.facebook.WebDriverAgentRunner.xctrunner']
        
        print("💡 Starting WebDriverAgent proxy...")
        print("🔗 WebDriverAgent will be available at: http://localhost:8100")
        print("⏹️  Press Ctrl+C to stop")
        print("")
        
        # Run the command
        subprocess.run(cmd, cwd=Path(__file__).parent)
        
    except KeyboardInterrupt:
        print("\n⏹️  WebDriverAgent stopped by user")
    except Exception as e:
        print_error(f"Failed to start WebDriverAgent: {e}")

def main():
    print("📱 iPhone WiFi Debugging Setup")
    print("===============================")
    print("This script helps you set up wireless debugging for your iPhone")
    print("")
    
    # Step 1: Check for USB devices first
    print("📋 Step 1: USB Connection Required")
    print("=" * 40)
    print("WiFi debugging must be enabled while connected via USB first")
    print("")
    
    devices = check_usb_devices()
    if not devices:
        print_error("No iPhone found via USB!")
        print("\n📋 Required steps:")
        print("1. Connect iPhone via USB cable")
        print("2. Unlock iPhone")
        print("3. Tap 'Trust This Computer'")
        print("4. Run this script again")
        return False
    
    device = devices[0]
    print_status(f"iPhone found: {device['name']} (iOS {device['version']})")
    print_info(f"Device UDID: {device['udid']}")
    
    # Step 2: Enable WiFi debugging
    print("\n📋 Step 2: Enable WiFi Debugging")
    print("=" * 40)
    
    if not enable_wifi_debugging(device['udid']):
        print_error("Failed to enable WiFi debugging")
        return False
    
    print_info("WiFi debugging should now be enabled")
    print("💡 You can now disconnect the USB cable")
    
    # Step 3: Get iPhone IP
    print("\n📋 Step 3: Get iPhone IP Address")
    print("=" * 40)
    
    device_ip = get_device_ip()
    if not device_ip:
        return False
    
    # Step 4: Test WiFi connection
    print(f"\n📋 Step 4: Test WiFi Connection")
    print("=" * 40)
    
    if not test_wifi_connection(device_ip):
        print_error("WiFi connection failed")
        print("\n🛠️  Troubleshooting:")
        print("1. Make sure iPhone and Mac are on same WiFi network")
        print("2. Check iPhone IP address is correct")
        print("3. Try reconnecting iPhone via USB and enable pairing again")
        print("4. Restart both iPhone and Mac WiFi")
        return False
    
    # Step 5: Start WebDriverAgent
    print(f"\n📋 Step 5: Start WebDriverAgent")
    print("=" * 40)
    
    print("🚀 Ready to start WebDriverAgent via WiFi!")
    answer = input("Start WebDriverAgent now? (y/n): ").strip().lower()
    
    if answer in ['y', 'yes']:
        start_wifi_wdaproxy(device_ip)
    else:
        print("\n💡 To start WebDriverAgent later, use:")
        print(f"   uv run tidevice -u {device_ip} wdaproxy -B com.facebook.WebDriverAgentRunner.xctrunner")
        print("\n🔗 Then connect iOS MCP with:")
        print(f"   uv run main.py --device {device_ip}:8100")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)