"""
Utility functions for file handling, text processing, and document management.

This module provides functionality for:
- Extracting text from PDF files
- Chunking text into smaller segments for processing
- Saving uploaded files with unique identifiers
"""

import uuid
from pathlib import Path

from pypdf import PdfReader

UPLOADS_DIR = '.instance/uploads'


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        file_path (str): Path to the PDF file to extract text from.

    Returns:
        str: Extracted text content from all pages, with newlines stripped.
    """
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Split text into overlapping chunks for processing.

    Args:
        text (str): The text to be chunked.
        chunk_size (int, optional): Number of words per chunk. Defaults to 500.
        overlap (int, optional): Number of words to overlap between chunks. Defaults to 50.

    Returns:
        list[str]: List of text chunks with specified overlap.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


async def save_upload(file) -> str:
    """
    Save an uploaded file with a unique filename to prevent overwriting.

    Args:
        file: The uploaded file object with filename and read() method.

    Returns:
        str: Path to the saved file with unique identifier appended.
    """
    uploads_dir = Path(UPLOADS_DIR)
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # file_path = uploads_dir / file.filename
    original_path = Path(file.filename)
    unique_filename = (
        f'{original_path.stem}_{uuid.uuid4().hex[:8]}{original_path.suffix}'
    )
    file_path = uploads_dir / unique_filename

    with open(file_path, 'wb') as f:
        f.write(await file.read())
    return str(file_path)
