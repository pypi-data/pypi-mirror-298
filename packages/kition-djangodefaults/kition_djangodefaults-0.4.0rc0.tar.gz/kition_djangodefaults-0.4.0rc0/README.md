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
2. Start your applications settings file with the default setting initialization
   ```python
   from kition_djangodefaults import initialize_default_settings

   initialize_default_settings(__name__)
   ```
3. (Optional) configure any of the following components.

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