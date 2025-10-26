#!/usr/bin/env python3
import requests
import ssl
import socket
from urllib.parse import urlparse

def check_web_service(subdomain):
    """
    Check if subdomain runs a web service and gather basic info
    """
    results = {}
    
    for protocol in ['https', 'http']:
        url = f"{protocol}://{subdomain}"
        try:
            response = requests.get(url, timeout=5, allow_redirects=True, verify=False)
            results['status_code'] = response.status_code
            results['server'] = response.headers.get('Server', 'Unknown')
            results['title'] = extract_title(response.text)
            results['protocol'] = protocol
            return results
        except:
            continue
    
    return None

def extract_title(html):
    """
    Extract page title from HTML
    """
    try:
        start = html.lower().find('<title>') + 7
        end = html.lower().find('</title>')
        if start > 6 and end > start:
            return html[start:end].strip()
    except:
        pass
    return "No title found"

def check_ssl_cert(domain):
    """
    Get SSL certificate information
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'version': cert['version']
                }
    except:
        return None

# Example usage
if __name__ == "__main__":
    subdomains = ["www.example.com", "mail.example.com"]  # Your found subdomains
    
    for subdomain in subdomains:
        print(f"\n[*] Checking {subdomain}")
        
        web_info = check_web_service(subdomain)
        if web_info:
            print(f"    [+] Web Service: {web_info['protocol'].upper()}")
            print(f"    [+] Status: {web_info['status_code']}")
            print(f"    [+] Server: {web_info['server']}")
            print(f"    [+] Title: {web_info['title']}")
        
        ssl_info = check_ssl_cert(subdomain)
        if ssl_info:
            print(f"    [+] SSL Subject: {ssl_info['subject']}")
            print(f"    [+] SSL Issuer: {ssl_info['issuer']}")