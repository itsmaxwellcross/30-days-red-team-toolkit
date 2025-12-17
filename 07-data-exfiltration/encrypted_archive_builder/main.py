"""
Encrypted Archive Builder - Main CLI
"""

import argparse
from core.orchestrator import EncryptedArchiveOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="Encrypted Archive Builder - Secure file archiving",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create encrypted ZIP archive
  python main.py --create file1.txt file2.txt --output archive.zip --password secret123
  
  # Create with directory
  python main.py --create /path/to/directory --output backup.tar.gz --password secret123 --format tar.gz
  
  # Multi-layer encryption
  python main.py --create sensitive_data/ --output data.zip --password secret123 --layers 3
  
  # Obfuscate filename
  python main.py --create data/ --output archive.zip --password secret123 --obfuscate
  
  # Decrypt and extract
  python main.py --decrypt archive.zip.encrypted --password secret123 --output ./extracted/
  
  # List formats
  python main.py --list-formats
        """
    )
    
    parser.add_argument('--create', nargs='+',
                       help='Files/directories to archive and encrypt')
    parser.add_argument('--decrypt', type=str,
                       help='Encrypted archive to decrypt')
    parser.add_argument('--output', type=str, required=True,
                       help='Output file or directory path')
    parser.add_argument('--password', type=str,
                       help='Encryption/decryption password')
    parser.add_argument('--format', type=str, default='zip',
                       choices=['zip', 'tar.gz', 'tar.bz2', 'tar'],
                       help='Archive format (default: zip)')
    parser.add_argument('--layers', type=int, default=1,
                       help='Number of encryption layers (default: 1)')
    parser.add_argument('--obfuscate', action='store_true',
                       help='Obfuscate output filename')
    parser.add_argument('--list-formats', action='store_true',
                       help='List supported archive formats')
    parser.add_argument('--no-banner', action='store_true',
                       help='Suppress banner')
    
    args = parser.parse_args()
    
    orchestrator = EncryptedArchiveOrchestrator()
    
    if not args.no_banner:
        orchestrator.display_banner()
    
    if args.list_formats:
        orchestrator.list_formats()
        return 0
    
    if args.create:
        if not args.password:
            print("[-] --password is required for encryption")
            return 1
        
        result = orchestrator.create_encrypted_archive(
            args.create,
            args.output,
            args.password,
            archive_format=args.format,
            layers=args.layers,
            obfuscate=args.obfuscate
        )
        
        return 0 if result else 1
    
    elif args.decrypt:
        if not args.password:
            print("[-] --password is required for decryption")
            return 1
        
        result = orchestrator.decrypt_and_extract(
            args.decrypt,
            args.password,
            args.output,
            layers=args.layers,
            archive_format=args.format
        )
        
        return 0 if result else 1
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)