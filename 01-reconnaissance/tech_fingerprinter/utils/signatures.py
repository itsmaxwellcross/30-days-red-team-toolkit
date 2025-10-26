#!/usr/bin/env python3
"""
Technology detection signatures
"""

class TechnologySignatures:
    """Container for technology detection patterns"""
    
    @staticmethod
    def get_cms_signatures():
        """CMS detection patterns"""
        return {
            'WordPress': {
                'html_patterns': ['wp-content', 'wp-includes', 'wp-json'],
                'version_regex': r'wp-includes/.*?ver=([\d.]+)'
            },
            'Drupal': {
                'html_patterns': ['Drupal', '/sites/all/', 'drupal.js'],
                'meta_generator': 'Drupal'
            },
            'Joomla': {
                'html_patterns': ['/components/com_', 'Joomla', '/media/jui/'],
                'meta_generator': 'Joomla'
            },
            'Magento': {
                'html_patterns': ['/skin/frontend/', 'Mage.', 'varien/'],
                'cookies': ['frontend']
            },
            'Shopify': {
                'html_patterns': ['cdn.shopify.com', 'Shopify'],
                'headers': ['X-ShopId']
            }
        }
    
    @staticmethod
    def get_framework_signatures():
        """Framework detection patterns"""
        return {
            'ASP.NET': {
                'headers': ['X-AspNet-Version', 'X-AspNetMvc-Version'],
                'cookies': ['ASP.NET_SessionId']
            },
            'Laravel': {
                'cookies': ['laravel_session'],
                'headers': ['X-Laravel-Session']
            },
            'Django': {
                'cookies': ['django', 'csrftoken'],
                'headers': ['X-Django-Version']
            },
            'Ruby on Rails': {
                'cookies': ['_rails_session'],
                'headers': ['X-Runtime']
            },
            'Spring': {
                'cookies': ['JSESSIONID'],
                'headers': ['X-Application-Context']
            }
        }
    
    @staticmethod
    def get_server_signatures():
        """Web server detection patterns"""
        return {
            'nginx': ['nginx'],
            'Apache': ['Apache'],
            'IIS': ['Microsoft-IIS', 'Microsoft-HTTPAPI'],
            'LiteSpeed': ['LiteSpeed'],
            'Caddy': ['Caddy']
        }