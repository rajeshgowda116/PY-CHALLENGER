"""
Compatibility WSGI entrypoint for platforms still configured to run
`gunicorn app:app`.
"""

from config.wsgi import application

# Gunicorn expects a module-level callable named `app` for `gunicorn app:app`.
app = application
