import importlib
import os
from copy import copy

from django.conf import ENVIRONMENT_VARIABLE as DJANGO_SETTINGS_ENVIRONMENT_VARIABLE
from django.conf import settings, Settings


def initialize_settings():
    if settings.configured:
        return

    default_settings = Settings("kition_djangodefaults.settings.default")

    SETTINGS_MODULE = os.environ.get(DJANGO_SETTINGS_ENVIRONMENT_VARIABLE)
    django_settings_module = importlib.import_module(SETTINGS_MODULE)

    django_settings_module_processed = copy(django_settings_module.__dict__)
    for key in django_settings_module.__dict__.keys():
        if not key.isupper():
            django_settings_module_processed.pop(key)

    settings.configure(default_settings, **django_settings_module_processed)
