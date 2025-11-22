import os
from ..core import SSHPersistence
from ..utils.helpers import run_command

class SSHDConfigModifier(SSHPersistence):
    def modify(self, setting: str, value: str):
        if not self.is_root:
            print("[!] Root required to modify sshd_config")
            return None

        config_file = "/etc/ssh/sshd_config"
        backup_file = f"{config_file}.bak"

        if not os.path.exists(backup_file):
            run_command(f"cp {config_file} {backup_file}")

        try:
            with open(config_file, 'r') as f:
                lines = f.readlines()

            new_lines = []
            found = False
            for line in lines:
                if line.strip().startswith(setting):
                    new_lines.append(f"{setting} {value}\n")
                    found = True
                else:
                    new_lines.append(line)

            if not found:
                new_lines.append(f"\n{setting} {value}\n")

            with open(config_file, 'w') as f:
                f.writelines(new_lines)

            print(f"[+] Modified: {setting} = {value}")
            print(f"[!] Restart SSH: systemctl restart sshd")
            return {
                'setting': setting,
                'value': value,
                'restore_cmd': f"cp {backup_file} {config_file} && systemctl restart sshd"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None