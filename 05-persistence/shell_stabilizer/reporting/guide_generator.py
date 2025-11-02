"""Generate comprehensive stabilization guides"""

from ..config import GUIDE_WIDTH
from . import troubleshooting

class GuideGenerator:
    """Generate comprehensive shell stabilization guides"""
    
    def __init__(self, shell_type):
        self.shell_type = shell_type
    
    def generate_guide(self, techniques, output_file='shell_stabilization.txt'):
        """
        Generate comprehensive stabilization guide
        Returns: Guide string
        """
        guide = self._generate_header()
        guide += self._generate_techniques_section(techniques)
        guide += self._generate_troubleshooting_section()
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write(guide)
        
        return guide
    
    def _generate_header(self):
        """Generate guide header"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║         SHELL STABILIZATION GUIDE - {self.shell_type.upper():14}          ║
╚══════════════════════════════════════════════════════════════╝

"""
    
    def _generate_techniques_section(self, techniques):
        """Generate techniques section"""
        section = ""
        
        for technique_id, technique_info in techniques.items():
            section += f"\n{'='*GUIDE_WIDTH}\n"
            section += f"[{technique_info['name']}]\n"
            section += f"{'='*GUIDE_WIDTH}\n\n"
            
            if isinstance(technique_info['commands'], list):
                for cmd in technique_info['commands']:
                    section += f"{cmd}\n"
            else:
                section += f"{technique_info['commands']}\n"
            
            section += f"\nℹ️  {technique_info['notes']}\n"
        
        return section
    
    def _generate_troubleshooting_section(self):
        """Generate troubleshooting section"""
        section = f"\n\n{'='*GUIDE_WIDTH}\n"
        section += "TROUBLESHOOTING\n"
        section += f"{'='*GUIDE_WIDTH}\n"
        
        if self.shell_type == 'linux':
            section += troubleshooting.get_linux_troubleshooting()
        else:
            section += troubleshooting.get_windows_troubleshooting()
        
        return section