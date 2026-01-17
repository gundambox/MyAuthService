# Redirect URI Validation Rules

## Overview

Redirect URIs are critical security components in OAuth 2.0 authorization flows. Each OAuth 2.0 client must register one or more whitelisted redirect URIs to prevent authorization code interception attacks.

## RFC Standards

This implementation follows these RFC standards:

- **RFC 6749 Section 3.1.2**: OAuth 2.0 Redirect URI Requirements
- **RFC 6749 Section 3.1.2.2**: Redirect URI Matching Rules (exact string match)
- **RFC 8252**: OAuth 2.0 for Native Apps (allows localhost and private URI schemes)

## Validation Rules

### Requirements

Each redirect URI must meet the following requirements:

1. **Absolute URI**: Must include a scheme (and host/path depending on scheme)
2. **No Fragment**: Must NOT contain a fragment component (`#`)
3. **Allowed Schemes**:
   - `https://` (required for production)
   - `http://localhost`, `http://127.0.0.1`, or `http://[::1]` (development only)
   - Any private-use URI schemes (e.g., `com.example.app:/callback`, `myapp://callback`)

**Note**: Private-use URI schemes are primarily for native applications (mobile apps, desktop apps), as allowed by RFC 8252.

### Validation Timing

Validation occurs at two points:

1. **Registration Time**: URI format is validated when creating or updating a client
2. **Authorization Time**: The `redirect_uri` parameter in authorization requests must exactly match a registered URI

### Matching Rules

- Uses **exact string match** (RFC 6749 Section 3.1.2.2)
- No partial matching or prefix matching allowed
- Case-sensitive comparison

## Examples

### Valid Redirect URIs

```python
# HTTPS (production)
"https://example.com/callback"
"https://example.com:8443/oauth/callback"
"https://example.com/callback?param=value"

# HTTP localhost (development)
"http://localhost/callback"
"http://localhost:8080/callback"
"http://127.0.0.1/callback"
"http://[::1]/callback"

# Private URI schemes (native apps)
"com.example.app:/callback"
"myapp://oauth/callback"
"my.app://callback"
```

### Invalid Redirect URIs

```python
# HTTP non-localhost (security risk)
"http://example.com/callback"  # ❌

# Contains fragment
"https://example.com/callback#section"  # ❌

# Relative URI
"/callback"  # ❌

# Missing scheme
"example.com/callback"  # ❌
```

## Usage

### Creating a Client

```python
from oauth2.models import Client

client = Client.objects.create(
    client_id="my_client_id",
    client_type="public",
    name="My Application",
    redirect_uris=[
        "https://example.com/callback",
        "http://localhost:8080/callback",
    ]
)
```

### Validating Redirect URI

```python
# Check if URI is whitelisted
is_valid = client.is_valid_redirect_uri("https://example.com/callback")

# Get redirect URI
# If URI provided: validate and return; if not provided and only one registered: return that URI
redirect_uri = client.get_redirect_uri("https://example.com/callback")

# If URI not provided and only one registered URI, auto-use that URI
redirect_uri = client.get_redirect_uri()  # Single URI: returns it; Multiple URIs: returns None
```

## Security Considerations

### Why Exact Match?

Partial matching or prefix matching can lead to security vulnerabilities:

```python
# If prefix matching were allowed
registered: "https://example.com/callback"
attacker uses: "https://example.com/callback.evil.com"  # ❌ might be accepted
```

### Why Prohibit Fragments?

Fragments are not sent to the server and can lead to authorization code leakage:

```python
# Fragment only exists in browser
"https://example.com/callback#code=AUTH_CODE"  # ❌ server doesn't receive code
```

### Why Require HTTPS?

HTTP transmission is unencrypted and can lead to authorization code interception during transit. Exceptions:

- `http://localhost`: For development, traffic doesn't leave the machine
- Private URI schemes: For native apps, not transmitted over network

## Multiple Redirect URIs

Clients can register multiple redirect URIs to support different environments:

```python
redirect_uris = [
    "https://example.com/callback",           # Production
    "https://staging.example.com/callback",   # Staging
    "http://localhost:8080/callback",         # Development
]
```

**Note**: Each URI must be explicitly registered; wildcards are not allowed.

## Admin Interface

The Django Admin interface provides:

- Real-time validation error display
- Format examples and requirement descriptions
- Support for managing multiple URIs

## Testing

Validation logic includes comprehensive test coverage:

```bash
# Run all tests
make test

# Run redirect URI related tests
docker compose run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test app pytest tests/unit/test_redirect_uri_validators.py
docker compose run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test app pytest tests/unit/test_client_redirect_uri.py
```

## Error Messages

The system provides clear error messages:

```python
# Empty list
ValidationError: "At least one redirect URI is required."

# Invalid scheme
ValidationError: "Redirect URI must include a scheme: /callback"

# HTTP non-localhost
ValidationError: "HTTP redirect URIs are only allowed for localhost: http://example.com/callback"

# Contains fragment
ValidationError: "Redirect URI must not contain a fragment: https://example.com/callback#section"

# Duplicate URI
ValidationError: "Duplicate redirect URI: https://example.com/callback"
```