# Security Policy

## Overview

MyAuthService is an OAuth2 authentication server that handles sensitive authentication flows and user credentials. Security is a top priority for this project, and we take all security vulnerabilities seriously.

If you discover a security vulnerability, please follow the responsible disclosure process outlined below.

---

## Supported Versions

As a solo development project, security updates are provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

**Note:** This project is currently in active development. Once version 1.0 is released, this table will be updated to reflect specific version support.

---

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

### Preferred Method: GitHub Security Advisories

The preferred way to report a vulnerability is through GitHub's private vulnerability reporting feature:

1. Navigate to the [Security tab](https://github.com/gundambox/MyAuthService/security) of this repository
2. Click "Report a vulnerability"
3. Fill out the vulnerability details form with as much information as possible

### Alternative Method: Private Email

If you prefer not to use GitHub Security Advisories, you can report vulnerabilities via email:

- **Email:** [Create a private security issue and request email contact]
- **Subject line:** `[SECURITY] Brief description of the issue`

### What to Include in Your Report

To help us understand and address the issue quickly, please include:

- **Description:** Clear description of the vulnerability
- **Impact:** What an attacker could achieve by exploiting this vulnerability
- **Steps to reproduce:** Detailed steps to reproduce the issue
- **Affected components:** Which parts of the system are affected (e.g., OAuth2 token endpoint, user authentication)
- **Proof of concept:** Code or screenshots demonstrating the vulnerability (if applicable)
- **Suggested fix:** If you have ideas on how to fix it (optional but appreciated)
- **Your environment:** Python version, deployment method, etc. (if relevant)

### What NOT to Do

- Do not publicly disclose the vulnerability before it has been addressed
- Do not exploit the vulnerability beyond what is necessary to demonstrate it
- Do not access, modify, or delete data that does not belong to you
- Do not perform actions that could harm the service or its users

---

## Response Timeline

**Important:** This is a practice/learning project maintained by a solo developer. While security is taken seriously, response timelines cannot be guaranteed.

- **Best effort response:** Security reports will be addressed as time permits
- **Priority:** Critical vulnerabilities affecting authentication flows will be prioritized
- **No SLA:** This project does not provide service level agreements or guaranteed response times

If you discover a critical security vulnerability and do not receive a timely response, you may choose to:
- Follow standard responsible disclosure practices (typically 90 days before public disclosure)
- Publicly disclose immediately if the vulnerability poses active risk to users

---

## What Happens After You Report

When a security report is received, the following process will be followed (timeline permitting):

1. **Acknowledgment:** Receipt of your report will be acknowledged when possible

2. **Validation:** Reproduction and validation of the vulnerability

3. **Assessment:** Severity and impact assessment using the CVSS framework

4. **Fix development:** Development and testing of a fix

5. **Disclosure coordination:** Coordination on the disclosure timeline
   - You'll be notified before any public disclosure (when feasible)
   - You'll be credited in the security advisory (unless you prefer to remain anonymous)

6. **Public disclosure:** Once a fix is deployed:
   - Publish a security advisory
   - Release a patched version
   - Update the changelog with security fix details

**Note:** Given this is a practice project, if you need immediate action on a critical vulnerability, consider public disclosure after a reasonable waiting period.

---

## Security Best Practices for Deployment

If you're deploying MyAuthService, please follow these security guidelines:

### Environment Configuration

- Use strong, randomly generated `SECRET_KEY` (minimum 50 characters)
- Enable `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` with your specific domain(s)
- Use HTTPS/TLS for all connections
- Set secure cookie flags (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)

### Database Security

- Use strong database passwords
- Restrict database access to application containers only
- Enable database connection encryption
- Regularly backup encrypted data

### OAuth2 Security

- Use strong client secrets for OAuth2 applications
- Implement rate limiting on authentication endpoints
- Set appropriate token expiration times
- Use PKCE (Proof Key for Code Exchange) for public clients
- Validate redirect URIs strictly

### Infrastructure

- Keep Docker images and dependencies up to date
- Use container security scanning tools
- Implement network segmentation
- Enable logging and monitoring
- Regularly review access logs for suspicious activity

---

## Security-Related Configuration

The following configuration options have security implications:

```python
# settings/production.py

SECRET_KEY = os.environ.get("SECRET_KEY")  # Must be strong and secret
DEBUG = False  # Never True in production
ALLOWED_HOSTS = ["yourdomain.com"]  # Specific domains only

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

Refer to [Django's security documentation](https://docs.djangoproject.com/en/stable/topics/security/) for comprehensive security guidance.

---

## Known Security Considerations

### Current Development Status

**This is a practice/learning project.** While security best practices are followed, please note:

- This is a solo practice project and has not undergone professional security audit
- **Not recommended for production use** - this is for learning purposes
- Security updates are best-effort and depend on available time
- Active maintenance is not guaranteed

### OAuth2 Implementation

This project implements OAuth2 authentication flows. Key security considerations:

- Authorization code flow with PKCE is recommended for all client types
- Client credentials must be stored securely
- Token storage and transmission must use secure channels
- Scope-based access control should be properly implemented

---

## Scope

### In Scope

The following are in scope for vulnerability reports:

- Authentication and authorization bypasses
- OAuth2 flow vulnerabilities
- SQL injection, XSS, CSRF, and other OWASP Top 10 issues
- Sensitive data exposure
- Token theft or manipulation
- Privilege escalation
- Denial of service (DoS) vulnerabilities
- Dependency vulnerabilities with demonstrated impact

### Out of Scope

The following are generally out of scope:

- Vulnerabilities in dependencies without demonstrated exploitability
- Social engineering attacks
- Physical attacks
- Denial of service attacks requiring excessive resources
- Issues in third-party services or libraries (please report to those projects)
- Theoretical vulnerabilities without proof of concept

---

## Recognition

We appreciate the security research community's efforts in responsible disclosure. If you report a valid security vulnerability:

- You'll be credited in the security advisory (unless you prefer anonymity)
- Your contribution will be acknowledged in the project's changelog
- You'll be listed in a "Security Researchers" section (if desired)

---

## Questions?

If you have questions about this security policy or need clarification on the reporting process, please open a regular (non-security) issue or discussion on GitHub.

Thank you for helping keep MyAuthService and its users safe!

---

**Last updated:** 2026-01-02
