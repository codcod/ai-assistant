"""
HTTP API routes for the document assistant application.

This module defines the web API endpoints for:
- Asking questions about uploaded documents
- Uploading PDF and text files
- Processing and storing document content
"""

from litestar import Request, post
from litestar.datastructures import UploadFile
from pydantic import BaseModel

from .embeddings import add_document
from .rag import rag_answer
from .storage import save_store
from .utils import chunk_text, extract_text_from_pdf, save_upload


class AskRequest(BaseModel):
    question: str


class UploadRequest(BaseModel):
    text: str


@post('/ask')
async def ask(data: AskRequest) -> dict:
    """
    Answer questions based on uploaded documents.

    Uses RAG (Retrieval-Augmented Generation) to find relevant document chunks
    and generate an answer based on the context.

    Args:
        data (AskRequest): Request containing the question to answer.

    Returns:
        dict: Response containing the original question and generated answer.
    """
    answer = rag_answer(data.question)
    return {'question': data.question, 'answer': answer}


@post('/upload/pdf')
async def upload_pdf(request: Request) -> dict:
    """
    Upload and process a PDF file for document search.

    Extracts text from the uploaded PDF, chunks it, and adds to the vector store.

    Args:
        request (Request): HTTP request containing the PDF file in form data.

    Returns:
        dict: Response indicating success and number of chunks added.
    """
    form_data = await request.form()
    file = form_data.get('file')
    if not isinstance(file, UploadFile):
        return {'error': 'No file uploaded'}

    path = await save_upload(file)
    text = extract_text_from_pdf(path)
    chunks = chunk_text(text)
    for chunk in chunks:
        add_document(chunk)
    save_store()
    return {'status': 'ok', 'chunks_added': len(chunks)}


@post('/upload/text')
async def upload_text(request: Request) -> dict:
    """
    Upload and process a text file for document search.

    Reads the uploaded text file, chunks it, and adds to the vector store.

    Args:
        request (Request): HTTP request containing the text file in form data.

    Returns:
        dict: Response indicating success and number of chunks added.
    """
    form_data = await request.form()
    file = form_data.get('file')
    if not isinstance(file, UploadFile):
        return {'error': 'No file uploaded'}

    path = await save_upload(file)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    chunks = chunk_text(text)
    for chunk in chunks:
        add_document(chunk)
    save_store()
    return {'status': 'ok', 'chunks_added': len(chunks)}


@post('/upload')
async def upload(data: UploadRequest) -> dict:
    """
    Upload text content directly for document search.

    Adds the provided text directly to the vector store without file handling.

    Args:
        data (UploadRequest): Request containing the text to add.

    Returns:
        dict: Response indicating successful addition.
    """
    add_document(data.text)
    return {'status': 'ok', 'message': 'Document added'}
