"""
Unit tests for Run Key persistence methods
"""

import unittest
from unittest.mock import patch, MagicMock
from methods.run_keys import RunKeyPersistence


class TestRunKeyPersistence(unittest.TestCase):
    
    def setUp(self):
        self.persistence = RunKeyPersistence()
    
    @patch('methods.run_keys.run_command')
    @patch('methods.run_keys.check_admin')
    def test_install_hkcu_run_success(self, mock_admin, mock_command):
        """Test successful HKCU Run key installation"""
        mock_admin.return_value = False
        mock_command.return_value = {'success': True, 'stdout': '', 'stderr': ''}
        
        result = self.persistence.install_hkcu_run(r'C:\payload.exe')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['method'], 'run_key')
        self.assertIn('remove_command', result)
    
    @patch('methods.run_keys.run_command')
    @patch('methods.run_keys.check_admin')
    def test_install_hklm_run_no_admin(self, mock_admin, mock_command):
        """Test HKLM Run key fails without admin"""
        mock_admin.return_value = False
        
        result = self.persistence.install_hklm_run(r'C:\payload.exe')
        
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
