import unittest
import os
import tempfile
from credential_harvester.harvesters.ssh import SSHKeyHarvester


class TestSSHKeyHarvester(unittest.TestCase):
    
    def setUp(self):
        self.credentials = {'passwords': [], 'hashes': [], 'keys': [], 'tokens': []}
        self.harvester = SSHKeyHarvester(self.credentials, 'posix')
        
        # Create temporary SSH key
        self.temp_dir = tempfile.mkdtemp()
        self.key_file = os.path.join(self.temp_dir, 'id_rsa')
        
        with open(self.key_file, 'w') as f:
            f.write('-----BEGIN RSA PRIVATE KEY-----\ntest key\n-----END RSA PRIVATE KEY-----')
    
    def tearDown(self):
        os.remove(self.key_file)
        os.rmdir(self.temp_dir)
    
    def test_process_key_file(self):
        result = self.harvester._process_key_file(self.key_file)
        self.assertTrue(result)
        self.assertEqual(len(self.credentials['keys']), 1)
        self.assertEqual(self.credentials['keys'][0]['type'], 'SSH Private Key')
    
    def test_invalid_key_file(self):
        invalid_file = os.path.join(self.temp_dir, 'not_a_key.txt')
        with open(invalid_file, 'w') as f:
            f.write('not a key')
        
        result = self.harvester._process_key_file(invalid_file)
        self.assertFalse(result)
        
        os.remove(invalid_file)


if __name__ == '__main__':
    unittest.main()