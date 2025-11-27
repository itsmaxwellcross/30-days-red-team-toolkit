import subprocess
import platform

def execute_command(command: str, timeout: int = 300):
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['cmd.exe', '/c', command],
                capture_output=True,
                text=True,
                timeout=timeout
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                executable='/bin/bash',
                timeout=timeout
            )

        output = result.stdout.strip()
        if result.stderr.strip():
            output += f"\n[STDERR]\n{result.stderr.strip()}"

        return output or "[No output]"
    except subprocess.TimeoutExpired:
        return "[ERROR] Command timed out"
    except Exception as e:
        return f"[ERROR] {str(e)}"