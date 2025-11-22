import os
from ..core import ShellProfilePersistence

class ProfileScanner(ShellProfilePersistence):
    def check_suspicious(self):
        patterns = [
            'bash -i', '/dev/tcp/', 'nc ', 'netcat', 'curl', 'wget', 'python', 'perl',
            '/tmp/', 'base64', 'eval', 'sh -c', '&>', '& disown'
        ]

        print("[*] Scanning shell profile files for suspicious content...\n")

        for path in self.profile_files + ["/etc/profile.d/", "/etc/update-motd.d/"]:
            if "profile.d" in path or "motd.d" in path:
                if os.path.exists(path):
                    for f in os.listdir(path):
                        fp = os.path.join(path, f)
                        if os.path.isfile(fp):
                            self._scan_file(fp, patterns)
            elif os.path.exists(path):
                self._scan_file(path, patterns)

    def _scan_file(self, path: str, patterns: list):
        try:
            with open(path, 'r') as f:
                content = f.read()
            found = [p for p in patterns if p in content.lower()]
            if found:
                print(f"[!] SUSPICIOUS → {path}")
                for p in found[:3]:
                    print(f"    → contains: {p}")
                print()
        except:
            pass