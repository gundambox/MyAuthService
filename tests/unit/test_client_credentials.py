import pytest
from django.core.exceptions import ValidationError
from oauth2.models import Client


@pytest.mark.django_db
class TestClientCredentialGeneration:
    def test_auto_generates_client_id_for_new_client(self):
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_id is not None
        assert len(client.client_id) >= 32
        assert isinstance(client.client_id, str)

    def test_auto_generates_client_secret_for_confidential_client(self):
        client = Client.objects.create(
            client_type="confidential",
            name="Test Confidential Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is not None
        assert len(client.client_secret) >= 48
        assert isinstance(client.client_secret, str)

    def test_public_client_has_no_secret(self):
        client = Client.objects.create(
            client_type="public",
            name="Test Public Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is None

    def test_public_client_secret_forced_to_none(self):
        client = Client.objects.create(
            client_type="public",
            client_secret="should_be_removed",
            name="Test Public Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is None

    def test_preserves_provided_client_id(self):
        custom_id = "custom_client_id_12345"
        client = Client.objects.create(
            client_id=custom_id,
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_id == custom_id

    def test_preserves_provided_client_secret(self):
        custom_secret = "custom_secret_12345"
        client = Client.objects.create(
            client_type="confidential",
            client_secret=custom_secret,
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret == custom_secret

    def test_credentials_not_regenerated_on_update(self):
        client = Client.objects.create(
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        original_id = client.client_id
        original_secret = client.client_secret

        client.name = "Updated Client"
        client.save()

        assert client.client_id == original_id
        assert client.client_secret == original_secret

    def test_client_id_uniqueness(self):
        client1 = Client.objects.create(
            client_type="public",
            name="Client 1",
            redirect_uris=["https://example.com/callback"],
        )
        client2 = Client.objects.create(
            client_type="public",
            name="Client 2",
            redirect_uris=["https://example.com/callback"],
        )
        assert client1.client_id != client2.client_id

    def test_generated_credentials_are_url_safe(self):
        client = Client.objects.create(
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert all(c.isalnum() or c in "-_" for c in client.client_id)
        assert all(c.isalnum() or c in "-_" for c in client.client_secret)

    def test_clean_validates_confidential_client_must_have_secret(self):
        client = Client(
            client_id="test_client_id",
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.save()

        client.client_secret = None
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "client_secret" in exc_info.value.error_dict

    def test_clean_allows_confidential_client_with_secret(self):
        client = Client(
            client_id="test_client_id",
            client_secret="test_secret",
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.save()
        client.clean()

    def test_clean_sets_public_client_secret_to_none(self):
        client = Client(
            client_id="test_client_id",
            client_secret="should_be_removed",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.clean()
        assert client.client_secret is None

    def test_multiple_clients_get_unique_ids(self):
        clients = [
            Client.objects.create(
                client_type="public",
                name=f"Client {i}",
                redirect_uris=["https://example.com/callback"],
            )
            for i in range(10)
        ]
        client_ids = [c.client_id for c in clients]
        assert len(set(client_ids)) == 10

    def test_confidential_client_creation_without_explicit_secret(self):
        client = Client.objects.create(
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is not None
        assert len(client.client_secret) >= 48
