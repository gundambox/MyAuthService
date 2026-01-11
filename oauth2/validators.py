from urllib.parse import urlparse
from django.core.exceptions import ValidationError


def validate_redirect_uri(uri):
    if not uri or not isinstance(uri, str):
        raise ValidationError("Redirect URI must be a non-empty string.")

    parsed = urlparse(uri)

    if not parsed.scheme:
        raise ValidationError(f"Redirect URI must include a scheme: {uri}")

    if not parsed.netloc and parsed.scheme not in ["http", "https"]:
        if not parsed.path:
            raise ValidationError(f"Redirect URI must be absolute: {uri}")

    if parsed.fragment:
        raise ValidationError(f"Redirect URI must not contain a fragment: {uri}")

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    if scheme == "https":
        if not netloc:
            raise ValidationError(f"HTTPS redirect URI must include a host: {uri}")
        return uri
    elif scheme == "http":
        if not netloc:
            raise ValidationError(f"HTTP redirect URI must include a host: {uri}")
        if netloc in ["localhost", "127.0.0.1", "[::1]"] or netloc.startswith(
            "localhost:"
        ):
            return uri
        else:
            raise ValidationError(
                f"HTTP redirect URIs are only allowed for localhost: {uri}"
            )
    else:
        # Allow private URI schemes (RFC 8252)
        # e.g., com.example.app:/callback, myapp://callback
        return uri


def validate_redirect_uris(uris):
    if not uris:
        raise ValidationError("At least one redirect URI is required.")

    if not isinstance(uris, list):
        raise ValidationError("Redirect URIs must be a list.")

    validated = []
    seen = set()

    for uri in uris:
        validated_uri = validate_redirect_uri(uri)

        if validated_uri in seen:
            raise ValidationError(f"Duplicate redirect URI: {validated_uri}")

        seen.add(validated_uri)
        validated.append(validated_uri)

    return validated
