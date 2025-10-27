"""
Main entry point for template generator
"""
import sys
import json
from pathlib import Path
from .core.generator import TemplateGenerator
from .core.target import TargetData

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python -m template_generator <command> [options]")
        print("\nCommands:")
        print("  generate <target_file> [template_type]  - Generate templates")
        print("  list                                     - List available types")
        print("  example                                  - Show example usage")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        from .config.settings import Settings
        print("\nAvailable template types:")
        for t in Settings.TEMPLATE_TYPES:
            print(f"  • {t}")
    
    elif command == 'example':
        show_example()
    
    elif command == 'generate':
        if len(sys.argv) < 3:
            print("Error: Provide target data file")
            print("Usage: python -m template_generator generate target.json [type]")
            sys.exit(1)
        
        target_file = sys.argv[2]
        template_type = sys.argv[3] if len(sys.argv) > 3 else None
        
        # Load target data
        with open(target_file, 'r') as f:
            target_data = json.load(f)
        
        # Generate templates
        generator = TemplateGenerator(target_data)
        
        if template_type:
            template = generator.generate(template_type)
            print_template(template)
        else:
            templates = generator.get_all_templates()
            for i, template in enumerate(templates, 1):
                print(f"\n{'='*60}")
                print(f"Template {i}: {template['template_type']}")
                print('='*60)
                print_template(template)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

def print_template(template: dict):
    """Pretty print a template"""
    print(f"\nSubject: {template['subject']}")
    print(f"Urgency: {template['urgency']}")
    print(f"\nBody:\n{template['body']}")

def show_example():
    """Show example usage"""
    print("\nExample target.json:")
    example = {
        'name': 'John Doe',
        'email': 'john.doe@target.com',
        'title': 'Senior Developer',
        'department': 'Engineering',
        'company_name': 'Target Corporation',
        'company_domain': 'target.com',
        'technologies_used': ['Office 365', 'Slack', 'GitHub', 'AWS']
    }
    print(json.dumps(example, indent=2))
    
    print("\n\nUsage examples:")
    print("  # Generate all templates")
    print("  python -m template_generator generate target.json")
    print("\n  # Generate specific template")
    print("  python -m template_generator generate target.json ceo_fraud")

if __name__ == "__main__":
    main()