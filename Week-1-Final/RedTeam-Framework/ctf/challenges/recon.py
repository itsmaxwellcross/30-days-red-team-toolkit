"""
Reconnaissance Challenge Creator
Tests information gathering skills
"""

from pathlib import Path


class ReconChallenge:
    """Creates reconnaissance challenge files"""
    
    def __init__(self, output_dir, flags):
        self.output_dir = Path(output_dir)
        self.flags = flags
    
    def create(self):
        """Create all reconnaissance challenge components"""
        self._create_index_html()
        self._create_robots_txt()
        self._create_git_exposure()
        self._create_hidden_files()
        print("[+] Created reconnaissance challenge")
    
    def _create_index_html(self):
        """Create main index page with hidden flag"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TargetCorp - Home</title>
    <!-- Flag 1: {self.flags['flag1_recon']} -->
    <!-- TODO: Remove before production! -->
    <!-- Remember to check robots.txt for disallowed paths -->
    <meta name="author" content="webmaster@targetcorp.local">
    <meta name="description" content="TargetCorp - Leading business solutions">
</head>
<body>
    <h1>Welcome to TargetCorp</h1>
    <p>We're a leading provider of business solutions and enterprise services.</p>
    
    <!-- Development note: Admin panel moved to /secret-admin-portal-2024 -->
    <!-- Old location: /admin (deprecated) -->
    
    <nav>
        <a href="/login">Admin Login</a> |
        <a href="/upload">File Upload</a> |
        <a href="/about.html">About Us</a> |
        <a href="/contact.html">Contact</a>
    </nav>
    
    <div style="display:none">
        <!-- Hidden contact information -->
        <p>Internal contacts:</p>
        <ul>
            <li>admin@targetcorp.local</li>
            <li>backup@targetcorp.local</li>
            <li>webmaster@targetcorp.local</li>
            <li>dev@targetcorp.local</li>
        </ul>
    </div>
    
    <footer>
        <p>&copy; 2024 TargetCorp. All rights reserved.</p>
        <p><small>Build version: 1.2.3 | Last updated: 2024-01-15</small></p>
    </footer>
</body>
</html>"""
        
        with open(self.output_dir / 'www' / 'index.html', 'w') as f:
            f.write(html)
    
    def _create_robots_txt(self):
        """Create robots.txt with hints"""
        robots = f"""# robots.txt for targetcorp.local
User-agent: *
Disallow: /admin/
Disallow: /backup/
Disallow: /secret-admin-portal-2024/
Disallow: /.git/
Disallow: /uploads/
Disallow: /config/

# Deprecated endpoints
Disallow: /old-admin/
Disallow: /test/

# Flag hint: Check the HTML source code for hidden comments!
# You're looking for: FLAG{{RECON_...}}

Sitemap: /sitemap.xml
"""
        
        with open(self.output_dir / 'www' / 'robots.txt', 'w') as f:
            f.write(robots)
    
    def _create_git_exposure(self):
        """Create exposed .git directory"""
        git_dir = self.output_dir / 'www' / '.git'
        git_dir.mkdir(exist_ok=True)
        
        # Git config
        config = """[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[remote "origin"]
    url = git@github.com:targetcorp/website.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master

# Exposed .git directory!
# Use git-dumper or similar tools to extract repository
"""
        
        with open(git_dir / 'config', 'w') as f:
            f.write(config)
        
        # Git HEAD
        with open(git_dir / 'HEAD', 'w') as f:
            f.write("ref: refs/heads/master\n")
    
    def _create_hidden_files(self):
        """Create hidden/backup files"""
        # Backup file
        backup = """<!DOCTYPE html>
<html>
<head><title>Old Admin Panel</title></head>
<body>
<h1>Deprecated Admin Panel</h1>
<p>This panel has been moved to a new location.</p>
<p>New location: /secret-admin-portal-2024</p>
<!-- Old credentials (DO NOT USE): admin / OldP@ss123 -->
</body>
</html>"""
        
        with open(self.output_dir / 'www' / 'admin.html.bak', 'w') as f:
            f.write(backup)
        
        # .DS_Store (Mac file)
        with open(self.output_dir / 'www' / '.DS_Store', 'wb') as f:
            f.write(b'\\x00\\x00\\x00\\x01')