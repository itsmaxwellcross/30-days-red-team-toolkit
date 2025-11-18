"""
CTF Challenge Web Server
Serves challenge files and handles interactions
"""

import http.server
import socketserver
import os
import json
from urllib.parse import parse_qs
from pathlib import Path
from urllib.parse import parse_qs, urlparse


class CTFRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for CTF challenge"""
    
    def __init__(self, *args, challenge_dir=None, flags=None, **kwargs):
        self.challenge_dir = Path(challenge_dir) if challenge_dir else Path('06-integration/ctf_challenge')
        self.flags = flags or self._load_flags()
        super().__init__(*args, directory=str(self.challenge_dir / 'www'), **kwargs)
    
    def _load_flags(self):
        """Load flags from file"""
        flag_file = self.challenge_dir / '.flags.json'
        if flag_file.exists():
            with open(flag_file, 'r') as f:
                data = json.load(f)
                return data['flags']
        return {}
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route requests
        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/robots.txt':
            self.serve_robots()
        elif path == '/login.php' or path == '/login':
            self.serve_login()
        elif path == '/upload.php' or path == '/upload':
            self.serve_upload()
        elif path == '/admin' or path == '/secret-admin-portal-2024':
            self.serve_admin()
        elif path.startswith('/uploads/'):
            self.serve_upload_file(path)
        else:
            # Serve static file
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/login.php' or path == '/login':
            self.handle_login()
        elif path == '/upload.php' or path == '/upload':
            self.handle_upload()
        elif path == '/validate_flag':
            self.handle_flag_validation()
        else:
            self.send_error(404, "Not Found")
    
    def serve_index(self):
        """Serve main index page"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>TargetCorp - Home</title>
    <meta charset="utf-8">
    <!-- Flag 1: {self.flags.get('flag1_recon', 'FLAG{PLACEHOLDER}')} -->
    <!-- Remember to check robots.txt and hidden directories! -->
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        .nav {{ margin: 20px 0; }}
        .nav a {{ margin-right: 15px; color: #0066cc; text-decoration: none; }}
        .nav a:hover {{ text-decoration: underline; }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to TargetCorp</h1>
        <p>We're a leading provider of business solutions and enterprise services.</p>
        
        <div class="nav">
            <a href="/login">Admin Login</a>
            <a href="/upload">File Upload</a>
            <a href="/about.html">About Us</a>
        </div>
        
        <!-- Development note: admin panel at /secret-admin-portal-2024 -->
        
        <div class="hidden">
            <p>Internal contacts:</p>
            <ul>
                <li>admin@targetcorp.local</li>
                <li>backup@targetcorp.local</li>
                <li>webmaster@targetcorp.local</li>
            </ul>
        </div>
        
        <hr>
        <p><small>&copy; 2024 TargetCorp. All rights reserved.</small></p>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_robots(self):
        """Serve robots.txt"""
        robots = """User-agent: *
Disallow: /admin/
Disallow: /backup/
Disallow: /secret-admin-portal-2024/
Disallow: /.git/

# Flag hint: Look in the HTML source code!
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(robots.encode())
    
    def serve_login(self):
        """Serve login page"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Admin Login - TargetCorp</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
        .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }}
        input[type="submit"] {{ background: #0066cc; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }}
        input[type="submit"]:hover {{ background: #0052a3; }}
        .hint {{ color: #666; font-size: 12px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Admin Panel Login</h2>
        <form method="POST" action="/login">
            <label>Username:</label>
            <input type="text" name="username" required>
            
            <label>Password:</label>
            <input type="password" name="password" required>
            
            <input type="submit" value="Login">
        </form>
        <p class="hint">Hint: Try SQL injection techniques</p>
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_login(self):
        """Handle login POST request"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]
        
        # Check for SQL injection
        sql_payloads = ["' OR '1'='1", "' or '1'='1", "admin' --", "admin' #"]
        
        if any(payload in username or payload in password for payload in sql_payloads):
            # Successful SQL injection
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Login Successful</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        .success {{ color: green; font-weight: bold; }}
        .flag {{ background: #ffffcc; padding: 15px; border-radius: 4px; font-family: monospace; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h2 class="success">✓ Login Successful!</h2>
        <p>SQL Injection detected and exploited successfully!</p>
        
        <div class="flag">
            <strong>Flag 2:</strong> {self.flags.get('flag2_exploit', 'FLAG{PLACEHOLDER}')}
        </div>
        
        <p>Congratulations! You've found Flag 2.</p>
        <p><a href="/upload">Continue to File Upload</a></p>
    </div>
</body>
</html>"""
        else:
            # Failed login
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Login Failed</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2 class="error">✗ Login Failed</h2>
        <p>Invalid credentials. Try SQL injection techniques.</p>
        <p><a href="/login">Try Again</a></p>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_upload(self):
        """Serve upload page"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>File Upload - TargetCorp</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        input[type="file"] { margin: 15px 0; }
        input[type="submit"] { background: #0066cc; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .hint { color: #666; font-size: 12px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>File Upload</h2>
        <p>Upload files for processing</p>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br>
            <input type="submit" value="Upload">
        </form>
        <p class="hint">Hint: Try uploading a PHP web shell with extension bypass</p>
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_upload(self):
        """Handle file upload"""
        content_type = self.headers['Content-Type']
        
        if 'multipart/form-data' not in content_type:
            self.send_error(400, "Bad Request")
            return
        
        # Parse multipart form data
        form = parse_qs.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        if 'file' in form:
            fileitem = form['file']
            filename = fileitem.filename
            
            # Save file
            upload_dir = self.challenge_dir / 'www' / 'uploads'
            upload_dir.mkdir(exist_ok=True)
            
            filepath = upload_dir / filename
            with open(filepath, 'wb') as f:
                f.write(fileitem.file.read())
            
            # Check if it's a web shell
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
                if 'FLAG{SHELL' in content or self.flags.get('flag3_shell') in content:
                    flag_found = True
                else:
                    flag_found = False
            
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Upload Success</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        .success {{ color: green; }}
        .flag {{ background: #ffffcc; padding: 15px; border-radius: 4px; font-family: monospace; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h2 class="success">✓ File Uploaded Successfully</h2>
        <p>File saved to: <code>/uploads/{filename}</code></p>
        <p>Access at: <a href="/uploads/{filename}">/uploads/{filename}</a></p>
        
        {'<div class="flag"><strong>Flag 3:</strong> ' + self.flags.get('flag3_shell', 'FLAG{PLACEHOLDER}') + '</div>' if flag_found else ''}
        
        <p><a href="/upload">Upload Another File</a></p>
    </div>
</body>
</html>"""
        else:
            html = """<!DOCTYPE html>
<html><body><h2>No file uploaded</h2><p><a href="/upload">Try Again</a></p></body></html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_admin(self):
        """Serve admin panel"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Secret Admin Portal</h2>
        <p>You found the hidden admin portal! Good reconnaissance work.</p>
        <p>Try logging in through the <a href="/login">login page</a>.</p>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_upload_file(self, path):
        """Serve uploaded files"""
        # Serve files from uploads directory
        super().do_GET()


class CTFServer:
    """
    CTF Challenge Server
    """
    
    def __init__(self, challenge_dir, host='0.0.0.0', port=8080):
        self.challenge_dir = Path(challenge_dir)
        self.host = host
        self.port = port
        self.flags = self._load_flags()
    
    def _load_flags(self):
        """Load flags"""
        flag_file = self.challenge_dir / '.flags.json'
        if flag_file.exists():
            with open(flag_file, 'r') as f:
                data = json.load(f)
                return data['flags']
        return {}
    
    def start(self):
        """Start the server"""
        handler = lambda *args, **kwargs: CTFRequestHandler(
            *args, 
            challenge_dir=self.challenge_dir,
            flags=self.flags,
            **kwargs
        )
        
        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            print(f"[+] Server started successfully")
            print(f"[+] Challenge URL: http://localhost:{self.port}")
            print(f"[+] Press Ctrl+C to stop\n")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[*] Shutting down server...")
                httpd.shutdown()