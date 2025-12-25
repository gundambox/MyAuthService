"""Smoke tests to verify the test infrastructure is working."""


def test_basic():
    """Basic test to ensure pytest runs correctly."""
    assert True


def test_import_django():
    """Verify Django can be imported."""
    import django

    assert django.VERSION >= (6, 0)  # Adjust version as needed
