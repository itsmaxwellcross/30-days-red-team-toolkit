#!/usr/bin/env python3
"""
Steganography encoding operations
"""

from .binary_ops import BinaryConverter
from .image_ops import ImageProcessor

class SteganographyEncoder:
    """Encode data into images using LSB steganography"""
    
    def __init__(self):
        """Initialize encoder"""
        self.binary_converter = BinaryConverter()
        self.image_processor = ImageProcessor()
    
    def encode_data(self, image_path, data, output_path):
        """
        Encode data into image
        
        Args:
            image_path: Path to carrier image
            data: Data to encode (string or bytes)
            output_path: Path for output image
            
        Returns:
            True if successful, False otherwise
        """
        # Load image
        img, img_array = self.image_processor.load_image(image_path)
        
        # Convert data to bytes if string
        data_bytes = data.encode() if isinstance(data, str) else data
        
        # Prepare data with length header
        data_with_header = self.binary_converter.prepare_data_with_header(data_bytes)
        
        # Convert to binary string
        binary_data = self.binary_converter.bytes_to_binary(data_with_header)
        
        # Check capacity
        max_bytes = self.image_processor.calculate_capacity(img_array)
        if len(data_with_header) > max_bytes:
            print(f"[-] Image too small! Max capacity: {max_bytes} bytes")
            print(f"[-] Data size: {len(data_with_header)} bytes")
            return False
        
        print(f"[*] Encoding {len(data_bytes)} bytes into image")
        print(f"[*] Image capacity: {max_bytes} bytes")
        print(f"[*] Capacity used: {len(data_with_header) / max_bytes * 100:.2f}%")
        
        # Flatten image for processing
        flat_img = self.image_processor.flatten_array(img_array)
        
        # Encode data into LSB
        flat_img = self._encode_bits_into_pixels(flat_img, binary_data)
        
        # Reshape and save
        encoded_img = self.image_processor.reshape_array(flat_img, img_array.shape)
        self.image_processor.save_image(encoded_img, output_path)
        
        print(f"[+] Data encoded successfully")
        print(f"[+] Output: {output_path}")
        
        return True
    
    def _encode_bits_into_pixels(self, flat_img, binary_data):
        """
        Encode binary data into pixel LSBs
        
        Args:
            flat_img: Flattened image array
            binary_data: Binary string to encode
            
        Returns:
            Modified image array
        """
        for i in range(len(binary_data)):
            # Clear LSB and set to data bit
            flat_img[i] = (flat_img[i] & 0xFE) | int(binary_data[i])
        
        return flat_img
    
    def encode_file(self, image_path, file_path, output_path):
        """
        Encode entire file into image
        
        Args:
            image_path: Path to carrier image
            file_path: Path to file to encode
            output_path: Path for output image
            
        Returns:
            True if successful, False otherwise
        """
        print(f"[*] Reading file: {file_path}")
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        print(f"[*] File size: {len(file_data)} bytes")
        
        return self.encode_data(image_path, file_data, output_path)
    
    def calculate_required_image_size(self, data_size):
        """
        Calculate minimum image dimensions needed for data
        
        Args:
            data_size: Size of data in bytes
            
        Returns:
            Dict with width and height recommendations
        """
        # Add 4 bytes for length header
        total_bytes = data_size + 4
        
        # Need 8 pixels per byte (1 bit per pixel)
        required_pixels = total_bytes * 8
        
        # Calculate square image dimensions
        side_length = int(required_pixels ** 0.5) + 1
        
        return {
            'data_bytes': data_size,
            'total_bytes_with_header': total_bytes,
            'required_pixels': required_pixels,
            'suggested_width': side_length,
            'suggested_height': side_length,
            'suggested_total_pixels': side_length * side_length
        }