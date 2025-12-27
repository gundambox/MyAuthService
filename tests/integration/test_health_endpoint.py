import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_version_endpoint(api_client):
    url = reverse("health-check")
    resp = api_client.get(url, format="json")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
