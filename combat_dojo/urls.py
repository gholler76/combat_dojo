from django.conf import settings
from django.contrib import admin
from django.urls import include, path

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('combat_app.routes')),
    path('__debug__/', include(debug_toolbar.urls)),
]
