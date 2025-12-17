#!/usr/bin/env python3
"""
Command-line interface for steganography toolkit
"""

import argparse
import os
import sys
from .core import ImageSteganography

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Image Steganography Toolkit - Hide data in images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Hide text in image
  steganography.py --encode carrier.png --data "secret message" --output encoded.png
  
  # Hide file in image
  steganography.py --encode photo.jpg --data passwords.txt --output vacation.jpg
  
  # Extract data from image
  steganography.py --decode encoded.png --output extracted.txt
  
  # Extract and display text
  steganography.py --decode encoded.png --text
  
  # Check image capacity
  steganography.py --capacity photo.jpg
  
  # Calculate required image size
  steganography.py --calc-size 1000000  # For 1MB of data
        """
    )
    
    parser.add_argument('--encode', type=str, metavar='IMAGE',
                       help='Carrier image for encoding')
    parser.add_argument('--decode', type=str, metavar='IMAGE',
                       help='Encoded image for decoding')
    parser.add_argument('--data', type=str,
                       help='Data or file to encode')
    parser.add_argument('--output', type=str, metavar='FILE',
                       help='Output file')
    parser.add_argument('--text', action='store_true',
                       help='Decode and display as text')
    parser.add_argument('--capacity', type=str, metavar='IMAGE',
                       help='Check image capacity')
    parser.add_argument('--calc-size', type=int, metavar='BYTES',
                       help='Calculate required image size for data')
    
    args = parser.parse_args()
    
    stego = ImageSteganography()
    
    try:
        if args.capacity:
            # Check capacity
            capacity = stego.check_capacity(args.capacity)
            print(f"\n[*] Image Capacity Analysis:")
            print(f"    Image: {args.capacity}")
            print(f"    Shape: {capacity['image_shape']}")
            print(f"    Total pixels: {capacity['image_pixels']:,}")
            print(f"    Max capacity: {capacity['max_bytes']:,} bytes")
            print(f"    Max capacity: {capacity['max_kb']:.2f} KB")
            print(f"    Max capacity: {capacity['max_mb']:.2f} MB")
        
        elif args.calc_size:
            # Calculate required size
            size_info = stego.calculate_required_image_size(args.calc_size)
            print(f"\n[*] Required Image Size:")
            print(f"    Data size: {size_info['data_bytes']:,} bytes")
            print(f"    Total with header: {size_info['total_bytes_with_header']:,} bytes")
            print(f"    Required pixels: {size_info['required_pixels']:,}")
            print(f"    Suggested dimensions: {size_info['suggested_width']}x{size_info['suggested_height']}")
            print(f"    Total pixels: {size_info['suggested_total_pixels']:,}")
        
        elif args.encode and args.data:
            if not args.output:
                print("[-] --output required for encoding")
                return 1
            
            # Check if data is a file
            if os.path.isfile(args.data):
                success = stego.encode_file(args.encode, args.data, args.output)
            else:
                success = stego.encode_data(args.encode, args.data, args.output)
            
            if not success:
                return 1
        
        elif args.decode:
            if args.text:
                # Decode as text
                text = stego.decode_text(args.decode)
                if not text:
                    return 1
            else:
                # Decode to file
                if not args.output:
                    print("[-] --output required for decoding to file")
                    return 1
                
                success = stego.decode_file(args.decode, args.output)
                if not success:
                    return 1
        
        else:
            parser.print_help()
            return 1
    
    except FileNotFoundError as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())