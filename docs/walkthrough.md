# Building an AI-Powered Document Assistant: A Walkthrough

In today’s fast-paced business environment, the ability to quickly extract
insights from company documents is invaluable.  Imagine uploading your PDFs or
text files and instantly being able to ask questions about their
content—receiving accurate, AI-generated answers in seconds.  Let's build an
open-source project that would deliver exactly that.

## What does this project do?

This repository is an **AI-powered assistant** that lets you upload documents
(PDF or text), automatically processes and stores their content as vector
embeddings, and enables you to ask questions about the uploaded material.  It
leverages modern NLP and vector search technologies to provide fast, relevant
answers.

Why is this useful?

- **Instant knowledge retrieval**: No more searching through lengthy documents.
- **Scalable**: Handles multiple documents and large text corpora.
- **Customizable**: Easily extend with new models or document types.

## How does it work?

### 1. **Document upload**

Users interact with the assistant via simple HTTP endpoints.  You can upload PDF
or text files using a POST request.  The server extracts and chunks the text
from these files, preparing them for further processing.

### 2. **Embedding & Storage**

Each chunk of text is converted into a vector embedding using
[SentenceTransformers](https://www.sbert.net/).  These embeddings are stored in
a [FAISS](https://faiss.ai/) vector database, enabling efficient similarity
search.

### 3. **Question answering (RAG)**

When you ask a question, the system embeds your query, searches for the most
relevant document chunks using FAISS, and generates an answer based on the
retrieved content.  This is known as **Retrieval-Augmented Generation (RAG)**—a
powerful approach for context-aware AI responses.

## Technologies used

- **Litestar**: Fast, async Python web framework for building APIs.
- **SentenceTransformers**: State-of-the-art text embedding models.
- **FAISS**: High-performance vector similarity search library.
- **NumPy**: Efficient numerical array handling for embeddings.
- **PDF/Text Processing**: Extracts and chunks document content for analysis.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.13+
- [Just](https://just.systems), a command runner

Download an LLM model:

```bash
mkdir ../models
curl -L -o '../models/Phi-3-mini-4k-instruct-q4.gguf' \
    https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf
```

### **1. Clone the repository and start the server**

```bash
git clone https://github.com/codcod/ai-assistant.git
cd ai-assistant
just install
just run
```

### **2. Upload a document**

**PDF Upload:**

```bash
curl -X POST "http://localhost:8000/api/v1/upload/pdf" -F "file=@YourDocument.pdf"
```

**Text File Upload:**

```bash
curl -X POST "http://localhost:8000/api/v1/upload/text" -F "file=@YourNotes.txt"
```

### **3. Ask a question**

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is our remote work policy?"}'
```

### **4. Get your answer**

The assistant retrieves relevant chunks from your uploaded documents, generates
a context-aware answer, and returns it as a JSON object.

**Example response:**

```json
{
  "question": "What is our remote work policy?",
  "answer": "Our remote work policy allows employees to work from home up to three days"
            "per week, subject to manager approval."
}

```

## Final thoughts

This project is a practical demonstration of how modern AI can transform
document management and knowledge retrieval. Whether you’re a developer, data
scientist, or business leader, integrating such an assistant can save time and
unlock new insights from your company’s data.

**Try it out, contribute, and bring AI-powered search to your organization!**

---

Feel free to connect if you have questions or want to collaborate on AI and NLP
projects!
