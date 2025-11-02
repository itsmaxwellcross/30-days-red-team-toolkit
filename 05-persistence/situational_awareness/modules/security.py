"""
Security product detection
"""

from ..core.utils import run_command


class SecurityEnumerator:
    """Detect security products"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
    
    def enumerate(self) -> dict:
        """Run security product detection"""
        print("\n[*] Checking for security products...")
        
        if self.os_type == 'linux':
            security_products = self._enumerate_linux_security()
        elif self.os_type == 'windows':
            security_products = self._enumerate_windows_security()
        else:
            security_products = {'antivirus': [], 'edr': [], 'firewall': []}
        
        self._print_results(security_products)
        return security_products
    
    def _enumerate_linux_security(self) -> dict:
        """Linux security product detection"""
        security_products = {'antivirus': [], 'edr': [], 'firewall': []}
        
        # Check for common security tools
        tools = ['clamav', 'chkrootkit', 'rkhunter', 'aide', 'ossec']
        
        for tool in tools:
            check = run_command(f'which {tool} 2>/dev/null')
            if check.strip():
                security_products['antivirus'].append(tool)
        
        # Check firewall
        if 'Chain' in run_command('iptables -L 2>/dev/null'):
            security_products['firewall'].append('iptables')
        
        if 'active' in run_command('ufw status 2>/dev/null').lower():
            security_products['firewall'].append('ufw')
        
        return security_products
    
    def _enumerate_windows_security(self) -> dict:
        """Windows security product detection"""
        security_products = {'antivirus': [], 'edr': [], 'firewall': []}
        
        # Check Windows Defender
        defender = run_command('powershell Get-MpComputerStatus 2>nul')
        if 'AntivirusEnabled' in defender and 'True' in defender:
            security_products['antivirus'].append('Windows Defender')
        
        # Check for EDR processes
        edr_processes = [
            'MsMpEng.exe', 'CrowdStrike', 'cb.exe', 
            'SentinelAgent', 'cylance'
        ]
        
        processes = run_command('tasklist')
        for edr in edr_processes:
            if edr.lower() in processes.lower():
                security_products['edr'].append(edr)
        
        # Check firewall
        firewall = run_command('netsh advfirewall show allprofiles state')
        if 'ON' in firewall:
            security_products['firewall'].append('Windows Firewall')
        
        return security_products
    
    def _print_results(self, security_products: dict):
        """Print security product results"""
        found_any = False
        
        for category, products in security_products.items():
            if products:
                found_any = True
                for product in products:
                    print(f"  [!] Found {category}: {product}")
        
        if not found_any:
            print(f"  [+] No obvious security products detected")
