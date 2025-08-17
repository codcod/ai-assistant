"""
Persistent storage module for vector embeddings and document data.

This module provides functionality for:
- Configuring ChromaDB persistent client
- Managing the document collection
- Setting up embedding functions
"""

import typing as tp

import chromadb
from chromadb.utils import embedding_functions

# Initialize persistent Chroma client
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-MiniLM-L6-v2'
)
chroma_client = chromadb.PersistentClient(path='.instance/chroma_store')


def get_collection() -> chromadb.Collection:
    """Get or create the persistent document collection."""
    return chroma_client.get_or_create_collection(
        name='docs', embedding_function=tp.cast(chromadb.EmbeddingFunction, embed_fn)
    )
