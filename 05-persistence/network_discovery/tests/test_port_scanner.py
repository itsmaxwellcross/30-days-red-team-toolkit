import unittest
from network_discovery.scanners.port_scanner import PortScanner


class TestPortScanner(unittest.TestCase):
    
    def setUp(self):
        self.scanner = PortScanner()
    
    def test_identify_service(self):
        # Test service identification
        self.assertEqual(self.scanner.identify_service(22), 'SSH')
        self.assertEqual(self.scanner.identify_service(80), 'HTTP')
        self.assertEqual(self.scanner.identify_service(445), 'SMB')
        self.assertEqual(self.scanner.identify_service(99999), 'Unknown (99999)')
    
    def test_default_ports(self):
        # Test that default ports list is not empty
        self.assertTrue(len(self.scanner.DEFAULT_PORTS) > 0)
        
        # Test that common ports are included
        self.assertIn(22, self.scanner.DEFAULT_PORTS)
        self.assertIn(445, self.scanner.DEFAULT_PORTS)
        self.assertIn(3389, self.scanner.DEFAULT_PORTS)


if __name__ == '__main__':
    unittest.main()