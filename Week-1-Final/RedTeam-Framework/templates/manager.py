#!/usr/bin/env python3
"""
Attack Chain Template Manager
Loads and manages attack chain templates
"""

import json
import os
from pathlib import Path
from datetime import datetime

from templates.web_app import WebAppTemplates
from templates.domain import DomainTemplates
from templates.lateral import LateralMovementTemplates
from templates.exfiltration import ExfiltrationTemplates
from templates.ransomware import RansomwareTemplates


class AttackChainTemplateManager:
    """
    Manages all attack chain templates
    Provides interface for loading and executing templates
    """
    
    def __init__(self):
        self.templates = {}
        self.template_dir = Path('templates/chains')
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.load_templates()
    
    def load_templates(self):
        """Load all attack chain templates"""
        # Load built-in templates
        self.templates = {
            'web_app_takeover': WebAppTemplates.web_app_takeover_chain(),
            'domain_compromise': DomainTemplates.domain_compromise_chain(),
            'lateral_movement': LateralMovementTemplates.lateral_movement_chain(),
            'data_exfiltration': ExfiltrationTemplates.data_exfiltration_chain(),
            'ransomware_simulation': RansomwareTemplates.ransomware_simulation_chain()
        }
        
        # Load custom templates from directory
        self._load_custom_templates()
    
    def _load_custom_templates(self):
        """Load custom templates from JSON files"""
        for template_file in self.template_dir.glob('*.json'):
            try:
                with open(template_file, 'r') as f:
                    template = json.load(f)
                    template_name = template_file.stem
                    self.templates[template_name] = template
            except Exception as e:
                print(f"[!] Error loading template {template_file}: {e}")
    
    def get_template(self, name):
        """Get a specific template by name"""
        return self.templates.get(name)
    
    def list_templates(self):
        """List all available templates"""
        return list(self.templates.keys())
    
    def save_template(self, name, template):
        """Save a custom template"""
        template_file = self.template_dir / f"{name}.json"
        with open(template_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        self.templates[name] = template
    
    def validate_template(self, template):
        """Validate template structure"""
        required_keys = ['name', 'description', 'phases']
        
        for key in required_keys:
            if key not in template:
                raise ValueError(f"Template missing required key: {key}")
        
        # Validate phases
        for phase in template['phases']:
            if 'phase' not in phase or 'steps' not in phase:
                raise ValueError("Phase must have 'phase' and 'steps' keys")
            
            # Validate steps
            for step in phase['steps']:
                required_step_keys = ['step', 'name', 'command']
                for key in required_step_keys:
                    if key not in step:
                        raise ValueError(f"Step missing required key: {key}")
        
        return True
    
    def format_command(self, command, variables):
        """Format command with provided variables"""
        for key, value in variables.items():
            command = command.replace(f'{{{key}}}', str(value))
        return command
    
    def export_template(self, name, output_file):
        """Export template to JSON file"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template '{name}' not found")
        
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
    
    def import_template(self, input_file):
        """Import template from JSON file"""
        with open(input_file, 'r') as f:
            template = json.load(f)
        
        self.validate_template(template)
        name = Path(input_file).stem
        self.save_template(name, template)
        
        return name