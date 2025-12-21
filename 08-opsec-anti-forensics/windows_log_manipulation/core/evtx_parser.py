"""
EVTX File Parser and Manipulator
Handles reading, parsing, and modifying Windows Event Log files
"""

import struct
from pathlib import Path
from .constants import EVTX_SIGNATURE, EVTX_MIN_HEADER_SIZE


class WindowsEventLog:
    """
    Windows Event Log (EVTX) file parser and manipulator
    
    Provides functionality to:
    - Read and parse EVTX file headers
    - Find events by Event ID
    - Delete specific event records
    """
    
    def __init__(self, log_path=None):
        """
        Initialize event log manipulation
        
        Args:
            log_path (str, optional): Path to EVTX file to work with
        """
        self.log_path = log_path
        
        print(f"[+] Windows Event Log Manipulation initialized")
        if log_path:
            print(f"[+] Target log: {log_path}")
    
    def parse_evtx_header(self, data):
        """
        Parse EVTX file header
        
        Args:
            data (bytes): Raw EVTX file data
            
        Returns:
            dict: Parsed header information or None if invalid
        """
        if len(data) < EVTX_MIN_HEADER_SIZE:
            print(f"[-] File too small to contain valid EVTX header")
            return None
        
        # Verify EVTX file signature
        signature = data[0:8]
        if signature != EVTX_SIGNATURE:
            print(f"[-] Invalid EVTX signature")
            return None
        
        # Parse header fields
        try:
            first_chunk_num = struct.unpack('<Q', data[8:16])[0]
            last_chunk_num = struct.unpack('<Q', data[16:24])[0]
            next_record_id = struct.unpack('<Q', data[24:32])[0]
            header_size = struct.unpack('<I', data[32:36])[0]
            
            header = {
                'signature': signature,
                'first_chunk': first_chunk_num,
                'last_chunk': last_chunk_num,
                'next_record_id': next_record_id,
                'header_size': header_size
            }
            
            return header
            
        except struct.error as e:
            print(f"[-] Error parsing header: {e}")
            return None
    
    def read_evtx(self, filepath):
        """
        Read and parse EVTX file
        
        Args:
            filepath (str): Path to EVTX file
            
        Returns:
            tuple: (raw_data, header_dict) or (None, None) on error
        """
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            header = self.parse_evtx_header(data)
            
            if header:
                print(f"[+] EVTX file parsed successfully")
                print(f"    First chunk: {header['first_chunk']}")
                print(f"    Last chunk: {header['last_chunk']}")
                print(f"    Next record ID: {header['next_record_id']}")
                
                return data, header
            else:
                return None, None
        
        except FileNotFoundError:
            print(f"[-] File not found: {filepath}")
            return None, None
        except PermissionError:
            print(f"[-] Permission denied: {filepath}")
            return None, None
        except Exception as e:
            print(f"[-] Error reading EVTX: {e}")
            return None, None
    
    def find_event_by_id(self, data, event_id):
        """
        Find all occurrences of a specific Event ID in EVTX data
        
        Note: This is a simplified implementation using string search.
        For production use, consider using the pyevtx library for
        complete EVTX parsing.
        
        Args:
            data (bytes): Raw EVTX file data
            event_id (int): Event ID to search for
            
        Returns:
            list: List of byte positions where Event ID was found
        """
        # Search for Event ID in XML data (simplified approach)
        event_id_str = f"<EventID>{event_id}</EventID>".encode()
        
        positions = []
        start = 0
        
        while True:
            pos = data.find(event_id_str, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return positions
    
    def delete_event_records(self, filepath, event_ids, output_path):
        """
        Delete specific event records from EVTX file
        
        Note: This is a simplified implementation. Full implementation requires:
        1. Parse complete event record structure
        2. Remove record from chunk
        3. Update chunk header
        4. Recalculate checksums
        5. Update file header
        
        For production use, consider using a complete EVTX manipulation library.
        
        Args:
            filepath (str): Input EVTX file path
            event_ids (list): List of Event IDs to delete
            output_path (str): Output file path for modified log
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Deleting events: {event_ids}")
        print(f"[*] Input: {filepath}")
        print(f"[*] Output: {output_path}")
        
        try:
            # Read original file
            with open(filepath, 'rb') as f:
                data = bytearray(f.read())
            
            # Find and count events to be removed
            deleted_count = 0
            
            for event_id in event_ids:
                positions = self.find_event_by_id(data, event_id)
                print(f"[*] Found {len(positions)} instances of Event ID {event_id}")
                deleted_count += len(positions)
            
            # Write modified file
            # Note: This simplified version only identifies events
            # Actual deletion requires proper EVTX manipulation
            with open(output_path, 'wb') as f:
                f.write(data)
            
            print(f"[+] Located {deleted_count} event records")
            print(f"[+] Modified log saved: {output_path}")
            print(f"[!] Note: Full deletion requires EVTX structure manipulation")
            
            return True
        
        except FileNotFoundError:
            print(f"[-] Input file not found: {filepath}")
            return False
        except PermissionError:
            print(f"[-] Permission denied")
            return False
        except Exception as e:
            print(f"[-] Deletion failed: {e}")
            return False
    
    def get_event_count(self, filepath):
        """
        Get total number of events in EVTX file
        
        Args:
            filepath (str): Path to EVTX file
            
        Returns:
            int: Number of events or -1 on error
        """
        data, header = self.read_evtx(filepath)
        
        if header:
            return header.get('next_record_id', -1)
        
        return -1