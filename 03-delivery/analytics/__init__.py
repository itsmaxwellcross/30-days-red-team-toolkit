"""
Campaign Analytics Package
Modular analytics for phishing campaigns
"""

from .funnel_analyzer import FunnelAnalyzer
from .time_analyzer import TimeAnalyzer
from .department_analyzer import DepartmentAnalyzer
from .report_exporter import ReportExporter
from .campaign_analytics import CampaignAnalytics

__all__ = [
    'FunnelAnalyzer',
    'TimeAnalyzer',
    'DepartmentAnalyzer',
    'ReportExporter',
    'CampaignAnalytics'
]