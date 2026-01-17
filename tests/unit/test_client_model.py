import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_confidential_client_with_secret(self):
        client = Client(
            client_id="test_client",
            client_type="confidential",
            client_secret="valid_secret",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.clean()

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


@pytest.mark.django_db
class TestClientModelFields:
    """Tests for Client model field definitions and constraints.

    Covers TODO items:
    - All required fields are present
    - Field types and constraints are correct
    - Default values work as expected
    """

    def test_all_required_fields_are_present(self):
        """Verify all expected fields exist on the Client model."""
        client = Client()
        expected_fields = [
            "id",
            "client_id",
            "client_secret",
            "client_type",
            "name",
            "description",
            "redirect_uris",
            "is_active",
            "created_at",
            "updated_at",
        ]
        for field_name in expected_fields:
            assert hasattr(client, field_name), f"Missing field: {field_name}"

    def test_client_id_field_type_and_constraints(self):
        """Verify client_id field has correct type and constraints."""
        field = Client._meta.get_field("client_id")
        assert field.max_length == 64
        assert field.unique is True
        assert field.db_index is True

    def test_client_secret_field_type_and_constraints(self):
        """Verify client_secret field allows null and blank."""
        field = Client._meta.get_field("client_secret")
        assert field.max_length == 128
        assert field.null is True
        assert field.blank is True

    def test_client_type_field_type_and_constraints(self):
        """Verify client_type field has correct choices."""
        field = Client._meta.get_field("client_type")
        assert field.max_length == 20
        expected_choices = [("confidential", "Confidential"), ("public", "Public")]
        assert list(field.choices) == expected_choices

    def test_name_field_type_and_constraints(self):
        """Verify name field has correct max_length."""
        field = Client._meta.get_field("name")
        assert field.max_length == 255

    def test_description_field_type_and_constraints(self):
        """Verify description field can be blank."""
        field = Client._meta.get_field("description")
        assert field.blank is True

    def test_redirect_uris_field_default_value(self):
        """Verify redirect_uris field defaults to empty list."""
        field = Client._meta.get_field("redirect_uris")
        assert field.default == list

    def test_is_active_field_default_value(self):
        """Verify is_active field defaults to True."""
        field = Client._meta.get_field("is_active")
        assert field.default is True

    def test_created_at_field_auto_now_add(self):
        """Verify created_at field uses auto_now_add."""
        field = Client._meta.get_field("created_at")
        assert field.auto_now_add is True

    def test_updated_at_field_auto_now(self):
        """Verify updated_at field uses auto_now."""
        field = Client._meta.get_field("updated_at")
        assert field.auto_now is True

    def test_default_values_work_on_creation(self):
        """Verify default values are applied correctly on creation."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_active is True
        assert client.description == ""
        assert client.created_at is not None
        assert client.updated_at is not None


@pytest.mark.django_db
class TestCredentialGeneration:
    """Tests for automatic credential generation.

    Covers TODO items:
    - client_id is auto-generated on creation
    - client_id is unique
    - client_secret is generated for confidential clients only
    - Public clients have null client_secret
    - Credentials not overwritten on update
    """

    def test_client_id_auto_generated_on_creation(self):
        """Verify client_id is auto-generated when not provided."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_id is not None
        assert len(client.client_id) >= 32
        assert isinstance(client.client_id, str)

    def test_client_id_is_unique(self):
        """Verify client_id must be unique (database constraint)."""
        Client.objects.create(
            client_id="duplicate_id",
            client_type="public",
            name="First Client",
            redirect_uris=["https://example.com/callback"],
        )
        with pytest.raises(IntegrityError):
            Client.objects.create(
                client_id="duplicate_id",
                client_type="public",
                name="Second Client",
                redirect_uris=["https://example.com/callback"],
            )

    def test_multiple_clients_get_unique_auto_generated_ids(self):
        """Verify multiple clients get unique auto-generated IDs."""
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

    def test_client_secret_generated_for_confidential_clients_only(self):
        """Verify client_secret is auto-generated for confidential clients."""
        client = Client.objects.create(
            client_type="confidential",
            name="Test Confidential Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is not None
        assert len(client.client_secret) >= 48
        assert isinstance(client.client_secret, str)

    def test_public_clients_have_null_client_secret(self):
        """Verify public clients have null client_secret."""
        client = Client.objects.create(
            client_type="public",
            name="Test Public Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is None

    def test_public_client_secret_forced_to_none_even_if_provided(self):
        """Verify any provided secret is removed for public clients."""
        client = Client.objects.create(
            client_type="public",
            client_secret="should_be_removed",
            name="Test Public Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is None

    def test_credentials_not_overwritten_on_update(self):
        """Verify credentials are not overwritten when updating client."""
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

    def test_provided_client_id_is_preserved(self):
        """Verify explicitly provided client_id is preserved."""
        custom_id = "custom_client_id_12345"
        client = Client.objects.create(
            client_id=custom_id,
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_id == custom_id

    def test_provided_client_secret_is_preserved(self):
        """Verify explicitly provided client_secret is preserved for confidential clients."""
        custom_secret = "custom_secret_12345"
        client = Client.objects.create(
            client_type="confidential",
            client_secret=custom_secret,
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret == custom_secret

    def test_generated_credentials_are_url_safe(self):
        """Verify generated credentials contain only URL-safe characters."""
        client = Client.objects.create(
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert all(c.isalnum() or c in "-_" for c in client.client_id)
        assert all(c.isalnum() or c in "-_" for c in client.client_secret)


@pytest.mark.django_db
class TestRedirectUriValidation:
    """Tests for redirect URI validation during model validation.

    Covers TODO items:
    - Valid HTTPS URIs accepted
    - Valid HTTP localhost URIs accepted
    - Invalid HTTP non-localhost rejected
    - Fragment URIs rejected
    - Relative URIs rejected
    - Empty list rejected
    - Duplicate URIs rejected
    """

    def test_valid_https_uris_accepted(self):
        """Verify valid HTTPS URIs are accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.clean()

    def test_valid_https_uri_with_port_accepted(self):
        """Verify HTTPS URI with port is accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com:8443/callback"],
        )
        client.clean()

    def test_valid_https_uri_with_query_accepted(self):
        """Verify HTTPS URI with query parameters is accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback?param=value"],
        )
        client.clean()

    def test_valid_http_localhost_accepted(self):
        """Verify HTTP localhost URIs are accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["http://localhost/callback"],
        )
        client.clean()

    def test_valid_http_localhost_with_port_accepted(self):
        """Verify HTTP localhost with port is accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["http://localhost:8080/callback"],
        )
        client.clean()

    def test_valid_http_127_0_0_1_accepted(self):
        """Verify HTTP 127.0.0.1 is accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["http://127.0.0.1/callback"],
        )
        client.clean()

    def test_valid_http_ipv6_localhost_accepted(self):
        """Verify HTTP IPv6 localhost is accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["http://[::1]/callback"],
        )
        client.clean()

    def test_invalid_http_non_localhost_rejected(self):
        """Verify HTTP URIs for non-localhost are rejected."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["http://example.com/callback"],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_fragment_uris_rejected(self):
        """Verify URIs containing fragments are rejected."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback#fragment"],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_relative_uris_rejected(self):
        """Verify relative URIs (without scheme) are rejected."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["/callback"],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_empty_list_rejected(self):
        """Verify empty redirect_uris list is rejected."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_none_redirect_uris_rejected(self):
        """Verify None redirect_uris is rejected."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=None,
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_duplicate_uris_rejected(self):
        """Verify duplicate URIs in list are rejected."""
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

    def test_private_uri_scheme_accepted(self):
        """Verify private-use URI schemes (RFC 8252) are accepted."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["com.example.app:/callback"],
        )
        client.clean()


@pytest.mark.django_db
class TestIsValidRedirectUri:
    """Tests for Client.is_valid_redirect_uri() method.

    Covers TODO items:
    - Exact match returns True
    - Non-match returns False
    - Case sensitivity verified
    """

    def test_exact_match_returns_true(self):
        """Verify exact URI match returns True."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://example.com/callback") is True

    def test_non_match_returns_false(self):
        """Verify non-matching URI returns False."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://example.com/different") is False

    def test_partial_match_returns_false(self):
        """Verify partial URI match returns False (no prefix matching)."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert (
            client.is_valid_redirect_uri("https://example.com/callback/extra") is False
        )

    def test_case_sensitivity_path(self):
        """Verify URI path comparison is case-sensitive."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://example.com/Callback") is False

    def test_case_sensitivity_host(self):
        """Verify URI host comparison is case-sensitive."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.is_valid_redirect_uri("https://Example.com/callback") is False

    def test_multiple_uris_exact_match(self):
        """Verify matching works with multiple registered URIs."""
        client = Client.objects.create(
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
class TestGetRedirectUri:
    """Tests for Client.get_redirect_uri() method.

    Covers TODO items:
    - With matching URI provided
    - With non-matching URI provided
    - With no URI and single registered
    - With no URI and multiple registered
    """

    def test_with_matching_uri_provided(self):
        """Verify matching URI is returned when provided."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        result = client.get_redirect_uri("https://example.com/callback")
        assert result == "https://example.com/callback"

    def test_with_non_matching_uri_provided(self):
        """Verify None is returned for non-matching URI."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.get_redirect_uri("https://example.com/different") is None

    def test_with_no_uri_and_single_registered(self):
        """Verify single registered URI is returned when none provided."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.get_redirect_uri() == "https://example.com/callback"

    def test_with_no_uri_and_multiple_registered(self):
        """Verify None is returned when multiple URIs registered and none provided."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=[
                "https://example.com/callback1",
                "https://example.com/callback2",
            ],
        )
        assert client.get_redirect_uri() is None

    def test_with_none_uri_and_single_registered(self):
        """Verify single registered URI is returned when None is passed."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.get_redirect_uri(None) == "https://example.com/callback"

    def test_with_none_uri_and_multiple_registered(self):
        """Verify None is returned when None passed with multiple URIs."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=[
                "https://example.com/callback1",
                "https://example.com/callback2",
            ],
        )
        assert client.get_redirect_uri(None) is None


