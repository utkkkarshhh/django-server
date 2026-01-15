import os
from datetime import datetime
from service.utils import logger


class Cron2:
    
    @classmethod
    def initialize(cls):
        logger.info(f"[Cronjob2] Running task in PID {os.getpid()} : Time: {datetime.now()}")