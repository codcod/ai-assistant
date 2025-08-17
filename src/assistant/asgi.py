"""
ASGI application entry point for the document assistant.

This module creates and configures the Litestar application with
all route handlers and middleware.
"""

from litestar import Litestar

from .routes import ask, list_docs, reset_docs, upload, upload_pdf, upload_text
from .storage import get_collection


def on_startup():
    # Trigger Chroma load
    col = get_collection()
    print(f'Loaded Chroma collection with {len(col.get()["ids"])} documents')


app = Litestar(
    route_handlers=[ask, upload, upload_pdf, upload_text, list_docs, reset_docs],
    path='/api/v1',
    on_startup=[on_startup],
)
