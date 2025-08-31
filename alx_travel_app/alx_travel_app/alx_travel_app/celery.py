# alx_travel_app/celery.py
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("alx_travel_app")

# Load configuration from Django settings with CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Set default broker connection retry setting (for Celery 5.3+)
app.conf.broker_connection_retry_on_startup = True

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Optional: Add task routing configuration if needed
# app.conf.task_routes = {
#     'listings.tasks.*': {'queue': 'listings'},
# }