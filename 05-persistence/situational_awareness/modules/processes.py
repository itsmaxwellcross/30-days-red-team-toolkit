"""
Running process enumeration
"""

from ..core.utils import run_command


class ProcessEnumerator:
    """Enumerate running processes"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
        self.interesting_keywords = [
            'ssh', 'sudo', 'mysql', 'postgres', 'apache', 'nginx',
            'docker', 'kube', 'jenkins', 'tomcat'
        ]
    
    def enumerate(self) -> dict:
        """Run process enumeration"""
        print("\n[*] Enumerating running processes...")
        
        if self.os_type == 'linux':
            processes = run_command('ps aux')
            interesting = self._find_interesting_linux(processes)
        elif self.os_type == 'windows':
            processes = run_command('tasklist /v')
            interesting = []
        else:
            processes = ""
            interesting = []
        
        self._print_results(interesting)
        
        return {
            'all_processes': processes,
            'interesting_processes': interesting
        }
    
    def _find_interesting_linux(self, processes: str) -> list:
        """Find interesting processes on Linux"""
        interesting_procs = []
        
        for line in processes.split('\n'):
            for keyword in self.interesting_keywords:
                if keyword in line.lower():
                    interesting_procs.append(line)
                    break
        
        return interesting_procs
    
    def _print_results(self, interesting: list):
        """Print process results"""
        if interesting:
            print(f"  Found {len(interesting)} interesting processes:")
            for proc in interesting[:10]:
                print(f"    {proc}")

