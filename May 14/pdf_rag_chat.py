"""
PDF RAG Chat System

This script implements a Retrieval-Augmented Generation (RAG) system that:
1. Extracts text from PDF documents
2. Chunks the text into manageable segments
3. Stores the chunks in ChromaDB
4. Retrieves relevant chunks based on user queries
5. Uses Gemini API to generate answers based on the retrieved context

Usage:
    python pdf_rag_chat.py --pdf path/to/document.pdf
    python pdf_rag_chat.py --query "Your question about the document" --collection_name "collection_name"
"""

import os
import sys
import argparse
from typing import List, Dict, Any, Optional
import PyPDF2
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize ChromaDB client
client = chromadb.PersistentClient("./chroma_db")

# Create embedding function for ChromaDB
embedding_function = embedding_functions.DefaultEmbeddingFunction()

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    return text

def chunk_text(text: str) -> List[str]:
    """
    Chunk text using LangChain's RecursiveCharacterTextSplitter.
    
    Args:
        text: The text to chunk
        
    Returns:
        List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text)
    return chunks

def store_chunks_in_chroma(chunks: List[str], collection_name: str) -> None:
    """
    Store text chunks in ChromaDB.
    
    Args:
        chunks: List of text chunks to store
        collection_name: Name of the collection to store chunks in
    """
    # Create or get the collection
    try:
        # Delete collection if it exists
        try:
            client.delete_collection(collection_name)
            print(f"Deleted existing collection: {collection_name}")
        except:
            pass
            
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
        
        # Add documents to the collection
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({"source": "pdf", "chunk_id": i})
            ids.append(f"chunk_{i}")
        
        # Add documents in batches if there are many
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Successfully stored {len(chunks)} chunks in ChromaDB collection '{collection_name}'")
    
    except Exception as e:
        print(f"Error storing chunks in ChromaDB: {str(e)}")
        raise

def retrieve_relevant_chunks(query: str, collection_name: str, n_results: int = 5) -> List[str]:
    """
    Retrieve relevant chunks from ChromaDB based on a query.
    
    Args:
        query: User query
        collection_name: Name of the collection to search in
        n_results: Number of results to retrieve
        
    Returns:
        List of relevant text chunks
    """
    try:
        # Get the collection
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
        
        # Query the collection
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Extract and return the documents
        if results and 'documents' in results and results['documents']:
            return results['documents'][0]
        else:
            return []
    
    except Exception as e:
        print(f"Error retrieving chunks from ChromaDB: {str(e)}")
        return []

def generate_answer(query: str, context: List[str]) -> str:
    """
    Generate an answer to a query using Gemini API with context from retrieved chunks.
    
    Args:
        query: User query
        context: List of relevant text chunks to use as context
        
    Returns:
        Generated answer as a string
    """
    try:
        # Create the model
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        
        # Combine context chunks
        context_text = "\n\n".join(context)
        
        # Create a prompt with the context and query
        prompt = f"""
        Based on the following information, please answer the question.
        If the answer is not contained in the provided information, say "I don't have enough information to answer this question."
        
        CONTEXT:
        {context_text}
        
        QUESTION:
        {query}
        
        ANSWER:
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        print(f"Error generating answer with Gemini API: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def process_pdf(pdf_path: str, collection_name: Optional[str] = None) -> str:
    """
    Process a PDF file: extract text, chunk it, and store in ChromaDB.
    
    Args:
        pdf_path: Path to the PDF file
        collection_name: Optional name for the ChromaDB collection
        
    Returns:
        Name of the collection where chunks are stored
    """
    # Extract filename without extension to use as collection name if not provided
    if collection_name is None:
        collection_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Using collection name: {collection_name}")
    
    # Extract text from PDF
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters of text")
    
    # Chunk the text
    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    # Store chunks in ChromaDB
    print("Storing chunks in ChromaDB...")
    store_chunks_in_chroma(chunks, collection_name)
    
    return collection_name

def answer_query(query: str, collection_name: str) -> str:
    """
    Answer a query using the RAG system.
    
    Args:
        query: User query
        collection_name: Name of the ChromaDB collection to search in
        
    Returns:
        Generated answer as a string
    """
    print(f"Query: {query}")
    print(f"Searching in collection: {collection_name}")
    
    # Retrieve relevant chunks
    print("Retrieving relevant chunks...")
    chunks = retrieve_relevant_chunks(query, collection_name)
    
    if not chunks:
        return "No relevant information found to answer your question."
    
    print(f"Retrieved {len(chunks)} relevant chunks")
    
    # Generate answer
    print("Generating answer...")
    answer = generate_answer(query, chunks)
    
    return answer

def interactive_mode(collection_name: str) -> None:
    """
    Run the RAG system in interactive mode, allowing the user to ask multiple questions.
    
    Args:
        collection_name: Name of the ChromaDB collection to search in
    """
    print(f"Interactive mode started. Using collection: {collection_name}")
    print("Type 'exit', 'quit', or 'q' to exit.")
    
    while True:
        query = input("\nEnter your question: ")
        
        if query.lower() in ["exit", "quit", "q"]:
            print("Exiting interactive mode.")
            break
        
        answer = answer_query(query, collection_name)
        print("\nAnswer:")
        print("-" * 50)
        print(answer)
        print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="PDF RAG Chat System")
    parser.add_argument("--pdf", help="Path to the PDF file to process")
    parser.add_argument("--query", help="Query to answer")
    parser.add_argument("--collection_name", help="Name of the ChromaDB collection to use")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Process PDF if provided
    if args.pdf:
        collection_name = process_pdf(args.pdf, args.collection_name)
    elif args.collection_name:
        collection_name = args.collection_name
    else:
        print("Error: Either --pdf or --collection_name must be provided")
        parser.print_help()
        sys.exit(1)
    
    # Answer query or run in interactive mode
    if args.interactive:
        interactive_mode(collection_name)
    elif args.query:
        answer = answer_query(args.query, collection_name)
        print("\nAnswer:")
        print("-" * 50)
        print(answer)
        print("-" * 50)
    elif args.pdf:
        print(f"\nPDF processed successfully. To ask questions, run:")
        print(f"python {sys.argv[0]} --query 'Your question' --collection_name '{collection_name}'")
        print(f"Or for interactive mode:")
        print(f"python {sys.argv[0]} --interactive --collection_name '{collection_name}'")

if __name__ == "__main__":
    main()
