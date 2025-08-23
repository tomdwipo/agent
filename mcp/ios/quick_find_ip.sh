#!/bin/bash
# Quick iPhone IP Finder

echo "📱 Quick iPhone IP Address Finder"
echo "================================="

# Get your Mac's IP to determine network range
MAC_IP=$(route get default | grep interface | awk '{print $2}' | xargs ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

if [ -n "$MAC_IP" ]; then
    echo "✅ Your Mac's IP: $MAC_IP"
    
    # Extract network base (e.g., 192.168.1 from 192.168.1.6)
    NETWORK_BASE=$(echo $MAC_IP | sed 's/\.[0-9]*$//')
    echo "🌐 Network: ${NETWORK_BASE}.0/24"
    echo ""
    
    echo "🔍 Checking common iPhone IP ranges..."
    
    # Check common device IPs (faster than full scan)
    COMMON_IPS=(
        "${NETWORK_BASE}.100"
        "${NETWORK_BASE}.101" 
        "${NETWORK_BASE}.102"
        "${NETWORK_BASE}.103"
        "${NETWORK_BASE}.2"
        "${NETWORK_BASE}.3"
        "${NETWORK_BASE}.4"
        "${NETWORK_BASE}.5"
        "${NETWORK_BASE}.10"
        "${NETWORK_BASE}.11"
        "${NETWORK_BASE}.12"
        "${NETWORK_BASE}.20"
        "${NETWORK_BASE}.30"
    )
    
    FOUND_DEVICES=()
    
    for IP in "${COMMON_IPS[@]}"; do
        if ping -c 1 -W 1000 "$IP" >/dev/null 2>&1; then
            echo "   📱 Device found: $IP"
            FOUND_DEVICES+=("$IP")
            
            # Check if WebDriverAgent is running
            if curl -s --connect-timeout 2 "http://$IP:8100/status" >/dev/null 2>&1; then
                echo "   ✅ WebDriverAgent found at $IP:8100"
                echo ""
                echo "🎉 Ready to connect!"
                echo "   uv run main.py --device $IP:8100"
                echo ""
            fi
        fi
    done
    
    if [ ${#FOUND_DEVICES[@]} -eq 0 ]; then
        echo "⚠️  No devices found in common IP ranges"
        echo ""
        echo "📝 Manual methods:"
        echo "1. Check iPhone Settings → Wi-Fi → (i) → IP Address"
        echo "2. Or run: ./find_iphone_ip.py (comprehensive scan)"
        echo ""
    fi
else
    echo "❌ Could not determine network information"
fi

echo "📋 Common iPhone IP ranges to try:"
echo "   ${NETWORK_BASE}.100 - ${NETWORK_BASE}.110"
echo "   ${NETWORK_BASE}.2 - ${NETWORK_BASE}.10" 
echo ""
echo "🚀 Once you have the IP:"
echo "   uv run main.py --device YOUR_IPHONE_IP:8100"