"""Main shell stabilizer orchestration"""

from .techniques import linux_techniques, windows_techniques
from .persistence import linux_persistence, windows_persistence
from .testing.feature_tests import ShellFeatureTester
from .reporting.guide_generator import GuideGenerator
from .config import DETECTION_COMMANDS

class ShellStabilizer:
    """Main shell stabilizer class"""
    
    def __init__(self, shell_type='linux'):
        self.shell_type = shell_type
        self.techniques_map = {
            'linux': linux_techniques.get_linux_techniques,
            'windows': windows_techniques.get_windows_techniques
        }
        self.persistence_map = {
            'linux': linux_persistence.get_linux_persistence_methods,
            'windows': windows_persistence.get_windows_persistence_methods
        }
    
    def detect_shell_type(self):
        """
        Detect what type of shell we're in
        This would be run ON the target system
        """
        return self.shell_type
    
    def get_techniques(self):
        """Get stabilization techniques for current shell type"""
        return self.techniques_map[self.shell_type]()
    
    def get_persistence_methods(self):
        """Get persistence methods for current shell type"""
        return self.persistence_map[self.shell_type]()
    
    def generate_stabilization_guide(self, output_file='shell_stabilization.txt'):
        """
        Generate comprehensive stabilization guide
        Returns: Guide string
        """
        techniques = self.get_techniques()
        guide_gen = GuideGenerator(self.shell_type)
        return guide_gen.generate_guide(techniques, output_file)
    
    def print_persistence_methods(self):
        """Print all persistence methods for current shell type"""
        methods = self.get_persistence_methods()
        
        print(f"\n[*] Persistence Methods for {self.shell_type.upper()}:")
        print("="*60)
        
        for method_name, method_info in methods.items():
            self._print_persistence_method(method_name, method_info)
    
    def _print_persistence_method(self, method_name, method_info):
        """Print a single persistence method"""
        print(f"\n[{method_name.upper()}]")
        print(f"Description: {method_info['description']}")
        print(f"Detection Risk: {method_info['detection_risk']}")
        print(f"Requires: {method_info['requires']}")
        print("\nCommands:")
        for cmd in method_info['commands']:
            print(f"  {cmd}")
    
    def test_shell_features(self):
        """Test shell features"""
        tester = ShellFeatureTester()
        tester.print_test_checklist()


class ShellPersistence:
    """Shell persistence utilities (kept for backward compatibility)"""
    
    def __init__(self):
        pass
    
    def linux_persistence_methods(self):
        """Get Linux persistence methods"""
        return linux_persistence.get_linux_persistence_methods()
    
    def windows_persistence_methods(self):
        """Get Windows persistence methods"""
        return windows_persistence.get_windows_persistence_methods()
