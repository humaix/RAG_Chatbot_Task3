# RAG Document Chatbot

A conversational AI chatbot that uses Retrieval-Augmented Generation (RAG)
to answer questions from user-provided documents.

The system supports multiple document formats, semantic retrieval,
conversation history, source tracking, and document upload through a Flask
web interface.

---

## Features

- Retrieval-Augmented Generation (RAG)
- Conversational question answering
- PDF, DOCX, TXT, and Excel XLSX support
- HuggingFace sentence-transformer embeddings
- ChromaDB vector database
- Semantic retrieval with MMR (Maximal Marginal Relevance)
- Context-aware prompt engineering
- Conversation memory (rolling window)
- Source tracking with row-level metadata for Excel files
- Semantic query routing (general vs. document queries)
- Casual conversation fallback (no unnecessary retrieval)
- Flask web interface with dark-themed chat UI
- Document upload and automatic indexing
- Duplicate upload protection
- Clear conversation history
- Logging and error handling

---

## Technologies

- Python
- LangChain
- ChromaDB
- HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
- Groq API (`openai/gpt-oss-120b`)
- Flask
- Pandas
- PyPDF
- python-docx / docx2txt
- OpenPyXL
- NumPy

---

## Architecture

### Query Flow

```text
                    User
                      |
                      v
                Flask Web App
                      |
                      v
                 Query Router
                 /         \
                /           \
        General Query    Document Query
             |                |
             v                v
       Direct Response     Retriever (MMR)
                              |
                              v
                          ChromaDB
                              |
                              v
                       Relevant Chunks
                              |
                              v
                    Prompt + Chat History
                              |
                              v
                        LLM (Groq API)
                              |
                              v
                       Answer + Sources
```

### Document Ingestion

```text
PDF / DOCX / TXT / XLSX
          |
          v
   Document Loader
          |
          v
      Chunking
          |
          v
    Embeddings
          |
          v
      ChromaDB
```

Excel files are converted into individual document records so that
specific rows (e.g., individual employee records) can be retrieved
independently.

---

## Project Structure

```text
Rag_chatbot/
|
├── app/
│   ├── brain/
│   │   ├── embedding.py        # HuggingFace embedding manager
│   │   ├── llm.py              # LLM wrapper (Groq API)
│   │   ├── prompt.py           # Prompt template
│   │   ├── query_router.py     # Semantic query router
│   │   ├── retriever.py        # MMR-based retriever
│   │   └── vector_store.py     # ChromaDB vector store
│   │
│   ├── chat/
│   │   └── conversation.py     # Conversation memory
│   │
│   ├── core/
│   │   ├── config.py           # YAML config reader
│   │   └── logger.py           # File + console logger
│   │
│   ├── knowledge_base/
│   │   ├── chunker.py          # Text splitter
│   │   └── loaders.py          # Multi-format document loaders
│   │
│   └── web/
│       ├── routes.py           # Flask routes (chat, upload, clear)
│       └── templates/
│           └── index.html      # Chat interface
│
├── data/
│   └── documents/              # Place documents here
│
├── storage/
│   ├── chroma/                 # ChromaDB persistence (gitignored)
│   └── logs/                   # Application logs (gitignored)
│
├── tests/
│   ├── test_loader.py          # Document loader test
│   └── test_query_router.py    # Query router test
│
├── docs/                       # Technical documentation
│   ├── Technical_Report.pdf
│   ├── Technical_Report.md
│   └── diagrams/
│
├── .env                        # API keys (gitignored)
├── .gitignore
├── config.yaml                 # Project configuration
├── ingest.py                   # Batch document ingestion
├── main.py                     # Terminal-based chatbot
├── requirements.txt            # Python dependencies
├── run.py                      # Flask web application
└── README.md
```

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit the `.env` file to GitHub.

---

## Usage

### Add Documents

Place supported documents inside:

```
data/documents/
```

Supported formats: **PDF**, **DOCX**, **TXT**, **XLSX**

### Build the Knowledge Base

```bash
python ingest.py
```

This loads the documents, creates chunks, generates embeddings,
and stores the vectors in ChromaDB.

### Run the Web Application

```bash
python run.py
```

Then open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Document Upload

Documents can also be uploaded directly from the web interface.

Uploaded documents are:

1. Saved to the document directory.
2. Loaded using the document loader.
3. Split into chunks.
4. Embedded using HuggingFace embeddings.
5. Added to ChromaDB.

Supported uploads: **PDF**, **DOCX**, **TXT**, **XLSX**

Duplicate filenames are rejected to prevent accidental duplicate indexing.

---

## Conversational Question Answering

The chatbot maintains conversation history for follow-up questions.

**Example:**

> **User:** How many leave days does Sara receive?
>
> **Bot:** Sara receives 22 leave days.
>
> **User:** Who is she?
>
> **Bot:** Sara is an employee in the Finance department.

---

## Query Routing

A lightweight semantic query router runs before document retrieval.

Casual or general questions such as:

- "Hello"
- "How are you?"
- "Which model are you?"

are handled without unnecessary document retrieval.

Document-related questions are sent through the full RAG pipeline.

---

## Source Tracking

For document-based answers, the chatbot displays the sources used
during retrieval.

**Example:**

> **Answer:** Sara receives 22 leave days.
>
> **Sources:**
> - sample.xlsx (Row 3)
> - sample.docx

---

## Example Questions

- Who is Sara?
- How many leave days does Sara receive?
- Which department does Ali work in?
- Who is Ahmed?
- What is the company leave policy?
- What is this paper about?

---

## Testing

Run the test suite:

```bash
python -m pytest
```

The project includes tests for document loading and query routing.

---

## Error Handling

The application handles common situations:

- Empty questions
- Unsupported file formats
- Invalid or empty document uploads
- Duplicate file uploads
- LLM API failures
- Retrieval failures

---

## Security

- API keys are stored in `.env` and excluded from Git.
- Private documents should not be committed to the repository.
- ChromaDB storage is excluded from version control.

---

## Future Improvements

- Document deletion from the UI
- Streaming responses
- User authentication
- Persistent conversation sessions
- Better source ranking
- Retrieval evaluation
- Reranking models
- Production deployment

---

## Author

Developed as an internship project focused on Retrieval-Augmented Generation,
LangChain, LLMs, ChromaDB, and conversational document question answering.