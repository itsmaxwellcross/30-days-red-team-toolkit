#!/usr/bin/env python3
import random
import string

class RandomGenerator:
    """Helper class for generating random values"""
    
    @staticmethod
    def random_string(length=10):
        """Generate random string for variable names"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def random_int(min_val=1, max_val=255):
        """Generate random integer"""
        return random.randint(min_val, max_val)