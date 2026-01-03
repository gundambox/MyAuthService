from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "client_id", "client_type", "is_active", "created_at"]
    list_filter = ["client_type", "is_active", "created_at"]
    search_fields = ["name", "client_id", "description"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (
            "Basic Information",
            {"fields": ["name", "description", "client_type", "is_active"]},
        ),
        (
            "Credentials",
            {
                "fields": ["client_id", "client_secret"],
                "description": "Client credentials for authentication",
            },
        ),
        (
            "Redirect URIs",
            {
                "fields": ["redirect_uris"],
                "description": (
                    "Whitelisted redirect URIs for OAuth 2.0 authorization flow.<br>"
                    "<strong>Format requirements:</strong><br>"
                    "- Must be absolute URIs (include scheme and host)<br>"
                    "- HTTPS required (except http://localhost for development)<br>"
                    "- No fragment components (#) allowed<br>"
                    "- Private-use URI schemes allowed (e.g., com.example.app:/callback)<br>"
                    "<strong>Examples:</strong><br>"
                    "- https://example.com/callback<br>"
                    "- http://localhost:8080/callback<br>"
                    "- com.example.app:/oauth/callback"
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]
