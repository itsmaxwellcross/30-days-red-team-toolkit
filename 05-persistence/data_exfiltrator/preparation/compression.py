"""
File compression functionality
"""

import os
import gzip


class Compressor:
    """Handle file compression"""
    
    def __init__(self, staging_dir: str):
        self.staging_dir = staging_dir
    
    def compress(self, file_path: str) -> str:
        """
        Compress file with gzip
        
        Args:
            file_path: Path to file to compress
        
        Returns:
            Path to compressed file or None
        """
        try:
            compressed_path = os.path.join(
                self.staging_dir,
                os.path.basename(file_path) + '.gz'
            )
            
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            return compressed_path
        except Exception as e:
            print(f"  [-] Compression failed: {e}")
            return None