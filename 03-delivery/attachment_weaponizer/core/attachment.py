"""
Attachment data model
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class AttachmentType(Enum):
    """Types of weaponized attachments"""
    MACRO_DOC = "macro_doc"
    MACRO_EXCEL = "macro_excel"
    ISO = "iso"
    PASSWORD_ZIP = "password_zip"
    HTML_SMUGGLING = "html_smuggling"
    LNK = "lnk"
    POLYGLOT = "polyglot"

@dataclass
class Attachment:
    """Represents a weaponized attachment"""
    
    name: str
    attachment_type: AttachmentType
    output_path: str
    payload: Optional[str] = None
    password: Optional[str] = None
    macro_code: Optional[str] = None
    payload_url: Optional[str] = None
    command: Optional[str] = None
    
    def get_summary(self) -> dict:
        """Get attachment summary"""
        return {
            'name': self.name,
            'type': self.attachment_type.value,
            'path': self.output_path,
            'has_payload': self.payload is not None,
            'has_password': self.password is not None
        }
    
    def get_delivery_instructions(self) -> str:
        """Get instructions for delivering this attachment"""
        instructions = {
            AttachmentType.MACRO_DOC: "Attach to email. Instruct user to enable macros.",
            AttachmentType.MACRO_EXCEL: "Attach to email. Instruct user to enable macros.",
            AttachmentType.ISO: "Attach to email. ISO files often bypass security.",
            AttachmentType.PASSWORD_ZIP: f"Attach ZIP. Include password in email: {self.password}",
            AttachmentType.HTML_SMUGGLING: "Attach HTML file. Payload downloads on open.",
            AttachmentType.LNK: "Attach LNK file. Executes command when opened.",
            AttachmentType.POLYGLOT: "Attach polyglot. Appears as one format, executes as another."
        }
        return instructions.get(self.attachment_type, "No specific instructions")