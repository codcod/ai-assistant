"""
Persistent storage module for vector embeddings and document data.

This module provides functionality for:
- Saving FAISS index and document data to disk
- Loading previously saved vector store data
- Managing persistent storage paths
"""

import pickle

import faiss

from .embeddings import documents, index

STORE_PATH = '.instance/vector_store.pkl'
INDEX_PATH = '.instance/index.faiss'


def save_store() -> None:
    """
    Save the current vector index and documents to disk.

    Persists the FAISS index and document list to separate files
    for later retrieval.
    """
    faiss.write_index(index, INDEX_PATH)  # type: ignore[attr-defined]
    with open(STORE_PATH, 'wb') as f:
        pickle.dump(documents, f)


def load_store() -> None:
    """
    Load previously saved vector index and documents from disk.

    Restores the FAISS index and document list from saved files
    if they exist.
    """
    import os

    if os.path.exists(INDEX_PATH) and os.path.exists(STORE_PATH):
        global index, documents  # pylint: disable=global-variable-not-assigned
        index = faiss.read_index(INDEX_PATH)  # type: ignore[attr-defined]
        with open(STORE_PATH, 'rb') as f:
            documents[:] = pickle.load(f)
