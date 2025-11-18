"""
Flag Validation System
Validates flag submissions and tracks progress
"""

import json
from pathlib import Path
from datetime import datetime


class FlagValidator:
    """
    Validates flags and tracks completion progress
    """
    
    def __init__(self, challenge_dir='06-integration/ctf_challenge'):
        self.challenge_dir = Path(challenge_dir)
        self.flag_file = self.challenge_dir / '.flags.json'
        self.progress_file = self.challenge_dir / '.progress.json'
        
        self.flags_data = self._load_flags()
        self.progress = self._load_progress()
    
    def _load_flags(self):
        """Load flag data"""
        if self.flag_file.exists():
            with open(self.flag_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_progress(self):
        """Load progress data"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {'flags_found': [], 'attempts': []}
    
    def _save_progress(self):
        """Save progress data"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def validate_flag(self, submitted_flag):
        """Validate a submitted flag"""
        # Record attempt
        self.progress['attempts'].append({
            'flag': submitted_flag,
            'timestamp': datetime.now().isoformat(),
            'valid': False
        })
        
        # Check against all flags
        for flag_id, flag_value in self.flags_data.get('flags', {}).items():
            if submitted_flag == flag_value:
                # Flag is correct
                flag_info = self.flags_data['flag_info'][flag_id]
                
                # Check if already found
                if flag_id not in self.progress['flags_found']:
                    self.progress['flags_found'].append({
                        'flag_id': flag_id,
                        'flag_value': flag_value,
                        'timestamp': datetime.now().isoformat(),
                        'flag_number': len(self.progress['flags_found']) + 1
                    })
                    
                    self.progress['attempts'][-1]['valid'] = True
                    self._save_progress()
                    
                    return {
                        'valid': True,
                        'flag_id': flag_id,
                        'flag_number': len(self.progress['flags_found']),
                        'name': flag_info['name'],
                        'description': flag_info['description'],
                        'points': flag_info['points'],
                        'already_found': False
                    }
                else:
                    return {
                        'valid': True,
                        'already_found': True,
                        'message': 'You already found this flag!'
                    }
        
        # Flag not found
        self._save_progress()
        return {
            'valid': False,
            'message': 'Invalid flag'
        }
    
    def show_progress(self):
        """Display current progress"""
        total_flags = len(self.flags_data.get('flags', {}))
        found_flags = len(self.progress['flags_found'])
        
        print("\n" + "="*70)
        print("CTF CHALLENGE PROGRESS")
        print("="*70)
        
        print(f"\nFlags Found: {found_flags}/{total_flags}")
        
        if found_flags > 0:
            total_points = sum(
                self.flags_data['flag_info'][f['flag_id']]['points'] 
                for f in self.progress['flags_found']
            )
            print(f"Points Earned: {total_points}/100")
            print(f"Completion: {(found_flags/total_flags*100):.1f}%")
            
            print("\n" + "-"*70)
            print("Flags Captured:")
            print("-"*70)
            
            for i, flag in enumerate(self.progress['flags_found'], 1):
                flag_info = self.flags_data['flag_info'][flag['flag_id']]
                timestamp = datetime.fromisoformat(flag['timestamp'])
                
                print(f"\n{i}. {flag_info['name']}")
                print(f"   Flag: {flag['flag_value']}")
                print(f"   Points: {flag_info['points']}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("\nNo flags found yet. Start with reconnaissance!")
        
        print("\n" + "="*70)
    
    def get_next_hint(self):
        """Get hint for next flag"""
        found_count = len(self.progress['flags_found'])
        
        hints = [
            "Check the HTML source code and robots.txt",
            "Try SQL injection on the login page: ' OR '1'='1",
            "Upload a PHP web shell through the file upload",
            "Enumerate the system: check config files in /var/www/html/",
            "Find SUID binaries and exploit them for privilege escalation",
            "Access /root/flag.txt as root user"
        ]
        
        if found_count < len(hints):
            return hints[found_count]
        return "All flags found! Congratulations!"
    
    def test_all_flags(self):
        """Test validation with all correct flags"""
        print("\n[*] Testing flag validation...")
        
        for flag_id, flag_value in self.flags_data.get('flags', {}).items():
            result = self.validate_flag(flag_value)
            flag_info = self.flags_data['flag_info'][flag_id]
            
            if result['valid']:
                print(f"[+] {flag_info['name']}: VALID")
            else:
                print(f"[-] {flag_info['name']}: FAILED")
        
        print("\n[*] Validation test complete")
    
    def get_statistics(self):
        """Get challenge statistics"""
        stats = {
            'total_flags': len(self.flags_data.get('flags', {})),
            'found_flags': len(self.progress['flags_found']),
            'total_attempts': len(self.progress['attempts']),
            'valid_attempts': sum(1 for a in self.progress['attempts'] if a['valid']),
            'invalid_attempts': sum(1 for a in self.progress['attempts'] if not a['valid'])
        }
        
        if stats['total_attempts'] > 0:
            stats['success_rate'] = (stats['valid_attempts'] / stats['total_attempts']) * 100
        else:
            stats['success_rate'] = 0
        
        if self.progress['flags_found']:
            first_flag = datetime.fromisoformat(self.progress['flags_found'][0]['timestamp'])
            last_flag = datetime.fromisoformat(self.progress['flags_found'][-1]['timestamp'])
            stats['time_elapsed'] = str(last_flag - first_flag)
        
        return stats