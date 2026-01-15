import os
import sys
from service.management.commands import ManageCrons

APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'local')

class Entrypoint:
    def __init__(self):
        self.setup_environment()
        self.start_cronjobs()
        self.runserver()

    def setup_environment(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_server.settings')
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        os.environ["PYTHONUNBUFFERED"] = "1"

    def runserver(self):
        print(f"APP PID: {os.getpid()}")
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
        cmd = [
            sys.executable, "-m", "gunicorn",
            "django_server.asgi:application",
            "--workers", "4",
            "--worker-class", "uvicorn.workers.UvicornWorker",
            "--bind", f"0.0.0.0:{port}"
        ]
        os.execvp(cmd[0], cmd)

    def start_cronjobs(self):
        ManageCrons()


if __name__ == '__main__':
    Entrypoint()
