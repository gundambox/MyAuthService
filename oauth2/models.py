from django.core.exceptions import ValidationError
from django.db import models
from .validators import validate_redirect_uris
from .utils import generate_unique_client_id, generate_client_secret


class Client(models.Model):

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "OAuth2 Client"
        verbose_name_plural = "OAuth2 Clients"

    CLIENT_TYPE_CHOICES = [
        ("confidential", "Confidential"),
        ("public", "Public"),
    ]

    client_id = models.CharField(max_length=64, unique=True, db_index=True)
    client_secret = models.CharField(max_length=128, blank=True, null=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    redirect_uris = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.client_id[:8]}...)"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            if not self.client_id:
                self.client_id = generate_unique_client_id(Client)

            if self.client_type == "confidential" and not self.client_secret:
                self.client_secret = generate_client_secret()

            if self.client_type == "public":
                self.client_secret = None

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        errors = {}

        if not self.redirect_uris or len(self.redirect_uris) == 0:
            errors["redirect_uris"] = "At least one redirect URI is required."
        else:
            try:
                validate_redirect_uris(self.redirect_uris)
            except ValidationError as e:
                errors["redirect_uris"] = e.message

        if self.client_type == "public":
            self.client_secret = None
        elif self.client_type == "confidential" and self.pk is not None:
            if not self.client_secret:
                errors["client_secret"] = (
                    "Confidential clients must have a client_secret."
                )

        if errors:
            raise ValidationError(errors)

    def is_valid_redirect_uri(self, uri):
        return uri in self.redirect_uris

    def get_redirect_uri(self, uri=None):
        if uri is not None:
            if self.is_valid_redirect_uri(uri):
                return uri
            return None

        if len(self.redirect_uris) == 1:
            return self.redirect_uris[0]

        return None
