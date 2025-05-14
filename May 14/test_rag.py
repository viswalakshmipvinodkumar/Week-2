"""
Test script for the PDF RAG Chat System

This script demonstrates how to use the PDF RAG Chat System
with a sample PDF document.
"""

from pdf_rag_chat import process_pdf, answer_query, interactive_mode
import os

def main():
    # Path to a sample PDF document
    # Replace this with the path to your actual PDF document
    sample_pdf_path = "sample.pdf"
    
    if not os.path.exists(sample_pdf_path):
        print(f"Sample PDF not found at {sample_pdf_path}")
        print("Please provide a valid PDF path.")
        return
    
    # Process the PDF
    print("Processing PDF...")
    collection_name = process_pdf(sample_pdf_path)
    
    # Ask a sample question
    sample_question = "What is the main topic of this document?"
    print(f"\nSample question: {sample_question}")
    answer = answer_query(sample_question, collection_name)
    
    print("\nAnswer:")
    print("-" * 50)
    print(answer)
    print("-" * 50)
    
    # Run interactive mode
    print("\nStarting interactive mode...")
    interactive_mode(collection_name)

if __name__ == "__main__":
    main()
