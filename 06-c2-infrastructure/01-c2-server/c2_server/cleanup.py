import threading
import time
from .database import cleanup_old_sessions

def start_cleanup_thread(db_path: str, max_age_days: int, logger):
    def worker():
        while True:
            try:
                deactivated = cleanup_old_sessions(db_path, max_age_days)
                if deactivated > 0:
                    logger.info(f"Deactivated {deactivated} old sessions")
                time.sleep(3600)  # Hourly
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()