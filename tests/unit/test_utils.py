import pytest
from unittest.mock import patch, MagicMock
from oauth2.utils import (
    generate_client_id,
    generate_client_secret,
    generate_unique_client_id,
)


class TestGenerateClientId:
    def test_generates_non_empty_string(self):
        client_id = generate_client_id()
        assert isinstance(client_id, str)
        assert len(client_id) > 0

    def test_generates_url_safe_string(self):
        client_id = generate_client_id()
        assert all(c.isalnum() or c in "-_" for c in client_id)

    def test_minimum_length(self):
        client_id = generate_client_id()
        assert len(client_id) >= 32

    def test_generates_unique_values(self):
        ids = [generate_client_id() for _ in range(100)]
        assert len(set(ids)) == 100


class TestGenerateClientSecret:
    def test_generates_non_empty_string(self):
        secret = generate_client_secret()
        assert isinstance(secret, str)
        assert len(secret) > 0

    def test_generates_url_safe_string(self):
        secret = generate_client_secret()
        assert all(c.isalnum() or c in "-_" for c in secret)

    def test_minimum_length(self):
        secret = generate_client_secret()
        assert len(secret) >= 48

    def test_generates_unique_values(self):
        secrets = [generate_client_secret() for _ in range(100)]
        assert len(set(secrets)) == 100


class TestGenerateUniqueClientId:
    def test_generates_unique_id_on_first_attempt(self):
        mock_model = MagicMock()
        mock_model.objects.filter.return_value.exists.return_value = False

        client_id = generate_unique_client_id(mock_model)

        assert isinstance(client_id, str)
        assert len(client_id) >= 32
        mock_model.objects.filter.assert_called_once()

    def test_retries_on_collision(self):
        mock_model = MagicMock()
        mock_model.objects.filter.return_value.exists.side_effect = [
            True,
            True,
            False,
        ]

        client_id = generate_unique_client_id(mock_model)

        assert isinstance(client_id, str)
        assert mock_model.objects.filter.call_count == 3

    def test_raises_error_after_max_retries(self):
        mock_model = MagicMock()
        mock_model.objects.filter.return_value.exists.return_value = True

        with pytest.raises(RuntimeError) as exc_info:
            generate_unique_client_id(mock_model, max_retries=5)

        assert "Failed to generate unique client_id after 5 attempts" in str(
            exc_info.value
        )
        assert mock_model.objects.filter.call_count == 5

    def test_custom_max_retries(self):
        mock_model = MagicMock()
        mock_model.objects.filter.return_value.exists.return_value = True

        with pytest.raises(RuntimeError):
            generate_unique_client_id(mock_model, max_retries=3)

        assert mock_model.objects.filter.call_count == 3
