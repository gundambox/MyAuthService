import secrets


def generate_client_id():
    return secrets.token_urlsafe(32)


def generate_client_secret():
    return secrets.token_urlsafe(48)


def generate_unique_client_id(model_class, max_retries=5):
    for _ in range(max_retries):
        client_id = generate_client_id()
        if not model_class.objects.filter(client_id=client_id).exists():
            return client_id
    raise RuntimeError(
        f"Failed to generate unique client_id after {max_retries} attempts"
    )
