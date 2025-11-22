"""
Unit tests for utility functions
"""

import unittest
from unittest.mock import patch
from core.utils import (
    generate_random_name,
    validate_payload_path,
    parse_reg_query_output
)


class TestUtils(unittest.TestCase):
    
    def test_generate_random_name(self):
        """Test random name generation"""
        name = generate_random_name()
        
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)
    
    def test_validate_payload_path_valid(self):
        """Test payload path validation"""
        is_valid, error = validate_payload_path(r'C:\payload.exe')
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_payload_path_invalid(self):
        """Test invalid payload path"""
        is_valid, error = validate_payload_path('C:\payload"test.exe')
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_parse_reg_query_output(self):
        """Test parsing registry query output"""
        output = """
HKEY_CURRENT_USER\\Software\\Test
    TestValue    REG_SZ    TestData
"""
        result = parse_reg_query_output(output, 'TestValue')
        
        self.assertEqual(result, 'TestData')


if __name__ == '__main__':
    unittest.main()