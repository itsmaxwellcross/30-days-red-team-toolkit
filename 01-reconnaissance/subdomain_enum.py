#!/usr/bin/env python3
import dns.resolver
import sys

def enumerate_subdomains(domain, wordlist):
    """
    Enumerate subdomains using DNS queries
    """
    found_subdomains = []
    
    with open(wordlist, 'r') as f:
        subdomains = f.read().splitlines()
    
    print(f"[*] Starting subdomain enumeration for {domain}")
    print(f"[*] Testing {len(subdomains)} subdomains...\n")
    
    for subdomain in subdomains:
        test_domain = f"{subdomain}.{domain}"
        try:
            # Try to resolve the subdomain
            answers = dns.resolver.resolve(test_domain, 'A')
            for rdata in answers:
                print(f"[+] Found: {test_domain} -> {rdata}")
                found_subdomains.append(test_domain)
        except dns.resolver.NXDOMAIN:
            # Subdomain doesn't exist
            pass
        except dns.resolver.NoAnswer:
            # Subdomain exists but no A record
            pass
        except Exception as e:
            # Other DNS errors
            pass
    
    return found_subdomains

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 subdomain_enum.py <domain> <wordlist>")
        print("Example: python3 subdomain_enum.py example.com subdomains.txt")
        sys.exit(1)
    
    domain = sys.argv[1]
    wordlist = sys.argv[2]
    
    results = enumerate_subdomains(domain, wordlist)
    
    print(f"\n[*] Enumeration complete. Found {len(results)} subdomains.")