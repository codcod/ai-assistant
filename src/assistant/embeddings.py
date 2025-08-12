"""
Vector embeddings module for document similarity search.

This module provides functionality for:
- Adding documents to a vector store using FAISS
- Converting text to embeddings using SentenceTransformers
- Searching for similar documents based on semantic similarity
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.IndexFlatL2(384)  # type: ignore[attr-defined]
documents: list[str] = []


def add_document(text: str) -> None:
    """
    Add a document to the vector store.

    Converts the input text to a vector embedding and stores it in the FAISS index
    along with the original text for retrieval.

    Args:
        text (str): The document text to add to the vector store.
    """
    vector = embedder.encode([text])
    # Ensure vector is 2D array with correct shape for FAISS
    vector = np.array(vector, dtype=np.float32)
    if vector.ndim == 1:
        vector = vector.reshape(1, -1)
    # FAISS add method signature: add(x: np.ndarray) -> None
    index.add(vector)  #  type: ignore pylint: disable=no-value-for-parameter
    documents.append(text)


def search(query: str, top_k: int = 3) -> list[str]:
    """
    Search for similar documents based on semantic similarity.

    Converts the query to a vector embedding and searches the FAISS index
    for the most similar documents.

    Args:
        query (str): The search query text.
        top_k (int, optional): Maximum number of similar documents to return. Defaults to 3.

    Returns:
        List[str]: List of the most similar document texts, ordered by similarity.
    """
    if len(documents) == 0:
        return []

    vector = embedder.encode([query])
    # Ensure vector is 2D array with correct shape for FAISS
    vector = np.array(vector, dtype=np.float32)
    if vector.ndim == 1:
        vector = vector.reshape(1, -1)

    # Limit top_k to available documents
    top_k = min(top_k, len(documents))

    # FAISS search method signature:
    # search(x: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]
    # pylint: disable=no-value-for-parameter
    _, indices = index.search(vector, top_k)  #  type:ignore
    return [documents[i] for i in indices[0] if i < len(documents)]
