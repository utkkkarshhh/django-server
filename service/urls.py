from django.urls import path

from service.views import *

urlpatterns = [
    path('Healthcheck', HealthCheckView.as_view(), name='Healthcheck'),
]
