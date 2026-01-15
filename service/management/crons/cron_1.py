import os
from datetime import datetime
from service.utils import logger


class Cron1:
    
    @classmethod
    def initialize(cls):
        logger.info(f"[Cronjob1] Running task in PID {os.getpid()} : Time: {datetime.now()}")