@pytest.mark.django_db
class TestModelValidationCleanMethod:
    """Tests for Client.clean() validation method.

    Covers TODO item: clean() method validation
    """

    def test_clean_passes_for_valid_client(self):
        """Verify clean() passes for a valid client configuration."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.clean()

    def test_clean_validates_redirect_uris_required(self):
        """Verify clean() validates that redirect_uris is required."""
        client = Client(
            client_id="test_client",
            client_type="public",
            name="Test Client",
            redirect_uris=[],
        )
        with pytest.raises(ValidationError) as exc_info:
            client.clean()
        assert "redirect_uris" in exc_info.value.error_dict

    def test_clean_validates_confidential_client_requires_secret(self):
        """Verify clean() requires secret for existing confidential clients."""
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
        """Verify clean() passes for confidential client with secret."""
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
        """Verify clean() removes secret from public clients."""
        client = Client(
            client_id="test_client_id",
            client_secret="should_be_removed",
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        client.clean()
        assert client.client_secret is None


@pytest.mark.django_db
class TestModelValidationSaveMethod:
    """Tests for Client.save() method behavior.

    Covers TODO item: save() method behavior
    """

    def test_save_generates_client_id_only_on_create(self):
        """Verify client_id is only generated for new clients."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        original_id = client.client_id

        client.name = "Updated Name"
        client.save()

        assert client.client_id == original_id

    def test_save_generates_secret_only_on_create_for_confidential(self):
        """Verify client_secret is only generated for new confidential clients."""
        client = Client.objects.create(
            client_type="confidential",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        original_secret = client.client_secret

        client.name = "Updated Name"
        client.save()

        assert client.client_secret == original_secret

    def test_save_sets_public_client_secret_to_none(self):
        """Verify save() sets client_secret to None for public clients."""
        client = Client.objects.create(
            client_type="public",
            client_secret="should_be_removed",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        assert client.client_secret is None

    def test_save_updates_updated_at_timestamp(self):
        """Verify updated_at changes on save."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        original_updated_at = client.updated_at

        client.name = "Updated Name"
        client.save()
        client.refresh_from_db()

        assert client.updated_at >= original_updated_at

    def test_save_preserves_created_at_timestamp(self):
        """Verify created_at does not change on update."""
        client = Client.objects.create(
            client_type="public",
            name="Test Client",
            redirect_uris=["https://example.com/callback"],
        )
        original_created_at = client.created_at

        client.name = "Updated Name"
        client.save()
        client.refresh_from_db()

        assert client.created_at == original_created_at
