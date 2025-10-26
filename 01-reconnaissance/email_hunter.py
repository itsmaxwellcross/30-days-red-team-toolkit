#!/usr/bin/env python3
import requests
import dns.resolver
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

class EmailHunter:
    def __init__(self, domain, company_name):
        self.domain = domain
        self.company_name = company_name
        self.emails = set()
        self.patterns = []
        
    def find_email_patterns(self):
        """
        Common email format patterns
        """
        return [
            '{first}.{last}@{domain}',
            '{first}{last}@{domain}',
            '{f}{last}@{domain}',
            '{first}@{domain}',
            '{first}_{last}@{domain}',
            '{last}@{domain}',
            '{first}{l}@{domain}'
        ]
    
    def search_github(self):
        """
        Search GitHub for email addresses
        """
        print("[*] Searching GitHub...")
        query = f'{self.domain} email'
        
        # GitHub search API would require authentication
        # This is a simplified example
        url = f'https://api.github.com/search/code?q={query}+in:file'
        
        try:
            # Note: Real implementation needs GitHub API token
            print("    [!] GitHub API requires authentication")
            print("    [!] Implement with: export GITHUB_TOKEN=your_token")
        except Exception as e:
            print(f"    [-] Error: {e}")
    
    def search_hunter_io(self):
        """
        Use Hunter.io API to find emails (requires API key)
        """
        print("[*] Hunter.io lookup...")
        print("    [!] Requires API key from hunter.io")
        print("    [!] Free tier: 25 requests/month")
        
        # Example implementation:
        # api_key = "your_hunter_io_key"
        # url = f"https://api.hunter.io/v2/domain-search?domain={self.domain}&api_key={api_key}"
        # response = requests.get(url)
        # Parse response for emails
    
    def generate_permutations(self, first_name, last_name):
        """
        Generate email permutations based on name
        """
        patterns = self.find_email_patterns()
        emails = []
        
        for pattern in patterns:
            email = pattern.format(
                first=first_name.lower(),
                last=last_name.lower(),
                f=first_name[0].lower(),
                l=last_name[0].lower(),
                domain=self.domain
            )
            emails.append(email)
        
        return emails
    
    def verify_email_smtp(self, email):
        """
        Verify if email exists via SMTP (basic check)
        Note: Many servers block this now
        """
        try:
            domain = email.split('@')[1]
            
            # Get MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_host = str(mx_records[0].exchange)
            
            # In a real implementation, you would:
            # 1. Connect to SMTP server
            # 2. Send VRFY or RCPT TO command
            # 3. Check response code
            
            return True  # Placeholder
        except:
            return False
    
    def search_linkedin(self):
        """
        Search LinkedIn for employees (requires LinkedIn account)
        """
        print(f"[*] LinkedIn enumeration for {self.company_name}...")
        print("    [!] Manual step: Search LinkedIn for:")
        print(f"    [!] https://www.linkedin.com/search/results/people/?keywords={self.company_name}")
        print("    [!] Note employee names and titles")
        
        # Example employee list you'd gather manually
        example_employees = [
            ("John", "Doe", "Senior Developer"),
            ("Jane", "Smith", "Security Engineer"),
            ("Bob", "Johnson", "IT Manager")
        ]
        
        print("\n[*] Generating email permutations for example employees:")
        for first, last, title in example_employees:
            emails = self.generate_permutations(first, last)
            print(f"\n    {first} {last} ({title}):")
            for email in emails:
                print(f"        • {email}")
                self.emails.add(email)
    
    def check_haveibeenpwned(self, email):
        """
        Check if email appears in data breaches
        """
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'hibp-api-key': 'your_api_key_here'  # Get free API key from haveibeenpwned.com
        }
        
        try:
            # Note: Requires API key for automated checks
            print(f"    [!] Check manually: https://haveibeenpwned.com/account/{email}")
        except Exception as e:
            pass
    
    def search_pastebin(self):
        """
        Search paste sites for leaked credentials
        """
        print("[*] Checking paste sites...")
        print(f"    [!] Manual search recommended:")
        print(f"    [!] https://psbdmp.ws/?q={self.domain}")
        print(f"    [!] https://ghostproject.fr/")
        print("    [!] Look for credential dumps containing your domain")
    
    def run_full_enumeration(self):
        """
        Run all enumeration techniques
        """
        print(f"[*] Starting email enumeration for {self.domain}")
        print("=" * 50 + "\n")
        
        self.search_linkedin()
        print()
        self.search_github()
        print()
        self.search_hunter_io()
        print()
        self.search_pastebin()
        
        print(f"\n[+] Found/Generated {len(self.emails)} potential email addresses")
        return list(self.emails)

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 email_hunter.py <domain> <company_name>")
        print("Example: python3 email_hunter.py example.com 'Example Corp'")
        sys.exit(1)
    
    domain = sys.argv[1]
    company = sys.argv[2]
    
    hunter = EmailHunter(domain, company)
    emails = hunter.run_full_enumeration()
    
    # Save results
    with open(f'{domain}_emails.txt', 'w') as f:
        for email in emails:
            f.write(email + '\n')
    
    print(f"\n[+] Results saved to {domain}_emails.txt")