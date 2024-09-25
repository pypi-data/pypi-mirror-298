# Kition Django Defaults

This package provides default configuration and components for Django projects.

## Motivation

Building, operating and maintaining many Django applications leads to repetitive code. This repository strives to reduce
the mental overhead by providing code that otherwise would have to be repeated.

## Installation

### Requirements

Python 3.12 and Django 5.1 supported.

### Installation

1. Install with **pip**:
   ```
   python -m pip install kition-djangodefaults
   ```
2. (Optional) configure any of the following components.

## Default Configuration

Use the default settings by calling `initialize_settings()` after defining the `DJANGO_SETTINGS_MODULE` within
`manage.py`.

Example

```python
import os
import sys

from kition_djangodefaults import initialize_settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")
    initialize_settings()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```

## Kubernetes Readiness Endpoint Middleware

Install via

```python
MIDDLEWARE = [
    # Putting the healthcheck middleware first to circumvent ALLOWED_HOSTS protections, which would fail Kubernetes
    # Readiness Probe requests.
    "kition_django_defaults.healthcheck.HealthCheckMiddleware",
    ...
]
```

## Development

```bash
poetry env use $(pyenv which python)
poetry install
```