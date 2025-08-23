#!/usr/bin/env python3
"""
iPhone IP Address Discovery Tool
Finds your iPhone's IP address on the local network for WiFi connections.
"""

import subprocess
import socket
import requests
import json
import re
from pathlib import Path
import sys

def print_status(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def get_local_network_info():
    """Get local network information."""
    try:
        # Get local IP and network
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Extract network range
        ip_parts = local_ip.split('.')
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        return local_ip, network
    except Exception as e:
        print_error(f"Failed to get network info: {e}")
        return None, None

def scan_network_for_devices(network):
    """Scan network for iOS devices."""
    print(f"🔍 Scanning network {network} for devices...")
    
    try:
        # Use nmap to scan for devices
        result = subprocess.run([
            'nmap', '-sn', network
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            devices = []
            lines = result.stdout.split('\n')
            current_ip = None
            
            for line in lines:
                # Look for IP addresses
                ip_match = re.search(r'Nmap scan report for (\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    current_ip = ip_match.group(1)
                
                # Look for device info that might indicate iPhone
                if current_ip and any(keyword in line.lower() for keyword in ['apple', 'iphone', 'ios']):
                    devices.append(current_ip)
                elif current_ip and 'Host is up' in line:
                    # Add all responsive devices for manual checking
                    devices.append(current_ip)
            
            return devices
        else:
            print_warning("nmap scan failed")
            return []
            
    except subprocess.TimeoutExpired:
        print_warning("Network scan timed out")
        return []
    except Exception as e:
        print_warning(f"Network scan failed: {e}")
        return []

def check_webdriveragent_port(ip, port=8100):
    """Check if WebDriverAgent is running on specific IP and port."""
    try:
        response = requests.get(f"http://{ip}:{port}/status", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return True, data
        return False, None
    except:
        return False, None

def find_iphone_with_webdriveragent(devices):
    """Find iPhone by checking for WebDriverAgent on common ports."""
    print("🔍 Checking devices for WebDriverAgent...")
    
    possible_iphones = []
    ports_to_check = [8100, 8200, 9100]
    
    for ip in devices:
        print(f"   Checking {ip}...")
        
        for port in ports_to_check:
            is_wda, data = check_webdriveragent_port(ip, port)
            if is_wda:
                device_info = {
                    'ip': ip,
                    'port': port,
                    'data': data
                }
                
                # Check if it's actually an iOS device
                if data and 'ios' in data:
                    device_info['confirmed_ios'] = True
                    device_info['ios_info'] = data['ios']
                else:
                    device_info['confirmed_ios'] = False
                
                possible_iphones.append(device_info)
                print_status(f"Found WebDriverAgent at {ip}:{port}")
                break
    
    return possible_iphones

def get_arp_table_devices():
    """Get devices from ARP table (alternative method)."""
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        if result.returncode == 0:
            devices = []
            for line in result.stdout.split('\n'):
                # Extract IP addresses from ARP table
                ip_match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', line)
                if ip_match:
                    ip = ip_match.group(1)
                    if not ip.endswith('.1'):  # Skip router
                        devices.append(ip)
            return devices
        return []
    except:
        return []

def manual_ip_input():
    """Allow manual IP input if auto-detection fails."""
    print("\n📝 Manual IP Address Input")
    print("==========================")
    print("If you know your iPhone's IP address, enter it here.")
    print("You can find it on your iPhone:")
    print("Settings → Wi-Fi → (i) next to your network → IP Address")
    print("")
    
    while True:
        ip = input("Enter iPhone IP address (or 'skip'): ").strip()
        
        if ip.lower() == 'skip':
            return None
        
        # Validate IP format
        try:
            socket.inet_aton(ip)
            return ip
        except socket.error:
            print_error("Invalid IP address format. Please try again.")

def test_connection(ip, port=8100):
    """Test iOS MCP connection to the device."""
    print(f"\n🧪 Testing iOS MCP connection to {ip}:{port}...")
    
    try:
        # Test connection using our iOS MCP code
        test_cmd = [
            'uv', 'run', 'python', '-c', f'''
import sys
sys.path.append("src")
from ios import IOSDevice

print("Testing connection to {ip}:{port}...")
try:
    device = IOSDevice(device="{ip}:{port}", auto_setup=False)
    info = device.get_device_info()
    print("✅ Connection successful!")
    print(f"📊 Device info: {{info}}")
    print("🎉 Your iPhone is ready for iOS MCP automation!")
except Exception as e:
    print(f"❌ Connection failed: {{e}}")
    print("💡 Make sure WebDriverAgent is running on your iPhone")
'''
        ]
        
        subprocess.run(test_cmd, cwd=Path(__file__).parent)
        
    except Exception as e:
        print_error(f"Test failed: {e}")

def main():
    print("📱 iPhone IP Address Discovery Tool")
    print("==================================")
    print("This tool helps you find your iPhone's IP address for WiFi connections.\n")
    
    # Method 1: Get network info
    local_ip, network = get_local_network_info()
    if local_ip:
        print_status(f"Your Mac's IP: {local_ip}")
        print_info(f"Scanning network: {network}")
    else:
        print_error("Could not determine network information")
        return
    
    # Method 2: Scan network
    print("\n🔍 Method 1: Network Scanning")
    devices = scan_network_for_devices(network)
    
    if not devices:
        print_warning("No devices found via network scan")
        # Fallback to ARP table
        print("\n🔍 Method 2: ARP Table")
        devices = get_arp_table_devices()
        if devices:
            print_status(f"Found {len(devices)} devices in ARP table")
        else:
            print_warning("No devices found in ARP table")
    else:
        print_status(f"Found {len(devices)} responsive devices")
    
    # Method 3: Check for WebDriverAgent
    iphones = []
    if devices:
        iphones = find_iphone_with_webdriveragent(devices)
    
    # Display results
    if iphones:
        print(f"\n🎉 Found {len(iphones)} device(s) with WebDriverAgent:")
        print("=" * 50)
        
        for i, device in enumerate(iphones, 1):
            ip = device['ip']
            port = device['port']
            print(f"\n📱 Device {i}: {ip}:{port}")
            
            if device['confirmed_ios']:
                ios_info = device['ios_info']
                print(f"   ✅ Confirmed iOS Device")
                print(f"   📱 Name: {ios_info.get('name', 'Unknown')}")
                print(f"   📱 iOS Version: {ios_info.get('version', 'Unknown')}")
                print(f"   📱 Model: {ios_info.get('model', 'Unknown')}")
            else:
                print(f"   ⚠️  WebDriverAgent found (may not be iOS)")
            
            print(f"\n🚀 To connect:")
            print(f"   uv run main.py --device {ip}:{port}")
        
        # Test the first confirmed iOS device
        confirmed_ios = [d for d in iphones if d['confirmed_ios']]
        if confirmed_ios:
            device = confirmed_ios[0]
            test_connection(device['ip'], device['port'])
        elif iphones:
            device = iphones[0]
            test_connection(device['ip'], device['port'])
            
    else:
        print("\n⚠️  No devices with WebDriverAgent found automatically")
        print("\nPossible reasons:")
        print("• WebDriverAgent is not running on your iPhone")
        print("• iPhone is not on the same WiFi network")
        print("• Firewall is blocking the connection")
        
        # Offer manual input
        manual_ip = manual_ip_input()
        if manual_ip:
            print(f"\n🧪 Testing manual IP: {manual_ip}")
            test_connection(manual_ip)
        
        print("\n📋 Manual Setup Instructions:")
        print("1. Make sure your iPhone and Mac are on the same WiFi")
        print("2. Start WebDriverAgent on your iPhone:")
        print("   • Use tidevice: tidevice wdaproxy")
        print("   • Or build WebDriverAgentRunner in Xcode")
        print("3. Find IP on iPhone: Settings → Wi-Fi → (i) → IP Address")
        print("4. Connect: uv run main.py --device YOUR_IP:8100")

if __name__ == "__main__":
    main()