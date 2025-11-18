from pathlib import Path

class EnumerationChallenge:
    """Creates enumeration challenge files"""
    
    def __init__(self, output_dir, flags):
        self.output_dir = Path(output_dir)
        self.flags = flags
    
    def create(self):
        """Create enumeration challenge components"""
        self._create_config_files()
        self._create_cron_files()
        self._create_database_info()
        print("[+] Created enumeration challenge")
    
    def _create_config_files(self):
        """Create configuration files with credentials"""
        # Database config
        config = f"""[database]
host = localhost
port = 3306
username = dbadmin
password = {self.flags['flag4_creds']}
database = targetcorp_production

[api]
api_key = sk_live_51234567890abcdef
api_secret = super_secret_api_key_2024
endpoint = https://api.targetcorp.com

[smtp]
host = smtp.targetcorp.com
port = 587
username = noreply@targetcorp.com
password = EmailP@ss2024

# Flag 4: The database password above is your flag!
# Format: FLAG{{CREDENTIALS_...}}
"""
        
        config_dir = self.output_dir / 'var' / 'www' / 'html'
        with open(config_dir / 'config.ini', 'w') as f:
            f.write(config)
        
        # .env file
        env = f"""APP_NAME=TargetCorp
APP_ENV=production
APP_DEBUG=false
APP_URL=https://targetcorp.com

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=targetcorp
DB_USERNAME=dbadmin
DB_PASSWORD={self.flags['flag4_creds']}

# AWS Credentials
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
"""
        
        with open(config_dir / '.env', 'w') as f:
            f.write(env)
    
    def _create_cron_files(self):
        """Create cron job files"""
        cron = """# /etc/crontab: system-wide crontab
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*/5 *   * * *   root    /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
0 2     * * *   root    /usr/local/bin/cleanup.sh
# Flag 5 hint: Check the backup script - it has a vulnerability!
"""
        
        with open(self.output_dir / 'etc' / 'crontab', 'w') as f:
            f.write(cron)
    
    def _create_database_info(self):
        """Create simulated database information"""
        db_info = """# Database Information

## Connection Details
- Host: localhost
- Database: targetcorp_production
- User: dbadmin
- Password: Found in config.ini (Flag 4)

## Tables
- users
- products
- orders
- sessions
- admin_logs

## Sample Query
```sql
SELECT * FROM users WHERE role='admin';
```

## Dump Command
```bash
mysqldump -u dbadmin -p targetcorp_production > db_backup.sql
```
"""
        
        with open(self.output_dir / 'DATABASE_INFO.md', 'w') as f:
            f.write(db_info)