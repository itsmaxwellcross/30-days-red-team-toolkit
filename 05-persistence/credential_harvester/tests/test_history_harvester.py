import unittest
from credential_harvester.harvesters.history import HistoryHarvester


class TestHistoryHarvester(unittest.TestCase):
    
    def setUp(self):
        self.credentials = {'passwords': [], 'hashes': [], 'keys': [], 'tokens': []}
        self.harvester = HistoryHarvester(self.credentials, 'posix')
    
    def test_credential_patterns(self):
        # Test that patterns are defined
        self.assertTrue(len(self.harvester.CREDENTIAL_PATTERNS) > 0)
        
        # Test pattern matching
        test_content = "mysql -u root -pMyPassword123"
        from credential_harvester.core.utils import extract_credentials_with_patterns
        
        creds = extract_credentials_with_patterns(test_content, self.harvester.CREDENTIAL_PATTERNS)
        self.assertTrue(len(creds) > 0)


if __name__ == '__main__':
    unittest.main()