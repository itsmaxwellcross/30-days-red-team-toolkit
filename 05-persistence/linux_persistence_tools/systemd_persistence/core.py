import os

class SystemdPersistence:
    def __init__(self):
        self.is_root = os.geteuid() == 0
        self.user = os.getenv('USER', os.getenv('USERNAME', 'user'))