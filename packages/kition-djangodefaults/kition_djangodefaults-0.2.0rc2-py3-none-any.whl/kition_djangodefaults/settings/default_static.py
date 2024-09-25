import importlib
import os
from pathlib import Path

from django.conf import ENVIRONMENT_VARIABLE as DJANGO_SETTINGS_ENVIRONMENT_VARIABLE

# Setting the BASE_DIR to be the grandparent of the DJANGO_SETTINGS_MODULE
SETTINGS_MODULE = os.environ.get(DJANGO_SETTINGS_ENVIRONMENT_VARIABLE)
django_settings_module = importlib.import_module(SETTINGS_MODULE)
BASE_DIR = Path(django_settings_module.__file__).resolve().parent.parent

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
