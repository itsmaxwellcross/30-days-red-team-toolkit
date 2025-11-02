"""
Utility functions shared across harvesters
"""

import subprocess
import os
import re
from typing import Optional, List


def run_command(command: str, shell: bool = True, timeout: int = 30) -> str:
    """
    Execute system command and return output
    
    Args:
        command: Command to execute
        shell: Whether to use shell execution
        timeout: Command timeout in seconds
    
    Returns:
        Command output as string, or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


def safe_read_file(filepath: str) -> Optional[str]:
    """
    Safely read file contents
    
    Args:
        filepath: Path to file
    
    Returns:
        File contents or None if error
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return None


def find_files(pattern: str, search_paths: List[str], max_results: int = 50) -> List[str]:
    """
    Find files matching pattern in search paths
    
    Args:
        pattern: File pattern to search for
        search_paths: List of directories to search
        max_results: Maximum number of results
    
    Returns:
        List of matching file paths
    """
    found_files = []
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
        
        try:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if re.match(pattern, file):
                        found_files.append(os.path.join(root, file))
                        if len(found_files) >= max_results:
                            return found_files
        except PermissionError:
            continue
    
    return found_files


def extract_credentials_with_patterns(content: str, patterns: List[str]) -> List[dict]:
    """
    Extract credentials from content using regex patterns
    
    Args:
        content: Text content to search
        patterns: List of regex patterns
    
    Returns:
        List of found credentials with context
    """
    credentials = []
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            credential = match.group(1) if match.groups() else match.group(0)
            
            # Skip obvious placeholders
            if credential.lower() not in ['password', 'your_password', 'changeme', 'secret', 'xxx']:
                credentials.append({
                    'credential': credential,
                    'context': match.group(0)[:50]
                })
    
    return credentials