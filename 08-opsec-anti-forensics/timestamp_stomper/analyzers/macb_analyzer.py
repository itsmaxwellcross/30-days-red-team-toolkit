"""
MACB (Modified, Accessed, Changed, Birth) Analysis
Detects timestamp anomalies that may indicate tampering
"""

from datetime import datetime

from ..core.timestamp_stomper import TimestampStomper
from ..core.constants import TIMESTAMP_IDENTICAL_THRESHOLD


class MACBAnalysis:
    """
    Analyze file timestamps for anomalies
    
    MACB stands for:
    - M: Modified time
    - A: Accessed time
    - C: Changed time (metadata change / creation on Windows)
    - B: Birth time (true creation time, where available)
    """
    
    @staticmethod
    def analyze_macb(filepath):
        """
        Analyze MACB times for anomalies
        
        Args:
            filepath (str): Path to file to analyze
        """
        stomper = TimestampStomper()
        times = stomper.get_file_times(filepath)
        
        if not times:
            print(f"[-] Could not read timestamps for: {filepath}")
            return
        
        print(f"\n[*] MACB Analysis: {filepath}")
        print("="*60)
        
        modified = times['modified']
        accessed = times['accessed']
        created = times['created']
        
        print(f"Modified: {modified}")
        print(f"Accessed: {accessed}")
        print(f"Created:  {created}")
        print()
        
        # Detect anomalies
        anomalies = MACBAnalysis._detect_anomalies(modified, accessed, created)
        
        if anomalies:
            print("[!] ANOMALIES DETECTED:")
            for anomaly in anomalies:
                print(f"    {anomaly}")
        else:
            print("[+] No obvious timestamp anomalies detected")
        
        print()
    
    @staticmethod
    def _detect_anomalies(modified, accessed, created):
        """
        Detect timestamp anomalies
        
        Args:
            modified (datetime): Modification time
            accessed (datetime): Access time
            created (datetime): Creation time
            
        Returns:
            list: List of anomaly descriptions
        """
        anomalies = []
        now = datetime.now()
        
        # Accessed before creation
        if accessed < created:
            anomalies.append("⚠️  File accessed before it was created")
        
        # Modified before creation
        if modified < created:
            anomalies.append("⚠️  File modified before it was created")
        
        # Created in the future
        if created > now:
            anomalies.append("⚠️  File created in the future")
        
        # Modified in the future
        if modified > now:
            anomalies.append("⚠️  File modified in the future")
        
        # Accessed in the future
        if accessed > now:
            anomalies.append("⚠️  File accessed in the future")
        
        # Access and modify times identical (suspicious)
        time_diff = abs((accessed - modified).total_seconds())
        if time_diff < TIMESTAMP_IDENTICAL_THRESHOLD:
            anomalies.append("⚠️  Access and modify times identical (suspicious)")
        
        # All times identical (very suspicious)
        if modified == accessed == created:
            anomalies.append("⚠️  All timestamps identical (likely stomped)")
        
        # Modified without access (unusual)
        if modified > accessed:
            time_since_access = (modified - accessed).total_seconds()
            if time_since_access > 60:  # More than 1 minute
                anomalies.append("⚠️  File modified after last access (unusual pattern)")
        
        return anomalies
    
    @staticmethod
    def compare_timestamps(file1, file2):
        """
        Compare timestamps between two files
        
        Args:
            file1 (str): First file path
            file2 (str): Second file path
        """
        stomper = TimestampStomper()
        
        times1 = stomper.get_file_times(file1)
        times2 = stomper.get_file_times(file2)
        
        if not times1 or not times2:
            print("[-] Could not read timestamps from both files")
            return
        
        print(f"\n[*] Timestamp Comparison:")
        print("="*60)
        
        print(f"\nFile 1: {file1}")
        print(f"  Created:  {times1['created']}")
        print(f"  Modified: {times1['modified']}")
        print(f"  Accessed: {times1['accessed']}")
        
        print(f"\nFile 2: {file2}")
        print(f"  Created:  {times2['created']}")
        print(f"  Modified: {times2['modified']}")
        print(f"  Accessed: {times2['accessed']}")
        
        print(f"\nDifferences:")
        
        # Calculate differences
        created_diff = abs((times1['created'] - times2['created']).total_seconds())
        modified_diff = abs((times1['modified'] - times2['modified']).total_seconds())
        accessed_diff = abs((times1['accessed'] - times2['accessed']).total_seconds())
        
        print(f"  Created:  {created_diff:.2f} seconds")
        print(f"  Modified: {modified_diff:.2f} seconds")
        print(f"  Accessed: {accessed_diff:.2f} seconds")
        
        # Check if timestamps match (within threshold)
        threshold = TIMESTAMP_IDENTICAL_THRESHOLD
        
        if created_diff < threshold and modified_diff < threshold and accessed_diff < threshold:
            print(f"\n[!] Timestamps match within {threshold}s - possibly copied!")
        
        print()
    
    @staticmethod
    def batch_analyze(directory):
        """
        Analyze all files in a directory for timestamp anomalies
        
        Args:
            directory (str): Directory to analyze
        """
        from pathlib import Path
        
        print(f"[*] Batch MACB Analysis: {directory}")
        print("="*60)
        
        try:
            files = list(Path(directory).rglob('*'))
            files = [f for f in files if f.is_file()]
        except Exception as e:
            print(f"[-] Error reading directory: {e}")
            return
        
        anomaly_count = 0
        
        for filepath in files:
            stomper = TimestampStomper()
            times = stomper.get_file_times(str(filepath))
            
            if times:
                anomalies = MACBAnalysis._detect_anomalies(
                    times['modified'],
                    times['accessed'],
                    times['created']
                )
                
                if anomalies:
                    print(f"\n[!] {filepath.name}")
                    for anomaly in anomalies:
                        print(f"    {anomaly}")
                    anomaly_count += 1
        
        print(f"\n[*] Analysis complete:")
        print(f"    Total files: {len(files)}")
        print(f"    Files with anomalies: {anomaly_count}")
        print()