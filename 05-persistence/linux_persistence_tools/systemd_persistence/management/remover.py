from ..core import SystemdPersistence
from ..utils.helpers import run_command
import os

class ServiceRemover(SystemdPersistence):
    def remove(self, service_name: str, is_user_service: bool = False):
        if is_user_service:
            run_command(f"systemctl --user stop {service_name}")
            run_command(f"systemctl --user disable {service_name}")
            path = os.path.expanduser(f"~/.config/systemd/user/{service_name}.service")
            run_command("systemctl --user daemon-reload")
        else:
            if not self.is_root:
                print("[!] Root required to remove system service")
                return False
            run_command(f"systemctl stop {service_name}")
            run_command(f"systemctl disable {service_name}")
            path = f"/etc/systemd/system/{service_name}.service"
            run_command("systemctl daemon-reload")

        if os.path.exists(path):
            os.remove(path)
        print(f"[+] Service removed: {service_name}")
        return True