#!/usr/bin/env python3
import requests
import time
import sys
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

class GoogleDorker:
    def __init__(self, domain, delay=2):
        self.domain = domain
        self.delay = delay  # Delay between requests to avoid rate limiting
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        self.results = []
    
    def build_dork(self, dork_type):
        """
        Build Google dork queries for different reconnaissance objectives
        """
        dorks = {
            'subdomains': f'site:*.{self.domain} -site:www.{self.domain}',
            'files': f'site:{self.domain} (ext:pdf OR ext:doc OR ext:docx OR ext:xls OR ext:xlsx OR ext:ppt OR ext:pptx)',
            'logins': f'site:{self.domain} (inurl:login OR inurl:admin OR inurl:portal OR inurl:signin)',
            'directories': f'site:{self.domain} intitle:"index of"',
            'configs': f'site:{self.domain} (ext:xml OR ext:conf OR ext:cnf OR ext:reg OR ext:inf OR ext:rdp OR ext:cfg OR ext:txt OR ext:ora OR ext:ini)',
            'databases': f'site:{self.domain} (ext:sql OR ext:dbf OR ext:mdb)',
            'backup_files': f'site:{self.domain} (ext:bkf OR ext:bkp OR ext:bak OR ext:old OR ext:backup)',
            'exposed_docs': f'site:{self.domain} (confidential OR "not for distribution" OR "internal only")',
            'employee_info': f'site:linkedin.com "{self.domain}" employees',
            'tech_stack': f'site:{self.domain} (powered by OR built with OR running)',
            'errors': f'site:{self.domain} (warning OR error OR exception OR "stack trace")',
            'credentials': f'site:{self.domain} (password OR passwd OR pwd OR pass)'
        }
        return dorks.get(dork_type, '')
    
    def search(self, query, num_results=10):
        """
        Perform Google search and parse results
        """
        encoded_query = quote_plus(query)
        url = f'https://www.google.com/search?q={encoded_query}&num={num_results}'
        
        headers = {'User-Agent': self.user_agent}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse search results
            results = []
            for result in soup.find_all('div', class_='g'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    href = link['href']
                    if href.startswith('/url?q='):
                        href = href.split('/url?q=')[1].split('&')[0]
                    
                    title_elem = result.find('h3')
                    title = title_elem.text if title_elem else 'No title'
                    
                    results.append({
                        'title': title,
                        'url': href
                    })
            
            return results
        except Exception as e:
            print(f"[-] Error searching: {e}")
            return []
    
    def run_all_dorks(self):
        """
        Run all dork types and collect results
        """
        dork_types = [
            'subdomains', 'files', 'logins', 'directories', 
            'configs', 'databases', 'backup_files', 'exposed_docs',
            'tech_stack', 'errors', 'credentials'
        ]
        
        print(f"[*] Starting Google dorking for {self.domain}")
        print(f"[*] Running {len(dork_types)} different dork types...\n")
        
        all_results = {}
        
        for dork_type in dork_types:
            query = self.build_dork(dork_type)
            print(f"[*] Searching: {dork_type}")
            print(f"    Query: {query}")
            
            results = self.search(query, num_results=10)
            all_results[dork_type] = results
            
            if results:
                print(f"    [+] Found {len(results)} results")
                for result in results[:3]:  # Show first 3
                    print(f"        • {result['title']}")
            else:
                print(f"    [-] No results found")
            
            print()
            time.sleep(self.delay)  # Rate limiting
        
        return all_results
    
    def save_results(self, results, filename):
        """
        Save results to a file
        """
        with open(filename, 'w') as f:
            f.write(f"Google Dorking Results for {self.domain}\n")
            f.write("=" * 50 + "\n\n")
            
            for dork_type, dork_results in results.items():
                f.write(f"\n{dork_type.upper()}\n")
                f.write("-" * 50 + "\n")
                
                if dork_results:
                    for result in dork_results:
                        f.write(f"Title: {result['title']}\n")
                        f.write(f"URL: {result['url']}\n\n")
                else:
                    f.write("No results found\n\n")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 google_dorker.py <domain>")
        print("Example: python3 google_dorker.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    dorker = GoogleDorker(domain, delay=3)  # 3 second delay between searches
    
    results = dorker.run_all_dorks()
    dorker.save_results(results, f'{domain}_dork_results.txt')
    
    print(f"\n[+] Dorking complete! Results saved to {domain}_dork_results.txt")