import os
from pdf_extractor import extract_pdf_text
from chroma_db import ChromaDBManager
from create_sample_pdf import create_sample_pdf

def main():
    """
    Main function to demonstrate PDF text extraction and ChromaDB functionality.
    """
    print("=" * 50)
    print("Week 2 Assignment - PDF Text Extraction and ChromaDB")
    print("=" * 50)
    
    # Step 1: Create a sample PDF
    print("\nStep 1: Creating a sample PDF...")
    sample_pdf_path = "sample.pdf"
    create_sample_pdf(sample_pdf_path)
    
    # Step 2: Extract text from the PDF
    print("\nStep 2: Extracting text from the PDF...")
    extracted_text = extract_pdf_text(sample_pdf_path)
    
    # Save the extracted text to a file
    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    print(f"Extracted {len(extracted_text)} characters of text")
    print("Sample of extracted text:")
    print(extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text)
    print("Full extracted text saved to 'extracted_text.txt'")
    
    # Step 3: Initialize ChromaDB and store the extracted text
    print("\nStep 3: Initializing ChromaDB and storing the document...")
    
    # Split the text into chunks (simple paragraph-based splitting for demonstration)
    chunks = [chunk.strip() for chunk in extracted_text.split("\n\n") if chunk.strip()]
    
    # Initialize ChromaDB
    db_manager = ChromaDBManager(collection_name="pdf_documents")
    
    # Add the chunks to ChromaDB
    db_manager.add_documents(
        documents=chunks,
        ids=[f"pdf_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": "sample.pdf", "chunk_id": i} for i in range(len(chunks))]
    )
    
    # Step 4: Query the ChromaDB collection
    print("\nStep 4: Querying the ChromaDB collection...")
    query = "What is Agentic RAG?"
    results = db_manager.query_collection(query, n_results=2)
    
    print(f"Query: {query}")
    if results:
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            print(f"\nResult {i+1}:")
            print(f"Document: {doc}")
            print(f"Metadata: {metadata}")
            print(f"Distance: {distance}")
    
    print("\nAssignment completed successfully!")

if __name__ == "__main__":
    main()
