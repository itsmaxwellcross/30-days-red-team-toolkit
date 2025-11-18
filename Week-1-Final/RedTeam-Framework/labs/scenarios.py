"""
Practice Scenario Generator
Creates structured practice exercises
"""

import os
from pathlib import Path
from labs.scenario_definitions import SCENARIO_DEFINITIONS


class ScenarioGenerator:
    """
    Generates practice scenario documentation
    Creates structured exercises with objectives, steps, and hints
    """
    
    def __init__(self, base_dir='06-integration'):
        self.base_dir = Path(base_dir)
        self.scenarios_dir = self.base_dir / 'scenarios' / 'practice'
        self.scenarios_dir.mkdir(parents=True, exist_ok=True)
        self.scenarios = SCENARIO_DEFINITIONS
    
    def generate_all_scenarios(self):
        """Generate all scenario documents"""
        print(f"[*] Generating practice scenarios...")
        
        for scenario_id, scenario in self.scenarios.items():
            self._generate_scenario_doc(scenario_id, scenario)
        
        self._generate_index()
        
        print(f"[+] Generated {len(self.scenarios)} practice scenarios")
        print(f"[+] Location: {self.scenarios_dir}/")
    
    def _generate_scenario_doc(self, scenario_id, scenario):
        """Generate individual scenario document"""
        filename = self.scenarios_dir / f"{scenario_id}.md"
        
        doc = self._build_scenario_markdown(scenario)
        
        with open(filename, 'w') as f:
            f.write(doc)
    
    def _build_scenario_markdown(self, scenario):
        """Build markdown content for scenario"""
        doc = f"# {scenario['name']}\n\n"
        doc += f"**Target:** {scenario['target']}\n"
        doc += f"**Difficulty:** {scenario['difficulty']}\n"
        
        if 'estimated_time' in scenario:
            doc += f"**Estimated Time:** {scenario['estimated_time']}\n"
        
        doc += "\n---\n\n"
        
        # Description
        if 'description' in scenario:
            doc += f"## Description\n\n{scenario['description']}\n\n"
        
        # Objectives
        doc += "## Objectives\n\n"
        for objective in scenario['objectives']:
            doc += f"- [ ] {objective}\n"
        
        # Prerequisites
        if 'prerequisites' in scenario:
            doc += "\n## Prerequisites\n\n"
            for prereq in scenario['prerequisites']:
                doc += f"- {prereq}\n"
        
        # Steps
        doc += "\n## Steps\n\n"
        for step in scenario['steps']:
            doc += f"### Step {step['step']}: {step['task']}\n\n"
            
            if 'description' in step:
                doc += f"{step['description']}\n\n"
            
            doc += f"**Command:**\n```bash\n{step['command']}\n```\n\n"
            
            if 'expected_output' in step:
                doc += f"**Expected Output:** {step['expected_output']}\n\n"
            
            doc += f"**Hint:** {step['hint']}\n\n"
            
            if 'notes' in step:
                doc += f"*Note: {step['notes']}*\n\n"
        
        # Success Criteria
        doc += f"## Success Criteria\n\n{scenario['success_criteria']}\n\n"
        
        # Additional Resources
        if 'resources' in scenario:
            doc += "## Additional Resources\n\n"
            for resource in scenario['resources']:
                doc += f"- {resource}\n"
            doc += "\n"
        
        # Footer
        doc += "---\n"
        doc += f"*{scenario.get('footer', 'Complete this scenario to practice red team techniques')}*\n"
        
        return doc
    
    def _generate_index(self):
        """Generate scenario index/README"""
        index = "# Practice Scenarios\n\n"
        index += "Complete these scenarios to practice Week 1 techniques.\n\n"
        index += "## Overview\n\n"
        index += "Each scenario is designed to practice specific skills from the red team toolkit.\n"
        index += "Start with Scenario 1 and progress through increasing difficulty levels.\n\n"
        
        # Group by difficulty
        difficulties = {}
        for scenario_id, scenario in self.scenarios.items():
            diff = scenario['difficulty']
            if diff not in difficulties:
                difficulties[diff] = []
            difficulties[diff].append((scenario_id, scenario))
        
        for difficulty in ['Beginner', 'Intermediate', 'Advanced']:
            if difficulty in difficulties:
                index += f"## {difficulty} Scenarios\n\n"
                
                for scenario_id, scenario in difficulties[difficulty]:
                    index += f"### [{scenario['name']}]({scenario_id}.md)\n"
                    index += f"- **Target:** {scenario['target']}\n"
                    index += f"- **Objectives:** {len(scenario['objectives'])}\n"
                    
                    if 'estimated_time' in scenario:
                        index += f"- **Time:** {scenario['estimated_time']}\n"
                    
                    index += "\n"
        
        # Quick Start Guide
        index += "## Quick Start\n\n"
        index += "1. Set up your practice lab (see [LAB_SETUP_GUIDE.md](../LAB_SETUP_GUIDE.md))\n"
        index += "2. Choose a scenario based on your skill level\n"
        index += "3. Follow the steps and use hints when needed\n"
        index += "4. Document your process and findings\n"
        index += "5. Review and understand each technique used\n\n"
        
        # Tips
        index += "## Tips for Success\n\n"
        index += "- **Take Notes:** Document every command and finding\n"
        index += "- **Understand, Don't Memorize:** Learn why each step works\n"
        index += "- **Use Hints Wisely:** Try to solve problems before checking hints\n"
        index += "- **Take Breaks:** Complex scenarios can take time\n"
        index += "- **Practice Variations:** Try different approaches to same objective\n"
        index += "- **Clean Up:** Always revert VMs to clean state between attempts\n\n"
        
        with open(self.scenarios_dir / 'README.md', 'w') as f:
            f.write(index)
        
        print(f"[+] Scenario index created: {self.scenarios_dir}/README.md")
    
    def generate_progress_tracker(self):
        """Generate progress tracking document"""
        tracker = "# Scenario Progress Tracker\n\n"
        tracker += "Track your completion of practice scenarios.\n\n"
        tracker += "## Completion Checklist\n\n"
        
        for scenario_id, scenario in self.scenarios.items():
            tracker += f"- [ ] {scenario['name']} ({scenario['difficulty']})\n"
            tracker += f"  - Date Completed: ___________\n"
            tracker += f"  - Time Taken: ___________\n"
            tracker += f"  - Notes: ___________\n\n"
        
        tracker += "## Skills Acquired\n\n"
        tracker += "Mark skills as you master them:\n\n"
        
        skills = [
            'Web Application Enumeration',
            'Vulnerability Scanning',
            'SQL Injection',
            'Web Shell Upload',
            'Reverse Shell Establishment',
            'Post-Exploitation Enumeration',
            'Credential Harvesting',
            'Network Discovery',
            'Lateral Movement',
            'Data Exfiltration',
            'Complete Attack Chain Execution'
        ]
        
        for skill in skills:
            tracker += f"- [ ] {skill}\n"
        
        tracker_file = self.scenarios_dir / 'PROGRESS_TRACKER.md'
        with open(tracker_file, 'w') as f:
            f.write(tracker)
        
        print(f"[+] Progress tracker created: {tracker_file}")