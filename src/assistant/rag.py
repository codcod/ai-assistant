"""
Retrieval-Augmented Generation (RAG) module for question answering.

This module provides functionality for:
- Retrieving relevant document chunks based on queries
- Generating context-aware answers using LLM
- Combining vector search with text generation

The logic is unchanged compared to before, just uses Chroma search.
"""

from .embeddings import search
from .llm import generate


def rag_answer(query: str) -> str:
    """
    Generate an answer to a query using retrieval-augmented generation.

    Retrieves relevant document chunks and uses them as context
    for generating an informed answer using the language model.

    Args:
        query (str): The question or query to answer.

    Returns:
        str: Generated answer based on retrieved document context.
    """
    context_chunks = search(query)
    context_text = '\n'.join(context_chunks)

    prompt = f"""
You are a helpful assistant. Use the provided context to answer the question.

Context:
{context_text}

Question: {query}
Answer:
"""
    return generate(prompt)
