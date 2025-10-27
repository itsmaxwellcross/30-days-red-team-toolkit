#!/usr/bin/env python3
"""
Report Exporter
Exports campaign data to various formats
"""

import sqlite3
import json
import csv
from datetime import datetime

class ReportExporter:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_target_details(self):
        """Get detailed information for each target"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            SELECT t.email, t.name, t.title, t.department, t.token,
                   COUNT(DISTINCT CASE WHEN e.event_type = 'email_opened' THEN e.id END) as opened,
                   COUNT(DISTINCT CASE WHEN e.event_type = 'link_clicked' THEN e.id END) as clicked,
                   COUNT(DISTINCT c.id) as submitted,
                   MIN(CASE WHEN e.event_type = 'email_opened' THEN e.timestamp END) as first_open,
                   MIN(CASE WHEN e.event_type = 'link_clicked' THEN e.timestamp END) as first_click
            FROM targets t
            LEFT JOIN events e ON t.id = e.target_id
            LEFT JOIN credentials c ON t.id = c.target_id
            GROUP BY t.id
        ''')
        
        targets = []
        for row in cursor.fetchall():
            targets.append({
                'email': row[0],
                'name': row[1],
                'title': row[2],
                'department': row[3],
                'token': row[4],
                'opened': row[5] > 0,
                'clicked': row[6] > 0,
                'submitted': row[7] > 0,
                'first_open': row[8],
                'first_click': row[9]
            })
        
        return targets
    
    def get_captured_credentials(self):
        """Get all captured credentials"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            SELECT t.email, t.name, c.username, c.password, c.timestamp
            FROM credentials c
            JOIN targets t ON c.target_id = t.id
            ORDER BY c.timestamp
        ''')
        
        credentials = []
        for row in cursor.fetchall():
            credentials.append({
                'target_email': row[0],
                'target_name': row[1],
                'username': row[2],
                'password': row[3],
                'timestamp': row[4]
            })
        
        return credentials
    
    def export_json(self, filename='campaign_report.json', include_credentials=True):
        """Export comprehensive JSON report"""
        targets = self.get_target_details()
        
        report = {
            'campaign_date': datetime.now().isoformat(),
            'total_targets': len(targets),
            'targets': targets
        }
        
        if include_credentials:
            report['captured_credentials'] = self.get_captured_credentials()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[+] JSON report exported to: {filename}")
        return report
    
    def export_csv(self, filename='campaign_report.csv'):
        """Export target summary to CSV"""
        targets = self.get_target_details()
        
        with open(filename, 'w', newline='') as f:
            fieldnames = ['email', 'name', 'title', 'department', 
                         'opened', 'clicked', 'submitted']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for target in targets:
                writer.writerow({
                    'email': target['email'],
                    'name': target['name'],
                    'title': target['title'],
                    'department': target['department'],
                    'opened': target['opened'],
                    'clicked': target['clicked'],
                    'submitted': target['submitted']
                })
        
        print(f"\n[+] CSV report exported to: {filename}")
    
    def export_credentials_csv(self, filename='captured_credentials.csv'):
        """Export captured credentials to CSV"""
        credentials = self.get_captured_credentials()
        
        if not credentials:
            print("\n[*] No credentials to export")
            return
        
        with open(filename, 'w', newline='') as f:
            fieldnames = ['target_email', 'target_name', 'username', 
                         'password', 'timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for cred in credentials:
                writer.writerow(cred)
        
        print(f"\n[+] Credentials exported to: {filename}")
        print(f"[!] WARNING: This file contains sensitive data - secure appropriately!")
    
    def export_html_report(self, filename='campaign_report.html'):
        """Export HTML formatted report"""
        targets = self.get_target_details()
        
        # Calculate statistics
        total = len(targets)
        opened = sum(1 for t in targets if t['opened'])
        clicked = sum(1 for t in targets if t['clicked'])
        submitted = sum(1 for t in targets if t['submitted'])
        
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Campaign Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        .stat {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
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
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        .success {{ color: #28a745; }}
        .danger {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Phishing Campaign Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total Targets</div>
            </div>
            <div class="stat">
                <div class="stat-number">{opened} ({opened/total*100:.1f}%)</div>
                <div class="stat-label">Emails Opened</div>
            </div>
            <div class="stat">
                <div class="stat-number">{clicked} ({clicked/total*100:.1f}%)</div>
                <div class="stat-label">Links Clicked</div>
            </div>
            <div class="stat">
                <div class="stat-number">{submitted} ({submitted/total*100:.1f}%)</div>
                <div class="stat-label">Credentials Submitted</div>
            </div>
        </div>
        
        <h2>Target Details</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Opened</th>
                <th>Clicked</th>
                <th>Submitted</th>
            </tr>
'''
        
        for target in targets:
            html += f'''
            <tr>
                <td>{target['name']}</td>
                <td>{target['email']}</td>
                <td>{target['department'] or 'N/A'}</td>
                <td class="{'success' if target['opened'] else 'danger'}">{'✓' if target['opened'] else '✗'}</td>
                <td class="{'success' if target['clicked'] else 'danger'}">{'✓' if target['clicked'] else '✗'}</td>
                <td class="{'success' if target['submitted'] else 'danger'}">{'✓' if target['submitted'] else '✗'}</td>
            </tr>
'''
        
        html += '''
        </table>
    </div>
</body>
</html>
'''
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"\n[+] HTML report exported to: {filename}")