"""
Report generation for engagement results
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generates various report formats for engagement results"""
    
    def __init__(self, results, config):
        self.results = results
        self.config = config
        self.report_dir = Path(f"results/{results['engagement_id']}")
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_phase_report(self, phase_name, phase_results):
        """Generate report for individual phase"""
        report_file = self.report_dir / f"phase_{phase_name}.json"
        
        with open(report_file, 'w') as f:
            json.dump(phase_results, f, indent=2)
        
        return str(report_file)
    
    def generate_final_report(self):
        """Generate final engagement report"""
        # JSON report
        json_report = self.report_dir / "engagement_report.json"
        with open(json_report, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Markdown report
        md_report = self.report_dir / "engagement_report.md"
        self._generate_markdown_report(md_report)
        
        return str(json_report), str(md_report)
    
    def _generate_markdown_report(self, filepath):
        """Generate human-readable markdown report"""
        report = self._build_markdown_content()
        
        with open(filepath, 'w') as f:
            f.write(report)
    
    def _build_markdown_content(self):
        """Build markdown report content"""
        report = f'''# Red Team Engagement Report

## Engagement Information
- **Engagement ID:** {self.results['engagement_id']}
- **Target:** {self.config.get('target.domain', 'N/A')}
- **Company:** {self.config.get('target.company_name', 'N/A')}
- **Start Time:** {self.results['start_time']}
- **End Time:** {self.results.get('end_time', 'In Progress')}

---

## Executive Summary

This report documents a red team engagement conducted against {self.config.get('target.company_name', 'the target organization')}.
The engagement followed the Cyber Kill Chain methodology, progressing through reconnaissance,
weaponization, delivery, exploitation, and post-exploitation phases.

---

'''
        
        # Add phase-specific sections
        report += self._build_reconnaissance_section()
        report += self._build_weaponization_section()
        report += self._build_delivery_section()
        report += self._build_exploitation_section()
        report += self._build_post_exploitation_section()
        
        # Add recommendations
        report += self._build_recommendations_section()
        
        # Add appendix
        report += self._build_appendix_section()
        
        return report
    
    def _build_reconnaissance_section(self):
        """Build reconnaissance section"""
        section = "## Phase 1: Reconnaissance\n\n"
        
        if 'reconnaissance' in self.results['phases']:
            recon = self.results['phases']['reconnaissance']
            section += f'''### Findings

- **Subdomains Discovered:** {len(recon.get('subdomains', []))}
- **Email Addresses Found:** {len(recon.get('emails', []))}
- **Technologies Identified:** {len(recon.get('technologies', {}))}

### Subdomains
'''
            for subdomain in recon.get('subdomains', [])[:10]:
                section += f"- {subdomain}\n"
            
            section += "\n### Email Addresses\n"
            for email in recon.get('emails', [])[:10]:
                section += f"- {email}\n"
        
        return section + "\n---\n\n"
    
    def _build_weaponization_section(self):
        """Build weaponization section"""
        section = "## Phase 2: Weaponization\n\n"
        
        if 'weaponization' in self.results['phases']:
            weapon = self.results['phases']['weaponization']
            section += f"Generated {len(weapon.get('payloads', []))} payload variants\n\n"
            
            for payload in weapon.get('payloads', []):
                section += f"- **{payload['type']}**: {payload['location']}\n"
        
        return section + "\n---\n\n"
    
    def _build_delivery_section(self):
        """Build delivery section"""
        section = "## Phase 3: Delivery\n\n"
        section += "Phishing infrastructure configured. Manual campaign execution required.\n"
        return section + "\n---\n\n"
    
    def _build_exploitation_section(self):
        """Build exploitation section"""
        section = "## Phase 4: Exploitation\n\n"
        
        if 'exploitation' in self.results['phases']:
            exploit = self.results['phases']['exploitation']
            section += f"- **Vulnerabilities Found:** {len(exploit.get('vulnerabilities_found', []))}\n\n"
            
            for vuln in exploit.get('vulnerabilities_found', [])[:5]:
                section += f"  - {vuln}\n"
        
        return section + "\n---\n\n"
    
    def _build_post_exploitation_section(self):
        """Build post-exploitation section"""
        section = "## Phase 5: Post-Exploitation\n\n"
        section += "Post-exploitation activities require active shell access.\n"
        section += "See auto_post_exploit.sh for automated enumeration script.\n"
        return section + "\n---\n\n"
    
    def _build_recommendations_section(self):
        """Build recommendations section"""
        return '''## Recommendations

1. Address identified vulnerabilities
2. Implement security awareness training
3. Strengthen access controls
4. Deploy additional monitoring
5. Review and update incident response procedures

---

'''
    
    def _build_appendix_section(self):
        """Build appendix section"""
        return f'''## Appendix

- Detailed logs: `logs/{self.results['engagement_id']}.log`
- Phase reports: `results/{self.results['engagement_id']}/phase_*.json`
'''