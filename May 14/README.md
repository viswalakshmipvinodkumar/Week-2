# PDF RAG Chat System

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to chat with PDF documents. The system extracts text from PDFs, chunks it into manageable segments, stores these chunks in ChromaDB, and uses Google's Gemini API to generate answers to user queries based on the relevant retrieved content.

## Features

- PDF text extraction
- Text chunking using LangChain's RecursiveCharacterTextSplitter
- Vector storage using ChromaDB
- Semantic search for relevant content retrieval
- Answer generation using Google Gemini API
- Interactive chat mode

## Requirements

- Python 3.8+
- PyPDF2
- ChromaDB
- Google Generative AI Python SDK
- LangChain
- python-dotenv

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Process a PDF document

```bash
python pdf_rag_chat.py --pdf path/to/your/document.pdf
```

This will extract text from the PDF, chunk it, and store it in ChromaDB.

### Ask a single question

```bash
python pdf_rag_chat.py --query "Your question about the document" --collection_name "collection_name"
```

### Interactive mode

```bash
python pdf_rag_chat.py --interactive --collection_name "collection_name"
```

This allows you to ask multiple questions in an interactive session.

## How It Works

1. **PDF Processing**:
   - Text is extracted from the PDF using PyPDF2
   - The text is split into chunks using LangChain's RecursiveCharacterTextSplitter

2. **Storage**:
   - Text chunks are stored in ChromaDB with embeddings

3. **Query Processing**:
   - User query is embedded and used to search for relevant chunks in ChromaDB
   - Top matching chunks are retrieved

4. **Answer Generation**:
   - Retrieved chunks are used as context for the Gemini API
   - Gemini generates an answer based on the provided context and query

## Example

```bash
# Process a PDF
python pdf_rag_chat.py --pdf research_paper.pdf

# Ask a question
python pdf_rag_chat.py --query "What are the main findings of the research?" --collection_name "research_paper"

# Interactive mode
python pdf_rag_chat.py --interactive --collection_name "research_paper"
```
