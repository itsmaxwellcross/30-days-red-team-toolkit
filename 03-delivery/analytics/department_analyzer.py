#!/usr/bin/env python3
"""
Department Analysis
Analyzes which departments were most susceptible
"""

import sqlite3

class DepartmentAnalyzer:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_department_stats(self):
        """Get statistics by department"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            SELECT t.department, 
                   COUNT(DISTINCT t.id) as total_count,
                   COUNT(DISTINCT CASE WHEN e.event_type = 'email_opened' THEN t.id END) as opened_count,
                   COUNT(DISTINCT CASE WHEN e.event_type = 'link_clicked' THEN t.id END) as clicked_count,
                   COUNT(DISTINCT c.target_id) as submitted_count
            FROM targets t
            LEFT JOIN events e ON t.id = e.target_id
            LEFT JOIN credentials c ON t.id = c.target_id
            WHERE t.department IS NOT NULL AND t.department != ''
            GROUP BY t.department
        ''')
        
        departments = []
        for row in cursor.fetchall():
            dept, total, opened, clicked, submitted = row
            departments.append({
                'department': dept,
                'total': total,
                'opened': opened,
                'clicked': clicked,
                'submitted': submitted,
                'open_rate': (opened / total * 100) if total > 0 else 0.0,
                'click_rate': (clicked / total * 100) if total > 0 else 0.0,
                'submit_rate': (submitted / total * 100) if total > 0 else 0.0
            })
        
        return departments
    
    def get_title_stats(self):
        """Get statistics by job title"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            SELECT t.title, 
                   COUNT(DISTINCT t.id) as total_count,
                   COUNT(DISTINCT c.target_id) as submitted_count
            FROM targets t
            LEFT JOIN credentials c ON t.id = c.target_id
            WHERE t.title IS NOT NULL AND t.title != ''
            GROUP BY t.title
        ''')
        
        titles = []
        for row in cursor.fetchall():
            title, total, submitted = row
            titles.append({
                'title': title,
                'total': total,
                'submitted': submitted,
                'submit_rate': (submitted / total * 100) if total > 0 else 0.0
            })
        
        return titles
    
    def get_most_vulnerable_department(self):
        """Identify most vulnerable department"""
        departments = self.get_department_stats()
        
        if not departments:
            return None
        
        return max(departments, key=lambda d: d['submit_rate'])
    
    def get_least_vulnerable_department(self):
        """Identify least vulnerable department"""
        departments = self.get_department_stats()
        
        if not departments:
            return None
        
        return min(departments, key=lambda d: d['submit_rate'])
    
    def analyze(self):
        """Perform complete department analysis"""
        return {
            'by_department': self.get_department_stats(),
            'by_title': self.get_title_stats(),
            'most_vulnerable': self.get_most_vulnerable_department(),
            'least_vulnerable': self.get_least_vulnerable_department()
        }
    
    def print_department_analysis(self):
        """Print formatted department analysis"""
        departments = self.get_department_stats()
        
        if not departments:
            print("\n[*] No department data available")
            return
        
        print("\n[*] Success Rate by Department:")
        print("="*60)
        for dept in sorted(departments, key=lambda d: d['submit_rate'], reverse=True):
            print(f"    {dept['department']:<20} {dept['submitted']}/{dept['total']} ({dept['submit_rate']:.1f}%)")
        
        # Print most/least vulnerable
        most_vuln = self.get_most_vulnerable_department()
        least_vuln = self.get_least_vulnerable_department()
        
        if most_vuln:
            print(f"\n    Most Vulnerable:  {most_vuln['department']} ({most_vuln['submit_rate']:.1f}%)")
        if least_vuln:
            print(f"    Least Vulnerable: {least_vuln['department']} ({least_vuln['submit_rate']:.1f}%)")
        
        return departments
    
    def print_title_analysis(self):
        """Print formatted title analysis"""
        titles = self.get_title_stats()
        
        if not titles:
            print("\n[*] No title data available")
            return
        
        print("\n[*] Success Rate by Job Title:")
        print("="*60)
        for title in sorted(titles, key=lambda t: t['submit_rate'], reverse=True):
            print(f"    {title['title']:<30} {title['submitted']}/{title['total']} ({title['submit_rate']:.1f}%)")
        
        return titles