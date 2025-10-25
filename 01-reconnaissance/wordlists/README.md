# Wordlists for Reconnaissance

## subdomains.txt

Common subdomain names for DNS enumeration. Includes:
- Standard subdomains (www, mail, ftp)
- Application subdomains (app, api, portal)
- Infrastructure (vpn, remote, proxy)
- Development (dev, test, staging)
- Regional variants
- Service-specific names

**Usage:**
```bash
python3 subdomain_enum.py target.com wordlists/subdomains.txt
```

**Size:** ~100 common subdomain names

---

## common_paths.txt

Common web paths and directories for discovery.

**Categories:**
- Admin panels (/admin, /administrator, /wp-admin)
- Authentication (/login, /signin, /auth)
- APIs (/api, /v1, /graphql)
- Backups (/backup, /old, /.git)
- Configuration (/.env, /config, /settings)
- Database tools (/phpmyadmin, /adminer)

**Usage:**
```bash
python3 tech_fingerprinter.py https://target.com
# Uses paths automatically for discovery
```

---

## Expanding Wordlists

### Adding Custom Entries
```bash
# Add industry-specific subdomains
echo "customer-portal" >> subdomains.txt
echo "partner-login" >> subdomains.txt

# Add application-specific paths
echo "/app-admin" >> common_paths.txt
echo "/api/v2" >> common_paths.txt
```

### External Wordlists

**Subdomain Lists:**
- SecLists: `/Discovery/DNS/`
- all.txt (large, comprehensive)
- bitquark-subdomains-top100000.txt

**Path Lists:**
- SecLists: `/Discovery/Web-Content/`
- common.txt
- directory-list-2.3-medium.txt

**Download SecLists:**
```bash
git clone https://github.com/danielmiessler/SecLists.git
```

---

## Best Practices

1. **Start small, expand as needed**
   - Begin with curated lists
   - Add discoveries to your lists
   - Build target-specific wordlists

2. **Quality over quantity**
   - Focused lists are faster
   - Less noise in results
   - Better for stealthy recon

3. **Customize for targets**
   - Add company-specific terms
   - Include industry jargon
   - Use discovered patterns

---

## Maintenance

Update wordlists regularly:
```bash
# Backup current lists
cp subdomains.txt subdomains.txt.bak

# Merge with new discoveries
cat new_subdomains.txt >> subdomains.txt

# Remove duplicates
sort -u subdomains.txt -o subdomains.txt
```