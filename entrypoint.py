import os
import sys
import signal
import subprocess
from dotenv import load_dotenv

load_dotenv()

from service.management.commands import ManageCrons
from service.utils import logger

APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'local')
ENABLE_CRONS = os.getenv('ENABLE_CRONS', 'False').lower() in ('true', '1', 't')

class Entrypoint:
    def __init__(self):
        self.cron_manager = None
        self.setup_environment()
        self.start_cronjobs()
        self.runserver()

    def setup_environment(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_server.settings')
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        os.environ["PYTHONUNBUFFERED"] = "1"

    def runserver(self):
        logger.info(f"`runserver()` : App Process ID: {os.getpid()}")
        from django.core.management import execute_from_command_line

        command_args = sys.argv[1:]
        port = "8000"
        if len(command_args) > 0 and command_args[0].isdigit():
            port = command_args[0]
            command_args = command_args[1:]

        try:
            if APP_ENVIRONMENT != 'local':
                self.run_gunicorn_asgi(port)
            else:
                execute_from_command_line(['manage.py', 'runserver', port] + command_args)
        except ImportError as exc:
            raise ImportError(
                'Failure while importing "Django", please check the system dependencies.'
            ) from exc

    def run_gunicorn_asgi(self, port: str):
        workers = "4"
        if os.environ.get('DJANGO_DEBUG', '') != 'False':
            workers = "1"

        cmd = [
            sys.executable, "-m", "gunicorn",
            "django_server.asgi:application",
            "--workers", workers,
            "--worker-class", "uvicorn.workers.UvicornWorker",
            "--bind", f"0.0.0.0:{port}"
        ]
        
        process = subprocess.Popen(cmd)

        def shutdown(signum, frame):
            logger.info(f"Received signal {signum}. Shutting down...")
            if self.cron_manager:
                self.cron_manager.shutdown()
            process.terminate()
            process.wait()
            sys.exit(0)

        signal.signal(signal.SIGTERM, shutdown)
        signal.signal(signal.SIGINT, shutdown)

        process.wait()

    def start_cronjobs(self):
        if ENABLE_CRONS:
            self.cron_manager = ManageCrons()
        else:
            logger.info("Crons Disabled")


if __name__ == '__main__':
    Entrypoint()
