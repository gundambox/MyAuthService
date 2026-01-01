# Contributing to MyAuthService

Thank you for your interest in contributing to MyAuthService! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Development Workflow (GitHub Flow)](#development-workflow-github-flow)
- [Getting Started](#getting-started)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Format](#commit-message-format)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Docker and Makefile Commands](#docker-and-makefile-commands)

---

## Development Workflow (GitHub Flow)

We follow **GitHub Flow**, a lightweight, branch-based workflow:

1. **Main branch (`main`) is always deployable** - The `main` branch should always be in a working state.
2. **Create a feature branch** - All work happens in feature branches created from `main`.
3. **Commit your changes** - Make commits with clear, descriptive messages.
4. **Open a Pull Request (PR)** - Open a PR early for discussion and feedback.
5. **Review and discuss** - Collaborate on the PR with reviews and discussions.
6. **Merge after approval** - Once approved and tests pass, merge into `main`.
7. **Delete the feature branch** - Clean up by deleting the merged branch.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- A GitHub account

### Initial Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/MyAuthService. git
   cd MyAuthService
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY and other required variables
   ```

3. **Build and start the Docker containers:**

   ```bash
   make build
   make up
   ```

4. **Run migrations:**

   ```bash
   make migrate
   ```

5. **Verify the setup by running tests:**

   ```bash
   make test
   ```

---

## Branch Naming Conventions

Use descriptive branch names that indicate the type and purpose of the work:

**Format:** `<type>/<short-description>`

**Types:**
- `feature/` - New features or enhancements
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes for production issues
- `refactor/` - Code refactoring without changing functionality
- `docs/` - Documentation updates
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks (dependencies, configuration)

**Examples:**
```
feature/add-oauth2-token-endpoint
bugfix/fix-login-500-error
docs/update-contributing-guide
test/add-integration-tests-for-auth
refactor/reorganize-settings-structure
chore/update-django-dependencies
```

**Best Practices:**
- Use lowercase and hyphens (kebab-case)
- Keep names concise but descriptive
- Reference issue numbers when applicable:  `feature/42-add-oauth2-endpoint`

---

## Commit Message Format

Write clear, meaningful commit messages that explain **what** changed and **why**.

**Format:**
```
<type>: <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat` - A new feature
- `fix` - A bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, missing semi-colons, etc.)
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks (build, CI, dependencies)

**Examples:**

```
feat: add token endpoint for OAuth2 authorization code flow

Implements the /oauth2/token endpoint that exchanges authorization
codes for access tokens according to RFC 6749 section 4.1.3.

Related to #42
```

```
fix: return 400 instead of 500 for invalid authorization code

The token endpoint was raising an unhandled exception when receiving
an invalid authorization code, resulting in a 500 error. Now it
properly validates the code and returns 400 with an appropriate
error message.

Related to #58
```

```
docs: update README with Docker setup instructions
```

**Best Practices:**
- Use the imperative mood ("add" not "added" or "adds")
- First line should be 50 characters or less
- Reference issues using `#<issue>` syntax to link without auto-closing
- Separate subject from body with a blank line
- Wrap body at 72 characters

### Referencing Issues in Commits

Always reference related issues in your commit messages to create automatic links and improve traceability.

**Linking to issues (without auto-closing):**

Use the `#` symbol followed by the issue number anywhere in your commit message:

```
feat: add token endpoint for OAuth2 #42

Implements the /oauth2/token endpoint that exchanges authorization
codes for access tokens according to RFC 6749 section 4.1.3.
```

Or:
```
fix: return 400 instead of 500 for invalid code

The token endpoint was raising an unhandled exception when receiving
an invalid authorization code (#58), resulting in a 500 error. Now it
properly validates the code and returns 400 with an appropriate error.
```

**Multiple issues:**
```
refactor: reorganize authentication middleware

Updates authentication flow to support multiple token types.

Related: #45, #47, #52
```

**Guidelines:**
- Use `#<number>` anywhere in the commit message to link to issues or PRs
- GitHub will automatically create clickable links
- Place issue references where they make sense contextually (subject line or body)
- Issues will be linked but not automatically closed
- Close issues manually or via PR descriptions when work is complete

---

## Making Changes

### Development Process

1. **Create a feature branch from `main`:**

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** in the appropriate files.

3. **Start the development environment:**

   ```bash
   make up
   ```

4. **Run the development server** (already running via docker-compose):
   - The app is accessible at `http://localhost:8000`
   - Changes to Python files will trigger auto-reload

5. **Access the container shell if needed:**

   ```bash
   make shell
   ```

6. **Format your code:**

   ```bash
   # Inside the container (after `make shell`)
   black .
   ```

   Or run black without entering the shell:

   ```bash
   docker compose exec app black .
   ```

7. **Lint your code:**

   ```bash
   # Inside the container
   flake8 .
   ```

   Or:

   ```bash
   docker compose exec app flake8 .
   ```

8. **Write tests** for your changes (see [Testing](#testing) section).

9. **Run tests** to ensure everything works:

   ```bash
   make test
   ```

10. **Commit your changes** with a clear commit message:

    ```bash
    git add .
    git commit -m "feat: add your feature description"
    ```

11. **Push your branch** to your fork:

    ```bash
    git push origin feature/your-feature-name
    ```

---

## Pull Request Process

### Before Opening a PR

- [ ] Code follows the project's code style (see [Code Style](#code-style))
- [ ] All tests pass (`make test`)
- [ ] Code is formatted with `black`
- [ ] Code passes `flake8` linting
- [ ] New tests are added for new features or bug fixes
- [ ] Documentation is updated if needed
- [ ] Commits follow the commit message format
- [ ] Branch is up-to-date with `main`

### Opening a PR

1. **Push your branch** to your fork on GitHub.

2. **Open a Pull Request** from your fork to the main repository's `main` branch.

3. **Fill out the PR template** (if available) with:
   - Description of changes
   - Related issue numbers (e.g., "Related to #42" or use "Closes #42" to auto-close when PR merges)
   - Testing steps
   - Screenshots (if applicable)

4. **Request a review** from maintainers or other contributors.

### PR Title Format

Use a clear, descriptive title that follows the commit message format:

```
<type>: <description>
```

**Examples:**
- `feat: add OAuth2 token endpoint`
- `fix: resolve 500 error on invalid auth code`
- `docs: add contribution guidelines`

### During Review

- Respond to feedback promptly and professionally
- Make requested changes in new commits
- Push updates to the same branch (the PR will update automatically)
- Re-request review after addressing feedback

### After Approval

- Maintainers will merge your PR
- Your feature branch will be deleted
- Your contribution will be part of the next release!  🎉

---

## Code Style

We use `black` for code formatting and `flake8` for linting to maintain consistent code style.

### Black (Code Formatting)

- **Line length:** 120 characters
- **Target Python version:** 3.12
- **Configuration:** See `setup.cfg`

**Run black:**
```bash
# Format all files
docker compose exec app black .

# Or inside the container
make shell
black .
```

### Flake8 (Linting)

- **Max line length:** 120 characters
- **Ignored rules:** E203, W503 (for black compatibility)
- **Configuration:** See `setup.cfg`

**Run flake8:**
```bash
# Lint all files
docker compose exec app flake8 .

# Or inside the container
make shell
flake8 .
```

### Python Style Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Write docstrings for functions, classes, and modules
- Keep functions small and focused
- Prefer explicit over implicit code

---

## Testing

We use `pytest` with `pytest-django` for testing.

### Running Tests

**Run all tests:**
```bash
make test
```

This runs pytest inside the Docker container with the test settings.

**Run specific tests:**
```bash
# Run tests in a specific directory
docker compose run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test app pytest tests/integration/

# Run a specific test file
docker compose run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test app pytest tests/integration/test_health_endpoint.py

# Run a specific test function
docker compose run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test app pytest tests/integration/test_health_endpoint.py::test_version_endpoint
```

### Writing Tests

- Place tests in the `tests/` directory
- Follow the naming convention: `test_*.py`
- Use `pytest` fixtures for common setup
- Mark Django tests with `@pytest.mark.django_db` when database access is needed
- Write tests for both happy paths and edge cases
- Test files should mirror the project structure

**Test structure:**
```
tests/
├── __init__.py
├── test_smoke.py           # Basic smoke tests
├── integration/            # Integration tests
│   ├── conftest.py        # Shared fixtures
│   ├── test_health_endpoint.py
│   └── test_version_endpoint.py
└── unit/                   # Unit tests (if applicable)
```

**Example test:**
```python
import pytest
from django.urls import reverse


@pytest.mark. django_db
def test_health_check(api_client):
    """Test the health check endpoint returns 200 OK."""
    url = reverse("health-check")
    response = api_client.get(url, format="json")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

---

## Docker and Makefile Commands

We use Docker Compose for containerization and a Makefile for common commands.

### Makefile Commands

```bash
make help       # Show all available commands
make build      # Build Docker images
make up         # Start containers in detached mode
make down       # Stop containers
make down-v     # Stop containers and remove volumes (resets database)
make logs       # Follow container logs
make shell      # Open a bash shell in the app container
make migrate    # Run Django migrations
make test       # Run pytest with test settings
```

### Common Workflows

**Starting development:**
```bash
make build      # Build images (first time or after Dockerfile changes)
make up         # Start containers
make migrate    # Run migrations
```

**Daily development:**
```bash
make up         # Start containers
make logs       # View logs (optional)
# Make code changes...
make test       # Run tests
```

**Accessing the shell:**
```bash
make shell
# Now you're inside the container
python manage.py createsuperuser
python manage.py makemigrations
black .
flake8 .
exit
```

**Resetting the database:**
```bash
make down-v     # Remove volumes (deletes database)
make up         # Start fresh
make migrate    # Re-run migrations
```

**Stopping development:**
```bash
make down       # Stop containers (preserves database)
```

### Direct Docker Compose Commands

If you need more control, use `docker compose` directly:

```bash
docker compose ps                    # List containers
docker compose exec app bash         # Access shell
docker compose logs -f app           # Follow app logs
docker compose restart app           # Restart app service
docker compose run --rm app <cmd>    # Run one-off command
```

---

## Questions or Issues?

- **Found a bug?** Open an issue with the `[Bug]` label
- **Have a question?** Open a discussion or issue with the `[Question]` label
- **Need help?** Reach out to maintainers in the issue or PR

Thank you for contributing to MyAuthService! 🚀