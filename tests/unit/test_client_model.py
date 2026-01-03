import pytest
from django.core.exceptions import ValidationError
from oauth2.models import Client


@pytest.mark.django_db
class TestClientModel:
    def test_create_confidential_client(self):
        client = Client.objects.create(
            client_id="test_client_123456789",
            client_secret="secret_key",
            client_type="confidential",
            name="Test Confidential Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_id == "test_client_123456789"
        assert client.client_secret == "secret_key"
        assert client.client_type == "confidential"
        assert client.name == "Test Confidential Client"
        assert client.redirect_uris == ["https://example.com/callback"]
        assert client.is_active is True
        assert client.created_at is not None
        assert client.updated_at is not None

    def test_create_public_client(self):
        client = Client.objects.create(
            client_id="public_client_123",
            client_type="public",
            name="Test Public Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is None
        assert client.client_type == "public"

    def test_client_id_unique_constraint(self):
        Client.objects.create(
            client_id="duplicate_id",
            client_type="public",
            name="First Client",
            redirect_uris=["https://example.com/callback"],
        )
        with pytest.raises(Exception):
            Client.objects.create(
                client_id="duplicate_id",
                client_type="public",
                name="Second Client",
                redirect_uris=["https://example.com/callback"],
            )

    def test_str_method(self):
        client = Client.objects.create(
            client_id="test_client_123456789",
            client_type="public",
            name="My App",
            redirect_uris=["https://example.com/callback"],
        )
        assert str(client) == "My App (test_cli...)"

    def test_clean_empty_redirect_uris(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.is_valid()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_clean_public_client_with_secret(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            client_secret="should_not_have_secret",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.is_valid()
        assert "client_secret" in exc_info.value.error_dict

    def test_confidential_client_with_secret(self):
        client = Client(
            client_id="test_client",
            client_type="confidential",
            client_secret="valid_secret",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.is_valid()

    def test_multiple_redirect_uris(self):
        client = Client.objects.create(
            client_id="multi_uri_client",
            client_type="public",
            name="Multi URI Client",
            redirect_uris=[
                "https://example.com/callback1",
                "https://example.com/callback2",
                "https://example.com/callback3",
            ],
        )
        assert len(client.redirect_uris) == 3

    def test_is_active_default(self):
        client = Client.objects.create(
            client_id="active_client",
            client_type="public",
            name="Active Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_active is True

    def test_ordering(self):
        _ = Client.objects.create(
            client_id="client1",
            client_type="public",
            name="Client 1",
            redirect_uris=["https://example.com/callback"],
        )
        _ = Client.objects.create(
            client_id="client2",
            client_type="public",
            name="Client 2",
            redirect_uris=["https://example.com/callback"],
        )
        clients = list(Client.objects.all())
        assert clients[0].client_id == "client2"
        assert clients[1].client_id == "client1"
