#!/usr/bin/env python3
import re
import random

class StringObfuscator:
    """Obfuscate strings and commands"""
    
    def obfuscate_strings(self, code):
        """Break up strings to avoid signature detection"""
        strings = re.findall(r'"([^"]+)"', code)
        
        for s in strings:
            if len(s) > 10:  # Only obfuscate longer strings
                chunks = [s[i:i+3] for i in range(0, len(s), 3)]
                concatenated = '"' + '" + "'.join(chunks) + '"'
                code = code.replace(f'"{s}"', concatenated, 1)
        
        return code
    
    def randomize_case(self, code):
        """Randomize command casing"""
        command_aliases = {
            'New-Object': ['NeW-OBJEcT', 'new-object', 'NEW-objECT'],
            'Out-String': ['ouT-StRiNG', 'out-string', 'OUT-string'],
            'GetString': ['gETsTRInG', 'getstring'],
            'Invoke-Expression': ['InVoKe-ExPreSsIoN', 'invoke-expression']
        }
        
        obfuscated_code = code
        
        for cmd, aliases in command_aliases.items():
            if cmd in obfuscated_code:
                obfuscated_code = obfuscated_code.replace(cmd, random.choice(aliases))
        
        return obfuscated_code