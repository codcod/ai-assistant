"""
ASGI application entry point for the document assistant.

This module creates and configures the Litestar application with
all route handlers and middleware.
"""

from litestar import Litestar

from .routes import ask, upload, upload_pdf, upload_text

app = Litestar(route_handlers=[ask, upload, upload_pdf, upload_text], path='/api/v1')
