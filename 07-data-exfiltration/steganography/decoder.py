#!/usr/bin/env python3
"""
Steganography decoding operations
"""

from .binary_ops import BinaryConverter
from .image_ops import ImageProcessor

class SteganographyDecoder:
    """Decode data from images using LSB steganography"""
    
    def __init__(self):
        """Initialize decoder"""
        self.binary_converter = BinaryConverter()
        self.image_processor = ImageProcessor()
    
    def decode_data(self, image_path):
        """
        Decode data from image
        
        Args:
            image_path: Path to encoded image
            
        Returns:
            Decoded bytes or None if failed
        """
        # Load image
        img, img_array = self.image_processor.load_image(image_path)
        
        # Flatten image
        flat_img = self.image_processor.flatten_array(img_array)
        
        # Extract length from first 32 bits
        length_bits = self._extract_bits_from_pixels(flat_img, 0, 32)
        data_len = self.binary_converter.extract_length_from_bits(length_bits)
        
        if data_len is None:
            print(f"[-] Failed to extract length header")
            return None
        
        print(f"[*] Encoded data length: {data_len} bytes")
        
        # Validate length
        max_bytes = self.image_processor.calculate_capacity(img_array)
        if data_len == 0 or data_len > max_bytes:
            print(f"[-] Invalid data length: {data_len}")
            print(f"[-] Image capacity: {max_bytes} bytes")
            return None
        
        # Extract data bits (skip 32-bit header)
        total_bits = (data_len + 4) * 8  # +4 for length header
        data_bits = self._extract_bits_from_pixels(flat_img, 32, total_bits)
        
        # Convert bits to bytes
        data_bytes = self.binary_converter.binary_to_bytes(data_bits)
        
        print(f"[+] Data decoded successfully")
        print(f"[+] Decoded {len(data_bytes)} bytes")
        
        return data_bytes
    
    def _extract_bits_from_pixels(self, flat_img, start_bit, end_bit):
        """
        Extract bits from pixel LSBs
        
        Args:
            flat_img: Flattened image array
            start_bit: Starting bit index
            end_bit: Ending bit index
            
        Returns:
            Binary string
        """
        bits = []
        for i in range(start_bit, end_bit):
            if i < len(flat_img):
                bits.append(str(flat_img[i] & 1))
        
        return ''.join(bits)
    
    def decode_file(self, image_path, output_path):
        """
        Decode file from image and save
        
        Args:
            image_path: Path to encoded image
            output_path: Path to save decoded file
            
        Returns:
            True if successful, False otherwise
        """
        data = self.decode_data(image_path)
        
        if data:
            with open(output_path, 'wb') as f:
                f.write(data)
            
            print(f"[+] File saved: {output_path}")
            print(f"[+] Size: {len(data)} bytes")
            return True
        
        return False
    
    def decode_text(self, image_path):
        """
        Decode data as text string
        
        Args:
            image_path: Path to encoded image
            
        Returns:
            Decoded string or None
        """
        data = self.decode_data(image_path)
        
        if data:
            try:
                text = data.decode('utf-8')
                print(f"[+] Decoded text:")
                print(text)
                return text
            except UnicodeDecodeError:
                print(f"[-] Data is not valid UTF-8 text")
                return None
        
        return None