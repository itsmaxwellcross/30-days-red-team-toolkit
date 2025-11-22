"""
Service wrapper creation for non-service binaries
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    run_command,
    check_admin,
    check_dotnet_compiler,
    escape_command_for_wrapper
)
from config import (
    SERVICE_WRAPPER_TEMPLATE,
    OUTPUT_PATHS
)
from methods.create import create_service

def create_service_wrapper(service_name, command):
    """
    Create C# service wrapper code
    
    Args:
        service_name (str): Service name
        command (str): Command to execute
        
    Returns:
        tuple: (source_code, source_path, binary_path)
    """
    print(f"[*] Generating service wrapper for: {service_name}")
    
    # Escape command for C#
    escaped_command = escape_command_for_wrapper(command)
    
    # Generate class name (remove spaces, special chars)
    class_name = ''.join(c for c in service_name if c.isalnum())
    
    # Generate source code from template
    source_code = SERVICE_WRAPPER_TEMPLATE.format(
        class_name=class_name,
        service_name=service_name,
        command=escaped_command
    )
    
    # Determine file paths
    source_path = OUTPUT_PATHS['wrapper_source'].format(service_name=service_name)
    binary_path = OUTPUT_PATHS['wrapper_binary'].format(service_name=service_name)
    
    print(f"[+] Wrapper code generated")
    print(f"    Source: {source_path}")
    print(f"    Binary: {binary_path}")
    
    return source_code, source_path, binary_path

def compile_wrapper(source_path, binary_path):
    """
    Compile C# wrapper to executable
    
    Args:
        source_path (str): Path to .cs source file
        binary_path (str): Output .exe path
        
    Returns:
        dict: Compilation result
    """
    print(f"[*] Compiling service wrapper...")
    
    # Find .NET compiler
    compiler_path = check_dotnet_compiler()
    
    if not compiler_path:
        print("[-] .NET Framework compiler not found")
        return {
            'success': False,
            'error': '.NET Framework compiler (csc.exe) not found'
        }
    
    print(f"[*] Using compiler: {compiler_path}")
    
    # Compile command
    compile_cmd = (
        f'"{compiler_path}" '
        f'/out:"{binary_path}" '
        f'/target:exe '
        f'/reference:System.ServiceProcess.dll '
        f'"{source_path}"'
    )
    
    result = run_command(compile_cmd, timeout=60)
    
    if result['success'] and os.path.exists(binary_path):
        print(f"[+] Wrapper compiled successfully")
        print(f"    Output: {binary_path}")
        return {
            'success': True,
            'binary_path': binary_path
        }
    else:
        error_msg = result.get('stderr', 'Unknown compilation error')
        print(f"[-] Compilation failed: {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }

def create_wrapped_service(service_name, command, display_name=None, description=None):
    """
    Create complete service with wrapper (for non-service binaries)
    
    Args:
        service_name (str): Service name
        command (str): Command to execute
        display_name (str): Display name
        description (str): Description
        
    Returns:
        dict: Complete result with all information
    """
    print(f"\n[*] Creating wrapped service: {service_name}")
    print(f"[*] Command: {command}")
    
    # Check admin privileges
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Step 1: Generate wrapper code
    source_code, source_path, binary_path = create_service_wrapper(
        service_name, 
        command
    )
    
    # Step 2: Write source code to file
    try:
        with open(source_path, 'w') as f:
            f.write(source_code)
        print(f"[+] Wrapper source saved: {source_path}")
    except Exception as e:
        print(f"[-] Failed to write source file: {e}")
        return {
            'success': False,
            'error': f'Failed to write source file: {e}'
        }
    
    # Step 3: Compile wrapper
    compile_result = compile_wrapper(source_path, binary_path)
    
    if not compile_result['success']:
        return compile_result
    
    # Step 4: Create service with compiled wrapper
    service_result = create_service(
        service_name=service_name,
        binary_path=binary_path,
        display_name=display_name,
        description=description
    )
    
    if service_result['success']:
        # Add wrapper-specific information
        service_result['wrapper'] = {
            'command': command,
            'source_path': source_path,
            'binary_path': binary_path
        }
        
        print(f"\n[+] Wrapped service created successfully!")
        print(f"[+] Service Name: {service_name}")
        print(f"[+] Wrapper Binary: {binary_path}")
        print(f"[+] Executing: {command}")
    
    return service_result

def cleanup_wrapper_files(service_name):
    """
    Clean up wrapper source and binary files
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Cleanup result
    """
    print(f"[*] Cleaning up wrapper files...")
    
    source_path = OUTPUT_PATHS['wrapper_source'].format(service_name=service_name)
    binary_path = OUTPUT_PATHS['wrapper_binary'].format(service_name=service_name)
    
    removed = []
    errors = []
    
    for path in [source_path, binary_path]:
        if os.path.exists(path):
            try:
                os.remove(path)
                removed.append(path)
                print(f"[+] Removed: {path}")
            except Exception as e:
                errors.append(f"Failed to remove {path}: {e}")
                print(f"[-] {errors[-1]}")
    
    return {
        'success': len(errors) == 0,
        'removed': removed,
        'errors': errors
    }

def list_wrapper_files():
    """
    List all existing wrapper files in public directory
    
    Returns:
        dict: Lists of source and binary files
    """
    public_dir = r'C:\Users\Public'
    
    if not os.path.exists(public_dir):
        return {
            'source_files': [],
            'binary_files': []
        }
    
    source_files = []
    binary_files = []
    
    for filename in os.listdir(public_dir):
        if filename.endswith('.cs'):
            source_files.append(os.path.join(public_dir, filename))
        elif filename.endswith('.exe'):
            # Check if it might be a wrapper (has corresponding .cs)
            base_name = filename[:-4]
            if os.path.exists(os.path.join(public_dir, f"{base_name}.cs")):
                binary_files.append(os.path.join(public_dir, filename))
    
    return {
        'source_files': source_files,
        'binary_files': binary_files
    }