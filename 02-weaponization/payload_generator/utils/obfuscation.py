#!/usr/bin/env python3
import random
import string

class Obfuscator:
    def __init__(self):
        self.var_names = {}
    
    def random_var_name(self, prefix="var", length=8):
        """Generate random variable names"""
        if prefix not in self.var_names:
            self.var_names[prefix] = ''.join(random.choices(string.ascii_lowercase, k=length))
        return self.var_names[prefix]