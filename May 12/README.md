# Week 2 Assignment: PDF Text Extraction and ChromaDB

This project demonstrates PDF text extraction using PyMuPDF and vector database operations using ChromaDB.

## Project Structure

- `pdf_extractor.py`: Contains the function to extract text from PDF files using PyMuPDF
- `chroma_db.py`: Implementation of ChromaDB for vector storage and retrieval
- `create_sample_pdf.py`: Utility to create a sample PDF for testing
- `main.py`: Main script that demonstrates all functionality together
- `vector_database_note.txt`: Detailed note on vector databases
- `agentic_rag_note.txt`: Detailed note on Agentic RAG
- `requirements.txt`: List of required Python packages

## Setup and Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the main script:
   ```
   python main.py
   ```

## Features

1. **PDF Text Extraction**: Extract all text content from PDF files using PyMuPDF
2. **Vector Database Operations**: Store and query document embeddings using ChromaDB
3. **Sample PDF Creation**: Generate a sample PDF for testing purposes

## Notes

The project includes detailed notes on:
- Vector databases: What they are and how they work
- Agentic RAG (Retrieval Augmented Generation): An advanced approach to combining retrieval systems with generative AI

## Output Files

When running the main script, the following output files will be generated:
- `sample.pdf`: A sample PDF file with test content
- `extracted_text.txt`: The extracted text from the sample PDF
- `chroma_db/`: Directory containing the ChromaDB database files
