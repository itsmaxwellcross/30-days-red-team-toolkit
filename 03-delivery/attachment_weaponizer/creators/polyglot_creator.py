"""
Polyglot file creator
"""
import os
from ..core.attachment import Attachment, AttachmentType

class PolyglotCreator:
    """Create polyglot files (valid as multiple formats)"""
    
    def __init__(self, output_dir: str):
        """
        Initialize polyglot creator
        
        Args:
            output_dir: Output directory
        """
        self.output_dir = output_dir
    
    def create_polyglot(self, payload_path: str,
                       output_name: str = "document.pdf",
                       cover_format: str = "pdf") -> Attachment:
        """
        Create polyglot file
        
        Args:
            payload_path: Path to executable payload
            output_name: Output filename
            cover_format: Format to masquerade as
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Creating polyglot file: {output_name}")
        print(f"[*] Payload: {payload_path}")
        print(f"[*] Cover format: {cover_format}")
        
        print("\n[!] Polyglot creation is advanced and complex")
        print("[!] Requires careful binary manipulation")
        
        print("\n[*] Polyglot techniques:")
        print("    • PDF/EXE polyglot - Valid as both")
        print("    • ZIP/JAR polyglot - Archive and executable")
        print("    • Image/EXE polyglot - Appears as image")
        print("    • HTML/EXE polyglot - Browser and executable")
        
        print("\n[*] How polyglots work:")
        print("    • Different parsers read files differently")
        print("    • PDF ignores data after %%EOF")
        print("    • ZIP reads from end of file")
        print("    • PE executables have specific headers")
        print("    • Craft file valid for multiple parsers")
        
        print("\n[*] Example: PDF/EXE polyglot structure:")
        print("    [PDF header]")
        print("    [PDF content]")
        print("    %%EOF")
        print("    [Padding]")
        print("    [PE/EXE executable]")
        
        print("\n[*] Tools for polyglot creation:")
        print("    • Mangle - Polyglot generator")
        print("    • AngeCryption - Crypto polyglots")
        print("    • Corkami - File format research")
        
        print("\n[!] Note: Very technique-specific")
        print("[!] Requires deep understanding of file formats")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.POLYGLOT,
            output_path=output_path,
            payload=payload_path
        )
    
    def explain_pdf_exe_polyglot(self):
        """Explain PDF/EXE polyglot technique"""
        explanation = """
PDF/EXE Polyglot Structure:

1. Start with valid PDF:
   %PDF-1.4
   [PDF objects and content]
   %%EOF

2. PDF parsers stop at %%EOF, ignore everything after

3. After %%EOF, append executable:
   [Padding to align executable]
   [Full Windows PE executable]

4. When opened as PDF: Shows PDF content
   When executed: Runs the executable

5. File appears as document.pdf but can execute

Key considerations:
- PDF readers ignore post-EOF content
- Windows checks for PE header (MZ signature)
- File extension determines default action
- Email filters may only check first format

This is why file inspection is critical for security.
"""
        print(explanation)