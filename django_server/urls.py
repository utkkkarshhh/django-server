from django.contrib import admin
from django.urls import path, include

from service.views.healthcheck import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('service.urls_v1'))
]
