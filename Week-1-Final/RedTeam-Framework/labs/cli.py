#!/usr/bin/env python3
"""
Practice Lab Setup - Command Line Interface
"""

import argparse
from labs.manager import LabManager
from labs.scenarios import ScenarioGenerator
from labs.documentation import DocumentationGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Practice Lab Setup and Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available labs
  python3 -m labs.cli --list

  # Setup a Docker lab
  python3 -m labs.cli --setup dvwa

  # Show lab details
  python3 -m labs.cli --info juice_shop

  # Generate practice scenarios
  python3 -m labs.cli --create-scenarios

  # Generate lab guide
  python3 -m labs.cli --create-guide

  # Setup and start lab
  python3 -m labs.cli --setup dvwa --start
        """
    )
    
    # Lab management
    parser.add_argument('--list', action='store_true',
                       help='List all available labs')
    parser.add_argument('--info', metavar='LAB',
                       help='Show detailed information about a lab')
    parser.add_argument('--setup', metavar='LAB',
                       help='Setup specific lab')
    parser.add_argument('--start', action='store_true',
                       help='Start lab after setup')
    parser.add_argument('--stop', metavar='LAB',
                       help='Stop running lab')
    parser.add_argument('--status', action='store_true',
                       help='Show status of all labs')
    
    # Content generation
    parser.add_argument('--create-scenarios', action='store_true',
                       help='Generate practice scenarios')
    parser.add_argument('--create-guide', action='store_true',
                       help='Generate lab setup guide')
    parser.add_argument('--create-all-docs', action='store_true',
                       help='Generate all documentation')
    
    # Output options
    parser.add_argument('--output-dir', default='06-integration',
                       help='Output directory for generated files')
    
    args = parser.parse_args()
    
    # Initialize managers
    lab_manager = LabManager()
    scenario_gen = ScenarioGenerator(args.output_dir)
    doc_gen = DocumentationGenerator(args.output_dir)
    
    # Handle commands
    if args.list:
        list_labs(lab_manager)
    
    elif args.info:
        show_lab_info(lab_manager, args.info)
    
    elif args.setup:
        setup_lab(lab_manager, args.setup, args.start)
    
    elif args.stop:
        stop_lab(lab_manager, args.stop)
    
    elif args.status:
        show_status(lab_manager)
    
    elif args.create_scenarios:
        scenario_gen.generate_all_scenarios()
        print(f"[+] Scenarios created in {args.output_dir}/scenarios/practice/")
    
    elif args.create_guide:
        doc_gen.generate_lab_guide()
        print(f"[+] Lab guide created: {args.output_dir}/LAB_SETUP_GUIDE.md")
    
    elif args.create_all_docs:
        scenario_gen.generate_all_scenarios()
        doc_gen.generate_lab_guide()
        doc_gen.generate_quick_start()
        doc_gen.generate_troubleshooting_guide()
        print(f"[+] All documentation created in {args.output_dir}/")
    
    else:
        parser.print_help()


def list_labs(manager):
    """List all available labs"""
    print("\n" + "="*70)
    print("AVAILABLE PRACTICE LABS")
    print("="*70)
    
    labs = manager.get_all_labs()
    
    for lab_id, lab in labs.items():
        print(f"\n{lab_id}")
        print(f"  Name: {lab['name']}")
        print(f"  Type: {lab['type']}")
        print(f"  Description: {lab['description']}")
        print(f"  Access: {lab['access_url']}")
        print(f"  Scenarios: {len(lab['practice_scenarios'])}")
    
    print(f"\nTotal labs: {len(labs)}\n")


def show_lab_info(manager, lab_id):
    """Show detailed lab information"""
    lab = manager.get_lab(lab_id)
    
    if not lab:
        print(f"[!] Lab '{lab_id}' not found")
        return
    
    print("\n" + "="*70)
    print(f"LAB: {lab['name']}")
    print("="*70)
    
    print(f"\nType: {lab['type']}")
    print(f"Description: {lab['description']}")
    print(f"\nSetup Command:")
    print(f"  {lab['setup_command']}")
    print(f"\nAccess: {lab['access_url']}")
    
    if lab['default_creds'] != 'N/A':
        print(f"Default Credentials: {lab['default_creds']}")
    
    print("\nPractice Scenarios:")
    for scenario in lab['practice_scenarios']:
        print(f"  - {scenario}")
    
    print()


def setup_lab(manager, lab_id, start=False):
    """Setup and optionally start a lab"""
    print(f"\n[*] Setting up lab: {lab_id}")
    
    success = manager.setup_lab(lab_id)
    
    if success and start:
        print(f"\n[*] Starting lab...")
        # Lab should already be running from setup
        print(f"[+] Lab is running and ready")


def stop_lab(manager, lab_id):
    """Stop a running lab"""
    print(f"\n[*] Stopping lab: {lab_id}")
    success = manager.stop_lab(lab_id)
    
    if success:
        print(f"[+] Lab stopped successfully")
    else:
        print(f"[!] Failed to stop lab")


def show_status(manager):
    """Show status of all labs"""
    print("\n" + "="*70)
    print("LAB STATUS")
    print("="*70)
    
    status = manager.get_status()
    
    for lab_id, is_running in status.items():
        status_str = "RUNNING" if is_running else "STOPPED"
        print(f"{lab_id:20} [{status_str}]")
    
    print()


if __name__ == '__main__':
    main()