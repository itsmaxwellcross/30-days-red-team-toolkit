import os
import pwd

class SSHPersistence:
    def __init__(self):
        self.current_user = pwd.getpwuid(os.getuid()).pw_name
        self.home_dir = os.path.expanduser("~")
        self.ssh_dir = f"{self.home_dir}/.ssh"
        self.is_root = os.geteuid() == 0