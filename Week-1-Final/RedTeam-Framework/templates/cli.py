#!/usr/bin/env python3
"""
Command-line interface for attack chain templates
"""

import argparse
import sys
from pathlib import Path

from templates.manager import AttackChainTemplateManager
from templates.executor import TemplateExecutor
from core.logger import EngagementLogger
from core.executor import CommandExecutor


def main():
    parser = argparse.ArgumentParser(
        description="Attack Chain Template Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all templates
  python3 -m templates.cli --list

  # Show template details
  python3 -m templates.cli --show web_app_takeover

  # Execute a template
  python3 -m templates.cli --execute web_app_takeover --vars config.json

  # Execute specific phase only
  python3 -m templates.cli --execute lateral_movement --phase reconnaissance

  # Export template to file
  python3 -m templates.cli --export domain_compromise --output my_template.json
        """
    )
    
    # Template management commands
    parser.add_argument('--list', action='store_true',
                       help='List all available templates')
    parser.add_argument('--show', metavar='TEMPLATE',
                       help='Show details of a specific template')
    parser.add_argument('--export', metavar='TEMPLATE',
                       help='Export template to JSON file')
    parser.add_argument('--import', metavar='FILE', dest='import_file',
                       help='Import template from JSON file')
    
    # Template execution
    parser.add_argument('--execute', metavar='TEMPLATE',
                       help='Execute an attack chain template')
    parser.add_argument('--vars', metavar='FILE',
                       help='JSON file containing variable substitutions')
    parser.add_argument('--phase', metavar='PHASE',
                       help='Execute only specified phase')
    parser.add_argument('--step', type=int, metavar='NUM',
                       help='Execute only specified step number')
    
    # Output options
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Output file for export operations')
    parser.add_argument('--results-dir', default='results/templates',
                       help='Directory for execution results (default: results/templates)')
    
    args = parser.parse_args()
    
    # Initialize template manager
    manager = AttackChainTemplateManager()
    
    # Handle commands
    if args.list:
        list_templates(manager)
    
    elif args.show:
        show_template(manager, args.show)
    
    elif args.export:
        export_template(manager, args.export, args.output)
    
    elif args.import_file:
        import_template(manager, args.import_file)
    
    elif args.execute:
        execute_template(manager, args.execute, args.vars, args.phase, 
                        args.step, args.results_dir)
    
    else:
        parser.print_help()


def list_templates(manager):
    """List all available templates"""
    print("\n" + "="*60)
    print("AVAILABLE ATTACK CHAIN TEMPLATES")
    print("="*60)
    
    templates = manager.list_templates()
    
    for i, template_name in enumerate(templates, 1):
        template = manager.get_template(template_name)
        print(f"\n{i}. {template['name']}")
        print(f"   ID: {template_name}")
        print(f"   Description: {template['description']}")
        
        if 'target_type' in template:
            print(f"   Target Type: {template['target_type']}")
        if 'difficulty' in template:
            print(f"   Difficulty: {template['difficulty']}")
        if 'estimated_time' in template:
            print(f"   Estimated Time: {template['estimated_time']}")
    
    print(f"\nTotal templates: {len(templates)}\n")


def show_template(manager, template_name):
    """Show detailed information about a template"""
    template = manager.get_template(template_name)
    
    if not template:
        print(f"[!] Template '{template_name}' not found")
        return
    
    print("\n" + "="*60)
    print(f"TEMPLATE: {template['name']}")
    print("="*60)
    print(f"\nDescription: {template['description']}")
    
    if 'target_type' in template:
        print(f"Target Type: {template['target_type']}")
    if 'difficulty' in template:
        print(f"Difficulty: {template['difficulty']}")
    if 'estimated_time' in template:
        print(f"Estimated Time: {template['estimated_time']}")
    
    if 'prerequisites' in template:
        print("\nPrerequisites:")
        for prereq in template['prerequisites']:
            print(f"  - {prereq}")
    
    if 'warnings' in template:
        print("\n⚠️  WARNINGS:")
        for warning in template['warnings']:
            print(f"  - {warning}")
    
    print("\nPhases:")
    for i, phase in enumerate(template['phases'], 1):
        print(f"\n{i}. {phase['name']} ({phase['phase']})")
        if 'description' in phase:
            print(f"   {phase['description']}")
        print(f"   Steps: {len(phase['steps'])}")
        
        # Show required variables
        all_vars = set()
        for step in phase['steps']:
            all_vars.update(step.get('required_vars', []))
        
        if all_vars:
            print(f"   Required Variables: {', '.join(sorted(all_vars))}")
    
    print()


def export_template(manager, template_name, output_file):
    """Export template to JSON file"""
    if not output_file:
        output_file = f"{template_name}.json"
    
    try:
        manager.export_template(template_name, output_file)
        print(f"[+] Template exported to: {output_file}")
    except Exception as e:
        print(f"[!] Export failed: {e}")


def import_template(manager, input_file):
    """Import template from JSON file"""
    try:
        template_name = manager.import_template(input_file)
        print(f"[+] Template imported as: {template_name}")
    except Exception as e:
        print(f"[!] Import failed: {e}")


def execute_template(manager, template_name, vars_file, phase_filter, 
                     step_filter, results_dir):
    """Execute an attack chain template"""
    # Get template
    template = manager.get_template(template_name)
    if not template:
        print(f"[!] Template '{template_name}' not found")
        return
    
    # Load variables
    import json
    variables = {}
    if vars_file:
        try:
            with open(vars_file, 'r') as f:
                variables = json.load(f)
        except Exception as e:
            print(f"[!] Failed to load variables file: {e}")
            return
    else:
        # Prompt for required variables
        variables = prompt_for_variables(template, phase_filter)
    
    # Initialize executor components
    logger = EngagementLogger(f"template_{template_name}")
    command_executor = CommandExecutor(logger)
    
    # Execute template
    executor = TemplateExecutor(template, variables, command_executor, logger)
    
    try:
        results = executor.execute(phase_filter=phase_filter, step_filter=step_filter)
        
        # Save results
        results_path = executor.save_results(results_dir)
        
        print("\n" + "="*60)
        print("EXECUTION COMPLETE")
        print("="*60)
        print(f"Results saved to: {results_path}")
        print(f"Logs available in: logs/")
        
    except KeyboardInterrupt:
        print("\n[!] Execution interrupted by user")
    except Exception as e:
        print(f"\n[!] Execution failed: {e}")


def prompt_for_variables(template, phase_filter=None):
    """Interactively prompt user for required variables"""
    print("\n" + "="*60)
    print("VARIABLE CONFIGURATION")
    print("="*60)
    print("Enter values for required variables:\n")
    
    # Collect all required variables from template
    all_vars = set()
    for phase in template['phases']:
        if phase_filter and phase['phase'] != phase_filter:
            continue
        
        for step in phase['steps']:
            all_vars.update(step.get('required_vars', []))
    
    variables = {}
    for var in sorted(all_vars):
        value = input(f"{var}: ")
        variables[var] = value
    
    return variables


if __name__ == '__main__':
    main()