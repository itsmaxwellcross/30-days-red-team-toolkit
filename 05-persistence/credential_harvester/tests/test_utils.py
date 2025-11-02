import unittest
from credential_harvester.core.utils import extract_credentials_with_patterns, run_command


class TestUtils(unittest.TestCase):
    
    def test_extract_credentials_basic(self):
        content = 'password="Secret123"'
        patterns = [r'password["\s]*[:=]["\s]*["\']([^"\']+)["\']']
        
        creds = extract_credentials_with_patterns(content, patterns)
        
        self.assertEqual(len(creds), 1)
        self.assertEqual(creds[0]['credential'], 'Secret123')
    
    def test_extract_credentials_skip_placeholders(self):
        content = 'password="password"'
        patterns = [r'password["\s]*[:=]["\s]*["\']([^"\']+)["\']']
        
        creds = extract_credentials_with_patterns(content, patterns)
        
        # Should skip placeholder "password"
        self.assertEqual(len(creds), 0)
    
    def test_run_command(self):
        # Test basic command execution
        result = run_command('echo test')
        self.assertIn('test', result)
    
    def test_run_command_timeout(self):
        # Test that timeout works
        result = run_command('sleep 100', timeout=1)
        self.assertIn('Error', result)


if __name__ == '__main__':
    unittest.main()