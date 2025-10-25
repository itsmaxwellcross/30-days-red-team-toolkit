# Reconnaissance Tools (Days 1-2)

Tools for OSINT, external reconnaissance, and target mapping.

## Tools Overview

### subdomain_enum.py
DNS-based subdomain enumeration using wordlist brute-forcing.

**Usage:**
```bash
python3 subdomain_enum.py target.com wordlists/subdomains.txt
```

**Features:**
- DNS resolution
- Concurrent lookups
- Result filtering
- Output to file

---

### web_service_checker.py
Checks discovered subdomains for active web services.

**Usage:**
```bash
python3 web_service_checker.py target.com
```

**Features:**
- HTTP/HTTPS detection
- Server identification
- Page title extraction
- SSL certificate info
- Response code checking

---

### google_dorker.py
Automated Google dorking for exposed information.

**Usage:**
```bash
python3 google_dorker.py target.com
```

**Features:**
- 12+ dork categories
- Automated searching
- Result parsing
- Report generation
- Rate limiting

**Dork Types:**
- Exposed files (PDFs, docs, spreadsheets)
- Login portals and admin pages
- Directory listings
- Configuration files
- Database files
- Backup files
- Internal documents
- Error messages
- Credentials

---

### email_hunter.py
Email enumeration and validation framework.

**Usage:**
```bash
python3 email_hunter.py target.com "Company Name"
```

**Features:**
- LinkedIn employee discovery
- Email pattern generation
- GitHub code search
- Hunter.io integration
- Breach checking (HIBP)
- Paste site searches

**Output:**
- Generated email permutations
- Valid addresses
- Breach information
- Save to file

---

### tech_fingerprinter.py
Technology stack fingerprinting and analysis.

**Usage:**
```bash
python3 tech_fingerprinter.py https://target.com
```

**Features:**
- HTTP header analysis
- HTML/JavaScript detection
- Cookie analysis
- Common path checking
- SSL certificate extraction
- CMS identification
- Framework detection
- Security header analysis

**Identifies:**
- Web servers
- Frameworks (React, Angular, Vue)
- CMS (WordPress, Drupal, Joomla)
- Backend languages
- CDN providers
- Security posture

---

### master_recon.py
Orchestrates all reconnaissance tools in sequence.

**Usage:**
```bash
python3 master_recon.py target.com "Company Name"
```

**Features:**
- Runs all recon tools
- Generates comprehensive report
- Automated workflow
- Result aggregation

**Process:**
1. Subdomain enumeration
2. Google dorking
3. Email harvesting
4. Technology fingerprinting
5. Report generation

---

## Wordlists

### wordlists/subdomains.txt
Common subdomain names for enumeration.

### wordlists/common_paths.txt
Common web paths and directories.

---

## Output Files

All tools save results to files:
- `{domain}_subdomains.txt` - Discovered subdomains
- `{domain}_dork_results.txt` - Google dork findings
- `{domain}_emails.txt` - Email addresses
- `{domain}_fingerprint.json` - Tech stack data
- `{domain}_recon_report.md` - Master report

---

## Tips for Effective Reconnaissance

1. **Start broad, then narrow**
   - Begin with subdomain enum
   - Fingerprint discovered assets
   - Deep dive on interesting finds

2. **Document everything**
   - Keep detailed notes
   - Screenshot interesting finds
   - Track what you've checked

3. **Stay passive as long as possible**
   - Exhaust OSINT before active scanning
   - Minimize footprint on target systems
   - Use legitimate services

4. **Correlate findings**
   - Connect pieces of information
   - Look for patterns
   - Identify weak points

5. **Respect rate limits**
   - Don't hammer APIs
   - Use delays between requests
   - Avoid detection

---

## Legal Notice

These tools are for authorized security testing only. Always obtain written permission before testing systems you don't own.

---

## Next Steps

After reconnaissance:
1. Review all collected data
2. Identify attack vectors
3. Proceed to weaponization (Day 3)
4. Plan delivery strategy (Day 4)