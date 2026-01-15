from django.db import connections
from django.db.utils import OperationalError
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.utils import CustomResponseHandler


class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Health check endpoint to verify if the service is up and running.
        """
        return CustomResponseHandler(
            message=ResponseMessages.SERVICE_UP,
            data={
                "is_db_healthy": self.is_database_healthy()
            }
        )

    def is_database_healthy(self, alias: str = "default") -> bool:
        """
        Performs a lightweight database health check.

        Returns:
            True  -> DB is reachable and responding
            False -> DB is down or unreachable
        """
        try:
            with connections[alias].cursor() as cursor:
                cursor.execute("SELECT 1;")
            return True
        except OperationalError:
            return False
