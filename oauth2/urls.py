from django.urls import path
from .views import health_check, version

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("version/", version, name="version"),
]
