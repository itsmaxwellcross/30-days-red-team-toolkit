"""Shell feature testing utilities"""

class ShellFeatureTester:
    """Test shell features and capabilities"""
    
    def __init__(self):
        self.tests = {
            'basic_commands': [
                'whoami',
                'pwd',
                'id',
                'hostname'
            ],
            'terminal_control': [
                'Ctrl+C (should not kill shell)',
                'Ctrl+Z (should background process)',
                'Tab completion',
                'Up arrow (command history)'
            ],
            'interactive_programs': [
                'vi test.txt',
                'less /etc/passwd',
                'top',
                'su (should prompt for password properly)'
            ]
        }
    
    def print_test_checklist(self):
        """Print shell feature test checklist"""
        print("\n[*] Shell Feature Tests:")
        for category, test_list in self.tests.items():
            print(f"\n{category.upper()}:")
            for test in test_list:
                print(f"  □ {test}")
    
    def get_tests(self):
        """Get all test categories"""
        return self.tests