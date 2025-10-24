try:
	from .celery import app as celery_app
except Exception:
	# Celery may not be installed in the current environment (dev). Fall back gracefully.
	celery_app = None

__all__ = ('celery_app',)