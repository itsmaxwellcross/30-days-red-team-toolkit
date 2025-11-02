import unittest
from network_discovery.core.utils import is_port_open, get_platform


class TestUtils(unittest.TestCase):
    
    def test_get_platform(self):
        # Test platform detection
        platform = get_platform()
        self.assertIn(platform, ['linux', 'windows', 'darwin'])
    
    def test_is_port_open_localhost(self):
        # This might fail if nothing is listening on port 80
        # Just test that it returns a boolean
        result = is_port_open('127.0.0.1', 80, timeout=0.5)
        self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()