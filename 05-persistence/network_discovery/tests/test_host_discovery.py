import unittest
from network_discovery.scanners.host_discovery import HostDiscovery


class TestHostDiscovery(unittest.TestCase):
    
    def setUp(self):
        self.discovery = HostDiscovery()
    
    def test_ping_host_localhost(self):
        # Test pinging localhost
        result = self.discovery._ping_host('127.0.0.1', timeout=1)
        self.assertEqual(result, '127.0.0.1')
    
    def test_ping_host_invalid(self):
        # Test pinging invalid/unreachable IP
        result = self.discovery._ping_host('192.0.2.1', timeout=1)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()