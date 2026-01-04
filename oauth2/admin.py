from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "client_id_display",
        "client_type",
        "is_active",
        "created_at",
    ]
    list_filter = ["client_type", "is_active", "created_at"]
    search_fields = ["name", "client_id", "description"]
    readonly_fields = ["client_id", "client_secret_display", "created_at", "updated_at"]
    actions = ["deactivate_clients", "activate_clients"]

    fieldsets = [
        (
            "Client Information",
            {"fields": ["name", "description", "client_type", "is_active"]},
        ),
        (
            "Credentials",
            {
                "fields": ["client_id", "client_secret_display"],
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

    def client_id_display(self, obj):
        if obj.client_id:
            return f"{obj.client_id[:16]}..."
        return "-"

    client_id_display.short_description = "Client ID"

    def client_secret_display(self, obj):
        if obj.client_type == "public":
            return mark_safe(
                '<span style="color: #999;">Not applicable (public client)</span>'
            )

        if not obj.pk:
            return mark_safe(
                '<span style="color: #999;">Will be generated on save</span>'
            )

        # Check if this is a newly created client (secret in session)
        if hasattr(self, "_display_secret") and self._display_secret:
            return format_html(
                """
<div style="padding: 15px; background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 4px; margin: 10px 0;">
    <strong style="color: #856404; font-size: 16px;">⚠️ IMPORTANT: Save this client secret now!</strong><br><br>
    <div style="background-color: #fff; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 3px;">
        <code style="font-size: 14px; color: #000; word-break: break-all; user-select: all;">{}</code>
    </div>
    <strong style="color: #856404;">This is the only time you will see this secret. Copy it immediately.</strong><br>
    <small>The secret will be masked when you navigate away from this page.</small>
</div>""",
                self._display_secret,
            )

        return mark_safe(
            '<span style="font-family: monospace;">••••••••••••••••</span>'
        )

    client_secret_display.short_description = "Client Secret"

    def save_model(self, request, obj, form, change):
        if not change and obj.client_type == "confidential":
            is_new_confidential = True
        else:
            is_new_confidential = False

        super().save_model(request, obj, form, change)

        if is_new_confidential and obj.client_secret:
            # Store secret in session for one-time display
            request.session[f"new_client_secret_{obj.pk}"] = obj.client_secret
            request.session.modified = True

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        # Check if we have a newly created secret to display
        if object_id:
            session_key = f"new_client_secret_{object_id}"
            if session_key in request.session:
                self._display_secret = request.session.pop(session_key)
                request.session.modified = True
            else:
                self._display_secret = None
        else:
            self._display_secret = None

        return super().changeform_view(request, object_id, form_url, extra_context)

    def deactivate_clients(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} client(s) successfully deactivated.")

    deactivate_clients.short_description = "Deactivate selected clients"

    def activate_clients(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} client(s) successfully activated.")

    activate_clients.short_description = "Activate selected clients"

    def response_add(self, request, obj, post_url_continue=None):
        # For confidential clients, redirect directly to the detail page
        if obj.client_type == "confidential":
            msg = f'The OAuth2 Client "{obj}" was added successfully. Please save the client secret below.'
            self.message_user(request, msg, messages.SUCCESS)

            return HttpResponseRedirect(
                reverse("admin:oauth2_client_change", args=[obj.pk])
            )

        # Public clients still go to the list page
        return super().response_add(request, obj, post_url_continue)
