#!/usr/bin/env python3
from ..utils.helpers import RandomGenerator

class VariableRandomizer:
    """Randomize PowerShell variable names"""
    
    def __init__(self):
        self.var_mapping = {}
    
    def randomize_variables(self, code):
        """Replace common variables with random names"""
        common_vars = [
            '$client', '$stream', '$bytes', '$data', 
            '$sendback', '$i', '$cmd', '$result'
        ]
        
        obfuscated_code = code
        
        for var in common_vars:
            if var not in self.var_mapping:
                self.var_mapping[var] = f'${RandomGenerator.random_string()}'
            
            obfuscated_code = obfuscated_code.replace(var, self.var_mapping[var])
        
        return obfuscated_code
    
    def get_mapping(self):
        """Return variable mapping dictionary"""
        return self.var_mapping