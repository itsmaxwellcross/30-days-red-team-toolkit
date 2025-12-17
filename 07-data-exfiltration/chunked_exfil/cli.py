#!/usr/bin/env python3
"""
Command-line interface for chunked exfiltration
"""

import argparse
import sys
from .core import ChunkedExfiltration

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Chunked File Exfiltration Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split file into 5MB chunks
  chunked_exfil.py --split largefile.zip
  
  # Split with custom chunk size (10MB)
  chunked_exfil.py --split database.sql --chunk-size 10
  
  # Reassemble file
  chunked_exfil.py --reassemble <TRANSFER_ID>
  
  # Reassemble to specific location
  chunked_exfil.py --reassemble <TRANSFER_ID> --output /path/to/file.zip
  
  # Get transfer progress
  chunked_exfil.py --progress <TRANSFER_ID>
        """
    )
    
    parser.add_argument('--split', type=str, metavar='FILE',
                       help='Split file into chunks')
    parser.add_argument('--reassemble', type=str, metavar='TRANSFER_ID',
                       help='Reassemble file from transfer ID')
    parser.add_argument('--progress', type=str, metavar='TRANSFER_ID',
                       help='Show transfer progress')
    parser.add_argument('--output', type=str, metavar='FILE',
                       help='Output file for reassembly')
    parser.add_argument('--chunk-size', type=int, default=5, metavar='MB',
                       help='Chunk size in MB (default: 5)')
    parser.add_argument('--staging-dir', type=str, default='exfil_staging',
                       help='Staging directory (default: exfil_staging)')
    
    args = parser.parse_args()
    
    # Initialize
    exfil = ChunkedExfiltration(
        chunk_size=args.chunk_size * 1024 * 1024,
        staging_dir=args.staging_dir
    )
    
    try:
        if args.split:
            result = exfil.split_file(args.split)
            print(f"\n[+] File split successfully")
            print(f"[+] Transfer ID: {result['transfer_id']}")
            print(f"\n[*] To reassemble:")
            print(f"    chunked_exfil.py --reassemble {result['transfer_id']}")
        
        elif args.reassemble:
            success = exfil.reassemble_file(args.reassemble, args.output)
            if success:
                print(f"\n[+] File reassembled successfully")
        
        elif args.progress:
            progress = exfil.get_transfer_progress(args.progress)
            if progress:
                print(f"\n[*] Transfer Progress:")
                print(f"    Total chunks: {progress['total_chunks']}")
                print(f"    Transferred: {progress['transferred_chunks']}")
                print(f"    Remaining: {progress['remaining_chunks']}")
                print(f"    Progress: {progress['progress_percent']:.1f}%")
            else:
                print(f"[-] Transfer not found: {args.progress}")
        
        else:
            parser.print_help()
            return 1
    
    except Exception as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())