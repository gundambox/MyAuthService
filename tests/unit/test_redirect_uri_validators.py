import pytest
from django.core.exceptions import ValidationError
from oauth2.validators import validate_redirect_uri, validate_redirect_uris


class TestValidateRedirectUri:
    def test_valid_https_uri(self):
        uri = "https://example.com/callback"
        assert validate_redirect_uri(uri) == uri

    def test_valid_https_uri_with_port(self):
        uri = "https://example.com:8443/callback"
        assert validate_redirect_uri(uri) == uri

    def test_valid_https_uri_with_query(self):
        uri = "https://example.com/callback?param=value"
        assert validate_redirect_uri(uri) == uri

    def test_valid_http_localhost(self):
        assert (
            validate_redirect_uri("http://localhost/callback")
            == "http://localhost/callback"
        )
        assert (
            validate_redirect_uri("http://localhost:8080/callback")
            == "http://localhost:8080/callback"
        )
        assert (
            validate_redirect_uri("http://127.0.0.1/callback")
            == "http://127.0.0.1/callback"
        )
        assert validate_redirect_uri("http://[::1]/callback") == "http://[::1]/callback"

    def test_valid_private_use_scheme(self):
        uri = "com.example.app:/callback"
        assert validate_redirect_uri(uri) == uri

    def test_valid_custom_scheme(self):
        uri = "myapp://callback"
        assert validate_redirect_uri(uri) == uri

    def test_valid_custom_scheme_with_dots(self):
        assert validate_redirect_uri("my.app://callback") == "my.app://callback"
        assert (
            validate_redirect_uri("com.example.app://callback")
            == "com.example.app://callback"
        )

    def test_invalid_http_non_localhost(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("http://example.com/callback")
        assert "HTTP redirect URIs are only allowed for localhost" in str(
            exc_info.value
        )

    def test_invalid_uri_with_fragment(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("https://example.com/callback#fragment")
        assert "must not contain a fragment" in str(exc_info.value)

    def test_invalid_relative_uri(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("/callback")
        assert "must include a scheme" in str(exc_info.value)

    def test_invalid_empty_uri(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("")
        assert "must be a non-empty string" in str(exc_info.value)

    def test_invalid_none_uri(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri(None)
        assert "must be a non-empty string" in str(exc_info.value)

    # New tests for host validation
    def test_invalid_https_without_host(self):
        """Verify HTTPS URI without host is rejected (RFC 6749 compliance)."""
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("https:///callback")
        assert "must include a host" in str(exc_info.value)

    def test_invalid_https_empty_authority(self):
        """Verify HTTPS URI with empty authority is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("https:///")
        assert "must include a host" in str(exc_info.value)

    def test_invalid_http_without_host(self):
        """Verify HTTP URI without host is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("http:///callback")
        assert "must include a host" in str(exc_info.value)

    def test_invalid_http_empty_authority(self):
        """Verify HTTP URI with empty authority is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uri("http:///")
        assert "must include a host" in str(exc_info.value)


class TestValidateRedirectUris:
    def test_valid_single_uri(self):
        uris = ["https://example.com/callback"]
        assert validate_redirect_uris(uris) == uris

    def test_valid_multiple_uris(self):
        uris = [
            "https://example.com/callback",
            "https://example.com/callback2",
            "http://localhost:8080/callback",
        ]
        assert validate_redirect_uris(uris) == uris

    def test_invalid_empty_list(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uris([])
        assert "At least one redirect URI is required" in str(exc_info.value)

    def test_invalid_none(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uris(None)
        assert "At least one redirect URI is required" in str(exc_info.value)

    def test_invalid_not_list(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uris("https://example.com/callback")
        assert "must be a list" in str(exc_info.value)

    def test_duplicate_uris(self):
        uris = [
            "https://example.com/callback",
            "https://example.com/callback",
        ]
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uris(uris)
        assert "Duplicate redirect URI" in str(exc_info.value)

    def test_invalid_uri_in_list(self):
        uris = [
            "https://example.com/callback",
            "http://example.com/callback",
        ]
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uris(uris)
        assert "HTTP redirect URIs are only allowed for localhost" in str(
            exc_info.value
        )

    def test_mixed_valid_schemes(self):
        uris = [
            "https://example.com/callback",
            "http://localhost/callback",
            "myapp://callback",
        ]
        assert validate_redirect_uris(uris) == uris

    # New tests for host validation in list
    def test_invalid_https_without_host_in_list(self):
        """Verify HTTPS URI without host in list is rejected."""
        uris = [
            "https://example.com/callback",
            "https:///callback",
        ]
        with pytest.raises(ValidationError) as exc_info:
            validate_redirect_uris(uris)
        assert "must include a host" in str(exc_info.value)
