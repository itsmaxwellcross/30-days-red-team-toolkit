import os
import pwd

class ShellProfilePersistence:
    def __init__(self):
        self.current_user = pwd.getpwuid(os.getuid()).pw_name
        self.home_dir = os.path.expanduser("~")
        self.is_root = os.geteuid() == 0

        self.profile_files = [
            f"{self.home_dir}/.bashrc",
            f"{self.home_dir}/.bash_profile",
            f"{self.home_dir}/.profile",
            f"{self.home_dir}/.zshrc",
            f"{self.home_dir}/.config/fish/config.fish"
        ]