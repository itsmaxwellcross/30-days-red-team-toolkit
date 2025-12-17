#!/usr/bin/env python3
"""
File splitting and reassembly operations
"""

import secrets
from pathlib import Path
from datetime import datetime
from .crypto import HashCalculator

class FileSplitter:
    """Split large files into chunks"""
    
    def __init__(self, chunk_size=5*1024*1024, staging_dir='exfil_staging'):
        """
        Initialize file splitter
        
        Args:
            chunk_size: Size of each chunk in bytes
            staging_dir: Directory for staging chunks
        """
        self.chunk_size = chunk_size
        self.staging_dir = Path(staging_dir)
        self.staging_dir.mkdir(exist_ok=True)
    
    def split(self, filepath):
        """
        Split file into chunks
        
        Args:
            filepath: Path to file to split
            
        Returns:
            Dict with transfer_id, transfer_dir, and manifest
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Calculate file hash
        print(f"[*] Calculating file hash...")
        file_hash = HashCalculator.calculate_file_hash(filepath)
        file_size = filepath.stat().st_size
        
        # Generate transfer ID
        transfer_id = secrets.token_hex(16)
        
        # Calculate number of chunks
        num_chunks = (file_size + self.chunk_size - 1) // self.chunk_size
        
        print(f"[*] Splitting file: {filepath.name}")
        print(f"[*] Size: {file_size / 1024 / 1024:.2f} MB")
        print(f"[*] Chunks: {num_chunks}")
        print(f"[*] Transfer ID: {transfer_id}")
        
        # Create transfer directory
        transfer_dir = self.staging_dir / transfer_id
        transfer_dir.mkdir(exist_ok=True)
        
        # Split file
        chunks = self._split_file_into_chunks(filepath, transfer_dir, num_chunks)
        
        # Create manifest
        manifest = {
            'transfer_id': transfer_id,
            'original_filename': filepath.name,
            'original_size': file_size,
            'original_hash': file_hash,
            'chunk_size': self.chunk_size,
            'num_chunks': num_chunks,
            'chunks': chunks,
            'created_at': datetime.now().isoformat()
        }
        
        # Save manifest
        manifest_path = transfer_dir / 'manifest.json'
        import json
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"[+] Manifest created: {manifest_path}")
        print(f"[+] Transfer directory: {transfer_dir}")
        
        return {
            'transfer_id': transfer_id,
            'transfer_dir': str(transfer_dir),
            'manifest': manifest
        }
    
    def _split_file_into_chunks(self, filepath, transfer_dir, num_chunks):
        """
        Internal method to split file
        
        Args:
            filepath: Source file path
            transfer_dir: Destination directory
            num_chunks: Expected number of chunks
            
        Returns:
            List of chunk info dicts
        """
        chunks = []
        
        with open(filepath, 'rb') as f:
            for i in range(num_chunks):
                chunk_data = f.read(self.chunk_size)
                
                if not chunk_data:
                    break
                
                # Calculate chunk hash
                chunk_hash = HashCalculator.calculate_data_hash(chunk_data)
                
                # Save chunk
                chunk_filename = f"chunk_{i:04d}.bin"
                chunk_path = transfer_dir / chunk_filename
                
                with open(chunk_path, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                
                chunks.append({
                    'index': i,
                    'filename': chunk_filename,
                    'size': len(chunk_data),
                    'hash': chunk_hash
                })
                
                print(f"[+] Created chunk {i+1}/{num_chunks}: {chunk_filename}")
        
        return chunks


class FileAssembler:
    """Reassemble files from chunks"""
    
    def __init__(self, staging_dir='exfil_staging'):
        """
        Initialize file assembler
        
        Args:
            staging_dir: Directory containing chunks
        """
        self.staging_dir = Path(staging_dir)
    
    def reassemble(self, transfer_id, output_path=None):
        """
        Reassemble file from chunks
        
        Args:
            transfer_id: Transfer ID from splitting operation
            output_path: Optional output path (uses original filename if not specified)
            
        Returns:
            True if successful, False otherwise
        """
        transfer_dir = self.staging_dir / transfer_id
        manifest_path = transfer_dir / 'manifest.json'
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        
        # Load manifest
        import json
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        original_filename = manifest['original_filename']
        original_hash = manifest['original_hash']
        num_chunks = manifest['num_chunks']
        
        if output_path is None:
            output_path = Path(original_filename)
        else:
            output_path = Path(output_path)
        
        print(f"[*] Reassembling file: {original_filename}")
        print(f"[*] Chunks: {num_chunks}")
        print(f"[*] Output: {output_path}")
        
        # Verify all chunks present
        missing_chunks = self._check_missing_chunks(transfer_dir, manifest)
        
        if missing_chunks:
            raise ValueError(f"Missing chunks: {missing_chunks}")
        
        # Reassemble file
        self._reassemble_chunks(transfer_dir, manifest, output_path)
        
        # Verify final file hash
        print(f"[*] Verifying file integrity...")
        final_hash = HashCalculator.calculate_file_hash(output_path)
        
        if final_hash != original_hash:
            raise ValueError(
                f"File hash mismatch!\n"
                f"Expected: {original_hash}\n"
                f"Got: {final_hash}"
            )
        
        print(f"[+] File reassembled successfully!")
        print(f"[+] Hash verified: {final_hash}")
        
        return True
    
    def _check_missing_chunks(self, transfer_dir, manifest):
        """Check for missing chunks"""
        missing = []
        
        for chunk_info in manifest['chunks']:
            chunk_path = transfer_dir / chunk_info['filename']
            if not chunk_path.exists():
                missing.append(chunk_info['index'])
        
        return missing
    
    def _reassemble_chunks(self, transfer_dir, manifest, output_path):
        """Reassemble chunks into file"""
        with open(output_path, 'wb') as output_file:
            for chunk_info in manifest['chunks']:
                chunk_path = transfer_dir / chunk_info['filename']
                
                with open(chunk_path, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                
                # Verify chunk hash
                if not HashCalculator.verify_chunk_hash(chunk_data, chunk_info['hash']):
                    raise ValueError(f"Chunk {chunk_info['index']} hash mismatch!")
                
                output_file.write(chunk_data)
                
                print(f"[+] Assembled chunk {chunk_info['index'] + 1}/{manifest['num_chunks']}")