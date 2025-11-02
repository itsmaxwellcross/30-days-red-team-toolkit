"""Configuration and constants for shell stabilizer"""

# Shell Types
SHELL_TYPES = ['linux', 'windows']
DEFAULT_SHELL_TYPE = 'linux'

# Detection Commands
DETECTION_COMMANDS = {
    'linux': 'uname -a',
    'windows': 'ver',
    'python': 'import sys; print(sys.platform)'
}

# Attacker IP placeholder
ATTACKER_IP_PLACEHOLDER = 'ATTACKER_IP'
ATTACKER_PORT_PLACEHOLDER = '4444'

# Output Settings
DEFAULT_GUIDE_FILENAME = 'shell_stabilization.txt'
GUIDE_WIDTH = 60