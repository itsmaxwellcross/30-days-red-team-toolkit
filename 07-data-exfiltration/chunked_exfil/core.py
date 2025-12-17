#!/usr/bin/env python3
"""
Core ChunkedExfiltration class - main interface
"""

import base64
from pathlib import Path
from .file_ops import FileSplitter, FileAssembler
from .chunk_manager import ChunkManager
from .crypto import HashCalculator

class ChunkedExfiltration:
    """Main interface for chunked file exfiltration"""
    
    def __init__(self, chunk_size=5*1024*1024, staging_dir='exfil_staging'):
        """
        Initialize chunked exfiltration
        
        Args:
            chunk_size: Size of each chunk in bytes (default: 5MB)
            staging_dir: Directory for staging chunks
        """
        self.chunk_size = chunk_size
        self.staging_dir = Path(staging_dir)
        self.staging_dir.mkdir(exist_ok=True)
        
        self.splitter = FileSplitter(chunk_size, staging_dir)
        self.assembler = FileAssembler(staging_dir)
        
        print(f"[+] Chunked exfiltration initialized")
        print(f"[+] Chunk size: {chunk_size / 1024 / 1024:.2f} MB")
        print(f"[+] Staging directory: {staging_dir}")
    
    def split_file(self, filepath):
        """
        Split file into chunks
        
        Args:
            filepath: Path to file to split
            
        Returns:
            Dict with transfer_id, transfer_dir, and manifest
        """
        return self.splitter.split(filepath)
    
    def reassemble_file(self, transfer_id, output_path=None):
        """
        Reassemble file from chunks
        
        Args:
            transfer_id: Transfer ID from splitting operation
            output_path: Optional output path
            
        Returns:
            True if successful
        """
        return self.assembler.reassemble(transfer_id, output_path)
    
    def get_next_chunk(self, transfer_id):
        """
        Get next chunk to transfer
        
        Args:
            transfer_id: Transfer ID
            
        Returns:
            Dict with chunk data or None if all transferred
        """
        transfer_dir = self.staging_dir / transfer_id
        manager = ChunkManager(transfer_dir)
        return manager.get_next_chunk()
    
    def mark_chunk_transferred(self, transfer_id, chunk_index):
        """
        Mark chunk as successfully transferred
        
        Args:
            transfer_id: Transfer ID
            chunk_index: Index of chunk
        """
        transfer_dir = self.staging_dir / transfer_id
        manager = ChunkManager(transfer_dir)
        manager.mark_chunk_transferred(chunk_index)
    
    def receive_chunk(self, chunk_data):
        """
        Receive and save chunk from remote source
        
        Args:
            chunk_data: Dict containing transfer_id, chunk_index, data, hash
            
        Returns:
            True if successful
        """
        transfer_id = chunk_data['transfer_id']
        chunk_index = chunk_data['chunk_index']
        data = base64.b64decode(chunk_data['data'])
        expected_hash = chunk_data['hash']
        
        # Verify hash
        if not HashCalculator.verify_chunk_hash(data, expected_hash):
            print(f"[-] Chunk {chunk_index} hash mismatch!")
            return False
        
        # Create transfer directory
        transfer_dir = self.staging_dir / transfer_id
        transfer_dir.mkdir(exist_ok=True)
        
        # Save chunk
        chunk_filename = f"chunk_{chunk_index:04d}.bin"
        chunk_path = transfer_dir / chunk_filename
        
        with open(chunk_path, 'wb') as f:
            f.write(data)
        
        print(f"[+] Received chunk {chunk_index + 1}/{chunk_data['total_chunks']}")
        
        return True
    
    def get_transfer_progress(self, transfer_id):
        """
        Get transfer progress for a transfer
        
        Args:
            transfer_id: Transfer ID
            
        Returns:
            Dict with progress information
        """
        transfer_dir = self.staging_dir / transfer_id
        manager = ChunkManager(transfer_dir)
        return manager.get_transfer_progress()
    
    def calculate_file_hash(self, filepath):
        """
        Calculate SHA256 hash of file
        
        Args:
            filepath: Path to file
            
        Returns:
            Hex digest of hash
        """
        return HashCalculator.calculate_file_hash(filepath)