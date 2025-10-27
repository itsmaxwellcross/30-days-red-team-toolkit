"""
Archive creator (ZIP, ISO)
"""
import os
import zipfile
import random
import string
from typing import Optional
from ..core.attachment import Attachment, AttachmentType
from ..config.settings import Settings

class ArchiveCreator:
    """Create weaponized archive files"""
    
    def __init__(self, output_dir: str):
        """
        Initialize archive creator
        
        Args:
            output_dir: Output directory
        """
        self.output_dir = output_dir
    
    def create_iso(self, payload_path: str,
                  output_name: str = "document.iso") -> Attachment:
        """
        Create ISO file containing payload
        
        Args:
            payload_path: Path to payload file
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Creating ISO file: {output_name}")
        print(f"[*] Payload: {payload_path}")
        print("\n[!] ISO creation requires external tools")
        print("[!] Options:")
        print("    Linux:   mkisofs -o output.iso payload.exe")
        print("    Windows: Use ImgBurn or similar tool")
        print("    Python:  pycdlib library (advanced)")
        
        command = f"mkisofs -o {output_path} {payload_path}"
        print(f"\n[*] Command to run:")
        print(f"    {command}")
        
        print("\n[*] Why ISO files work:")
        print("    • Often bypass email security filters")
        print("    • Users trust disk image formats")
        print("    • Can autorun on some systems")
        print("    • Hide true file extensions")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.ISO,
            output_path=output_path,
            payload=payload_path
        )
    
    def create_password_zip(self, file_path: str,
                           password: Optional[str] = None,
                           output_name: str = "document.zip") -> Attachment:
        """
        Create password-protected ZIP
        
        Args:
            file_path: File to archive
            password: ZIP password (generated if None)
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        if password is None:
            password = ''.join(random.choices(
                string.ascii_letters + string.digits, 
                k=Settings.DEFAULT_ZIP_PASSWORD_LENGTH
            ))
        
        print(f"[*] Creating password-protected ZIP: {output_name}")
        print(f"[*] Password: {password}")
        print(f"[*] File: {file_path}")
        
        print("\n[!] Python's zipfile module doesn't support AES encryption")
        print("[!] Options:")
        print("    1. Use pyminizip library:")
        print(f"       pyminizip.compress('{file_path}', '', '{output_path}', '{password}', 5)")
        print("    2. Use 7zip command:")
        print(f"       7z a -p{password} -mem=AES256 {output_path} {file_path}")
        print("    3. Use pyzipper library (AES support)")
        
        print("\n[*] Why password-protected ZIPs work:")
        print("    • Email security can't scan encrypted content")
        print("    • Password in email body seems legitimate")
        print("    • Users expect documents to be protected")
        print("    • Bypasses attachment filters")
        
        # Create basic ZIP (unencrypted for demo)
        try:
            with zipfile.ZipFile(output_path, 'w') as zipf:
                zipf.write(file_path, os.path.basename(file_path))
            print(f"\n[+] Basic ZIP created: {output_path}")
            print("[!] Note: Not encrypted - use tools above for encryption")
        except Exception as e:
            print(f"[-] Error creating ZIP: {e}")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.PASSWORD_ZIP,
            output_path=output_path,
            payload=file_path,
            password=password
        )
    
    def generate_zip_password(self, length: int = 8) -> str:
        """
        Generate random ZIP password
        
        Args:
            length: Password length
            
        Returns:
            Random password
        """
        # Mix of letters and digits for credibility
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))