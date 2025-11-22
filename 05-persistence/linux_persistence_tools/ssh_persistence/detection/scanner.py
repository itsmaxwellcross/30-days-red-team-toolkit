import os
from ..core import SSHPersistence
from ..utils.helpers import run_command

class SSHKeyScanner(SSHPersistence):
    def list_all(self):
        print(f"[CURRENT USER: {self.current_user}]")
        auth_file = f"{self.ssh_dir}/authorized_keys"
        if os.path.exists(auth_file):
            with open(auth_file, 'r') as f:
                print(f.read() or "(empty)")
        else:
            print("(no authorized_keys)")

        if self.is_root:
            print("\n[ALL USERS ON SYSTEM]")
            result = run_command("find /home /root -name authorized_keys 2>/dev/null")
            if result['success']:
                for path in result['stdout'].split('\n'):
                    if path:
                        print(f"\n{path}:")
                        try:
                            with open(path, 'r') as f:
                                print(f.read().strip() or "(empty)")
                        except:
                            print("(permission denied)")