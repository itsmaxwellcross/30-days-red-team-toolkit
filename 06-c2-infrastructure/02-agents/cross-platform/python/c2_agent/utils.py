import random
import time
from datetime import datetime

def jitter_sleep(base: int, jitter: int):
    variation = random.randint(-jitter, jitter)
    sleep_time = max(1, base + variation)
    time.sleep(sleep_time)

def log(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")