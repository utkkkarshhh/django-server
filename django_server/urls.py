from django.contrib import admin
from django.urls import path, include

from service.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootView.as_view(), name='Root'),
    path('api/v1/', include('service.urls'))
]
