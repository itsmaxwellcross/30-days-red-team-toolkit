#!/usr/bin/env python3
"""
Image loading and processing utilities
"""

import numpy as np
from PIL import Image

class ImageProcessor:
    """Process images for steganography operations"""
    
    @staticmethod
    def load_image(image_path):
        """
        Load image and convert to numpy array
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (PIL Image, numpy array)
        """
        img = Image.open(image_path)
        img_array = np.array(img)
        return img, img_array
    
    @staticmethod
    def save_image(img_array, output_path):
        """
        Save numpy array as image
        
        Args:
            img_array: Numpy array containing image data
            output_path: Path to save image
        """
        result_img = Image.fromarray(img_array.astype('uint8'))
        result_img.save(output_path)
    
    @staticmethod
    def calculate_capacity(img_array):
        """
        Calculate maximum data capacity of image
        
        Args:
            img_array: Numpy array containing image data
            
        Returns:
            Maximum number of bytes that can be stored
        """
        # Each pixel can store 1 bit in LSB
        # Total pixels = img_array.size
        # 8 bits per byte
        return img_array.size // 8
    
    @staticmethod
    def flatten_array(img_array):
        """
        Flatten image array for bit manipulation
        
        Args:
            img_array: Multi-dimensional image array
            
        Returns:
            Flattened 1D array
        """
        return img_array.flatten()
    
    @staticmethod
    def reshape_array(flat_array, original_shape):
        """
        Reshape flattened array back to original image shape
        
        Args:
            flat_array: Flattened 1D array
            original_shape: Original shape tuple
            
        Returns:
            Reshaped array
        """
        return flat_array.reshape(original_shape)
    
    @staticmethod
    def validate_image_format(image_path):
        """
        Validate image is in supported format
        
        Args:
            image_path: Path to image
            
        Returns:
            True if valid, False otherwise
        """
        try:
            img = Image.open(image_path)
            # Check for supported formats (RGB or grayscale)
            if img.mode not in ['RGB', 'RGBA', 'L']:
                return False
            return True
        except Exception:
            return False