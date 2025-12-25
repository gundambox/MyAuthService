from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def version(request):
    return Response({"service": "MyAuthService", "version": settings.SERVICE_VERSION})
