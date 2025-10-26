#!/usr/bin/env python3
"""
Technology Fingerprinter - Main Entry Point
"""

import sys
import warnings
from core.fingerprinter import TechFingerprinter

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Technology Fingerprinter")
        print("=" * 50)
        print("\nUsage: python3 main.py <url> [options]")
        print("\nOptions:")
        print("  --json       Export results as JSON (default)")
        print("  --markdown   Export results as Markdown")
        print("  --both       Export both formats")
        print("\nExamples:")
        print("  python3 main.py https://example.com")
        print("  python3 main.py example.com --markdown")
        print("  python3 main.py https://example.com --both")
        sys.exit(1)
    
    url = sys.argv[1]
    export_format = 'json'  # default
    
    # Parse options
    if '--markdown' in sys.argv:
        export_format = 'markdown'
    elif '--both' in sys.argv:
        export_format = 'both'
    
    # Create fingerprinter and run
    fingerprinter = TechFingerprinter(url)
    fingerprinter.run_fingerprint()
    fingerprinter.print_results()
    
    # Export results
    if export_format == 'both':
        fingerprinter.export_results('json')
        fingerprinter.export_results('markdown')
    else:
        fingerprinter.export_results(export_format)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)