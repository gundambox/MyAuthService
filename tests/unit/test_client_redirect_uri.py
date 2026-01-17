import pytest
from django.core.exceptions import ValidationError
from oauth2.models import Client


@pytest.mark.django_db
class TestClientRedirectUriValidation:
    def test_clean_validates_redirect_uris(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.clean()

    def test_clean_rejects_invalid_redirect_uri(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["http://example.com/callback"],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_clean_rejects_empty_redirect_uris(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_clean_rejects_duplicate_redirect_uris(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[
                "https://example.com/callback",
                "https://example.com/callback",
            ],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_clean_rejects_uri_with_fragment(self):
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback#fragment"],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict


@pytest.mark.django_db
class TestClientIsValidRedirectUri:
    def test_exact_match_returns_true(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://example.com/callback") is True

    def test_no_match_returns_false(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://example.com/different") is False

    def test_partial_match_returns_false(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert (
            client.is_valid_redirect_uri("https://example.com/callback/extra") is False
        )

    def test_case_sensitive_match(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://example.com/Callback") is False

    def test_multiple_uris_exact_match(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[
                "https://example.com/callback1",
                "https://example.com/callback2",
                "http://localhost/callback",
            ],
        )
        assert client.is_valid_redirect_uri("https://example.com/callback1") is True
        assert client.is_valid_redirect_uri("https://example.com/callback2") is True
        assert client.is_valid_redirect_uri("http://localhost/callback") is True
        assert client.is_valid_redirect_uri("https://example.com/callback3") is False


@pytest.mark.django_db
class TestClientGetRedirectUri:
    def test_with_valid_uri_returns_uri(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert (
            client.get_redirect_uri("https://example.com/callback")
            == "https://example.com/callback"
        )

    def test_with_invalid_uri_returns_none(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.get_redirect_uri("https://example.com/different") is None

    def test_without_uri_single_registered_returns_uri(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.get_redirect_uri() == "https://example.com/callback"

    def test_without_uri_multiple_registered_returns_none(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[
                "https://example.com/callback1",
                "https://example.com/callback2",
            ],
        )
        assert client.get_redirect_uri() is None

    def test_with_none_uri_single_registered_returns_uri(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.get_redirect_uri(None) == "https://example.com/callback"

    def test_with_none_uri_multiple_registered_returns_none(self):
        client = Client.objects.create(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[
                "https://example.com/callback1",
                "https://example.com/callback2",
            ],
        )
        assert client.get_redirect_uri(None) is None
