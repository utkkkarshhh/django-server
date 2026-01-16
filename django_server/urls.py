from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from service.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootView.as_view(), name='Root'),
    path('api/v1/', include('service.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
