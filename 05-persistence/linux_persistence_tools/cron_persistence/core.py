import os
from .utils.helpers import get_current_user

class CronPersistence:
    def __init__(self):
        self.current_user = get_current_user()
        self.is_root = os.geteuid() == 0