"""
Vector embeddings module for document similarity search.

This module provides functionality for:
- Adding documents to a vector store using ChromaDB
- Converting text to embeddings using SentenceTransformers
- Searching for similar documents based on semantic similarity
"""

import uuid

from .storage import get_collection

collection = get_collection()


def add_document(text: str, metadata: dict | None = None) -> None:
    """
    Add a document to the vector store.

    Converts the input text to a vector embedding and stores it in the ChromaDB
    collection along with the original text for retrieval.

    Args:
        text (str): The document text to add to the vector store.
        metadata (dict | None, optional): Additional metadata to store with the
        document.
    """
    doc_id = str(uuid.uuid4())
    collection.add(ids=[doc_id], documents=[text], metadatas=[metadata or {}])


def search(query: str, top_k: int = 3) -> list[str]:
    """
    Search for similar documents based on semantic similarity.

    Converts the query to a vector embedding and searches the ChromaDB collection
    for the most similar documents.

    Args:
        query (str): The search query text.
        top_k (int, optional): Maximum number of similar documents to return.
        Defaults to 3.

    Returns:
        List[str]: List of the most similar document texts, ordered by
        similarity.
    """
    results = collection.query(query_texts=[query], n_results=top_k)
    docs = results['documents']
    return docs[0] if docs else []


def list_documents(limit: int = 50):
    """
    List stored documents and metadata.

    Retrieves documents from the collection with their metadata and provides
    a preview of the document content.

    Args:
        limit (int, optional): Maximum number of documents to return. Defaults
        to 50.

    Returns:
        list[dict]: List of documents with id, metadata, and content preview.
    """
    data = collection.get()
    if not data:
        return []

    ids = (data.get('ids') or [])[:limit]
    docs = (data.get('documents') or [])[:limit]
    metas = (data.get('metadatas') or [])[:limit]
    return [
        {'id': i, 'metadata': m, 'preview': (d[:100] + '...') if len(d) > 100 else d}
        for i, d, m in zip(ids, docs, metas)
    ]


def clear_documents():
    """
    Clear all documents from the vector store.

    Removes all documents and their embeddings from the ChromaDB collection.
    This operation cannot be undone.
    """
    data = collection.get()
    doc_ids = data.get('ids', [])

    # No documents to clear - collection is already empty
    if not doc_ids:
        return

    collection.delete(ids=doc_ids)
