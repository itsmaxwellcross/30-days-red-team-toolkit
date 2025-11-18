from pathlib import Path


class ShellAccessChallenge:
    """Creates shell access challenge files"""
    
    def __init__(self, output_dir, flags):
        self.output_dir = Path(output_dir)
        self.flags = flags
    
    def create(self):
        """Create shell access challenge components"""
        self._create_system_files()
        self._create_user_files()
        print("[+] Created shell access challenge")
    
    def _create_system_files(self):
        """Create simulated system files"""
        # /etc/passwd
        passwd = f"""root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
admin:x:1000:1000:Admin User:/home/admin:/bin/bash
backup:x:1001:1001:Backup User:/home/backup:/bin/bash
# Flag 3 hint: Check admin's bash history
"""
        
        etc_dir = self.output_dir / 'etc'
        with open(etc_dir / 'passwd', 'w') as f:
            f.write(passwd)
        
        # /etc/hosts
        hosts = """127.0.0.1    localhost
127.0.1.1    targetcorp
192.168.1.100    targetcorp.local
192.168.1.10    db.targetcorp.local
"""
        
        with open(etc_dir / 'hosts', 'w') as f:
            f.write(hosts)
    
    def _create_user_files(self):
        """Create user home directory files"""
        admin_home = self.output_dir / 'home' / 'admin'
        
        # .bash_history with flag
        bash_history = f"""ls -la
cd /var/www/html
cat config.php
echo '{self.flags['flag3_shell']}' > /tmp/flag3.txt
mysql -u root -p'P@ssw0rd123'
sudo -l
find / -perm -4000 2>/dev/null
cat /etc/crontab
"""
        
        with open(admin_home / '.bash_history', 'w') as f:
            f.write(bash_history)
        
        # .bashrc
        bashrc = """# .bashrc
export PATH=/usr/local/bin:/usr/bin:/bin
alias ls='ls --color=auto'
alias ll='ls -la'
"""
        
        with open(admin_home / '.bashrc', 'w') as f:
            f.write(bashrc)
        
        # SSH config
        ssh_dir = admin_home / '.ssh'
        ssh_config = """Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
"""
        
        with open(ssh_dir / 'config', 'w') as f:
            f.write(ssh_config)