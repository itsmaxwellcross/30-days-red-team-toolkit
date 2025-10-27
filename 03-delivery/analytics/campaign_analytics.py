#!/usr/bin/env python3
"""
Campaign Analytics - Main Orchestrator
Coordinates all analytics modules
"""

import sqlite3
from .funnel_analyzer import FunnelAnalyzer
from .time_analyzer import TimeAnalyzer
from .department_analyzer import DepartmentAnalyzer
from .report_exporter import ReportExporter

class CampaignAnalytics:
    def __init__(self, db_path='phishing_campaign.db'):
        self.db = sqlite3.connect(db_path)
        self.funnel = FunnelAnalyzer(self.db)
        self.time = TimeAnalyzer(self.db)
        self.department = DepartmentAnalyzer(self.db)
        self.exporter = ReportExporter(self.db)
    
    def get_full_funnel_analysis(self):
        """Analyze the complete attack funnel"""
        return self.funnel.print_analysis()
    
    def get_time_analysis(self):
        """Analyze when victims interacted"""
        hourly = self.time.print_hourly_analysis()
        time_to_action = self.time.print_time_to_action()
        return {
            'hourly': hourly,
            'time_to_action': time_to_action
        }
    
    def get_department_analysis(self):
        """Analyze which departments were most susceptible"""
        departments = self.department.print_department_analysis()
        titles = self.department.print_title_analysis()
        return {
            'departments': departments,
            'titles': titles
        }
    
    def export_report(self, filename='campaign_report.json'):
        """Export comprehensive report"""
        return self.exporter.export_json(filename)
    
    def export_csv(self, filename='campaign_report.csv'):
        """Export CSV report"""
        return self.exporter.export_csv(filename)
    
    def export_html(self, filename='campaign_report.html'):
        """Export HTML report"""
        return self.exporter.export_html_report(filename)
    
    def export_credentials(self, filename='captured_credentials.csv'):
        """Export captured credentials"""
        return self.exporter.export_credentials_csv(filename)
    
    def get_complete_analysis(self):
        """Get all analytics data"""
        return {
            'funnel': self.funnel.analyze(),
            'time': self.time.analyze(),
            'department': self.department.analyze()
        }
    
    def print_full_report(self):
        """Print complete analytics report"""
        print("\n" + "="*60)
        print(" PHISHING CAMPAIGN ANALYTICS REPORT")
        print("="*60)
        
        self.get_full_funnel_analysis()
        self.get_time_analysis()
        self.get_department_analysis()
    
    def close(self):
        """Close database connection"""
        self.db.close()

# Standalone execution
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = 'phishing_campaign.db'
    
    analytics = CampaignAnalytics(db_path)
    analytics.print_full_report()
    analytics.close()