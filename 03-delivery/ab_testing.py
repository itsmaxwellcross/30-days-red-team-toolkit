#!/usr/bin/env python3
"""
A/B Testing for Phishing Templates
Send different versions to split audience
"""

class PhishingABTest:
    def __init__(self, targets):
        self.targets = targets
        self.groups = self.split_targets(2)
    
    def split_targets(self, num_groups):
        """Split targets into groups for testing"""
        import random
        shuffled = self.targets.copy()
        random.shuffle(shuffled)
        
        group_size = len(shuffled) // num_groups
        return [shuffled[i*group_size:(i+1)*group_size] 
                for i in range(num_groups)]
    
    def test_urgency_levels(self):
        """Test high urgency vs low urgency"""
        
        template_a = {
            'name': 'High Urgency',
            'subject': 'URGENT: Account Suspended - Immediate Action Required',
            'urgency_words': ['URGENT', 'Immediate', 'within 2 hours']
        }
        
        template_b = {
            'name': 'Low Urgency',
            'subject': 'Please Review: Account Security Update Available',
            'urgency_words': ['Please', 'when convenient', 'at your earliest']
        }
        
        print("[*] A/B Test: Urgency Levels")
        print(f"    Group A ({len(self.groups[0])} targets): {template_a['name']}")
        print(f"    Group B ({len(self.groups[1])} targets): {template_b['name']}")
    
    def test_sender_types(self):
        """Test internal vs external sender"""
        
        template_a = {
            'name': 'Internal Sender',
            'from': 'IT Support <support@company.com>'
        }
        
        template_b = {
            'name': 'External Sender',
            'from': 'Microsoft Security <security@microsoft.com>'
        }
        
        print("[*] A/B Test: Sender Types")
        print(f"    Group A: {template_a['from']}")
        print(f"    Group B: {template_b['from']}")