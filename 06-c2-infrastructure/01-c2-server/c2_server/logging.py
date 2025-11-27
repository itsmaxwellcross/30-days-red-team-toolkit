import logging
import os
from datetime import datetime

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    log_file = f"logs/c2_server_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('C2Server')