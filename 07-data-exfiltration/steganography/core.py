#!/usr/bin/env python3
"""
Core ImageSteganography class - main interface
"""

from .encoder import SteganographyEncoder
from .decoder import SteganographyDecoder
from .image_ops import ImageProcessor

class ImageSteganography:
    """Main interface for image steganography operations"""
    
    def __init__(self):
        """Initialize steganography toolkit"""
        self.encoder = SteganographyEncoder()
        self.decoder = SteganographyDecoder()
        self.image_processor = ImageProcessor()
        
        print("[+] Image steganography initialized")
    
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
        return self.encoder.encode_data(image_path, data, output_path)
    
    def decode_data(self, image_path):
        """
        Decode data from image
        
        Args:
            image_path: Path to encoded image
            
        Returns:
            Decoded bytes or None
        """
        return self.decoder.decode_data(image_path)
    
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
        return self.encoder.encode_file(image_path, file_path, output_path)
    
    def decode_file(self, image_path, output_path):
        """
        Decode file from image
        
        Args:
            image_path: Path to encoded image
            output_path: Path to save decoded file
            
        Returns:
            True if successful, False otherwise
        """
        return self.decoder.decode_file(image_path, output_path)
    
    def decode_text(self, image_path):
        """
        Decode data as text string
        
        Args:
            image_path: Path to encoded image
            
        Returns:
            Decoded string or None
        """
        return self.decoder.decode_text(image_path)
    
    def check_capacity(self, image_path):
        """
        Check how much data an image can hold
        
        Args:
            image_path: Path to image
            
        Returns:
            Dict with capacity information
        """
        _, img_array = self.image_processor.load_image(image_path)
        max_bytes = self.image_processor.calculate_capacity(img_array)
        
        return {
            'max_bytes': max_bytes,
            'max_kb': max_bytes / 1024,
            'max_mb': max_bytes / (1024 * 1024),
            'image_pixels': img_array.size,
            'image_shape': img_array.shape
        }
    
    def calculate_required_image_size(self, data_size):
        """
        Calculate minimum image size needed for data
        
        Args:
            data_size: Size of data in bytes
            
        Returns:
            Dict with size recommendations
        """
        return self.encoder.calculate_required_image_size(data_size)