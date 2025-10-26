#!/usr/bin/env python3
import random
import string

class VBAObfuscator:
    """VBA obfuscation utilities"""
    
    @staticmethod
    def random_var(length=8):
        """Generate random variable name"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def create_auto_open_stubs(function_name):
        """Create AutoOpen and Document_Open stubs"""
        return f'''
Private Sub Document_Open()
    {function_name}
End Sub

Private Sub AutoOpen()
    {function_name}
End Sub
'''