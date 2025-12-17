#!/usr/bin/env python3
"""
Chunk tracking and state management
"""

import json
import base64
from pathlib import Path

class ChunkManager:
    """Manage chunk transfer state and tracking"""
    
    def __init__(self, transfer_dir):
        """
        Initialize chunk manager
        
        Args:
            transfer_dir: Directory containing chunks
        """
        self.transfer_dir = Path(transfer_dir)
        self.state_file = self.transfer_dir / 'transfer_state.json'
        self.manifest_file = self.transfer_dir / 'manifest.json'
    
    def load_manifest(self):
        """Load transfer manifest"""
        if not self.manifest_file.exists():
            return None
        
        with open(self.manifest_file, 'r') as f:
            return json.load(f)
    
    def save_manifest(self, manifest):
        """Save transfer manifest"""
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
    
    def load_state(self):
        """Load transfer state"""
        if not self.state_file.exists():
            return {'transferred': []}
        
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def save_state(self, state):
        """Save transfer state"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
    
    def mark_chunk_transferred(self, chunk_index):
        """
        Mark chunk as successfully transferred
        
        Args:
            chunk_index: Index of transferred chunk
        """
        state = self.load_state()
        
        if chunk_index not in state['transferred']:
            state['transferred'].append(chunk_index)
        
        self.save_state(state)
    
    def get_next_chunk(self):
        """
        Get next chunk that needs to be transferred
        
        Returns:
            Dict with chunk data or None if all chunks transferred
        """
        manifest = self.load_manifest()
        if not manifest:
            return None
        
        state = self.load_state()
        
        # Find first untransferred chunk
        for chunk_info in manifest['chunks']:
            if chunk_info['index'] not in state['transferred']:
                chunk_path = self.transfer_dir / chunk_info['filename']
                
                if not chunk_path.exists():
                    continue
                
                with open(chunk_path, 'rb') as f:
                    chunk_data = f.read()
                
                return {
                    'transfer_id': manifest['transfer_id'],
                    'chunk_index': chunk_info['index'],
                    'total_chunks': manifest['num_chunks'],
                    'data': base64.b64encode(chunk_data).decode(),
                    'hash': chunk_info['hash'],
                    'size': chunk_info['size']
                }
        
        return None  # All chunks transferred
    
    def get_transfer_progress(self):
        """
        Get current transfer progress
        
        Returns:
            Dict with progress information
        """
        manifest = self.load_manifest()
        if not manifest:
            return None
        
        state = self.load_state()
        
        total_chunks = manifest['num_chunks']
        transferred_chunks = len(state['transferred'])
        
        return {
            'total_chunks': total_chunks,
            'transferred_chunks': transferred_chunks,
            'remaining_chunks': total_chunks - transferred_chunks,
            'progress_percent': (transferred_chunks / total_chunks * 100) if total_chunks > 0 else 0
        }
    
    def is_transfer_complete(self):
        """Check if all chunks have been transferred"""
        manifest = self.load_manifest()
        if not manifest:
            return False
        
        state = self.load_state()
        
        return len(state['transferred']) == manifest['num_chunks']