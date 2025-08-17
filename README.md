# AI Document Assistant

This project is an AI-powered assistant that enables users to upload documents
(PDF or text), automatically processes and stores their content as vector
embeddings, and allows users to ask questions about the uploaded material.

You can upload documents, and then ask questions about their content. The
assistant finds relevant information from your uploads and answers using AI.

How it works:

1. Users upload PDF or text files via HTTP endpoints. The server extracts and
chunks the text from these files.
1. Each text chunk is converted into a vector embedding using a
`SentenceTransformer` model. These embeddings are stored in a ChromaDB vector
database for efficient similarity search.
1. When a user asks a question, the system embeds the query, searches for the
most relevant document chunks using ChromaDB, and generates an answer based on the
retrieved content (using a Retrieval-Augmented Generation approach).

Technologies:

* [Litestar](https://litestar.dev): Web framework for API endpoints.
* [SentenceTransformers](https://www.sbert.net): For generating text embeddings.
* [Chroma](https://www.trychroma.com/): The AI-native database for embeddings.
* [PDF](https://github.com/py-pdf/pypdf): Extracts and chunks document content.
