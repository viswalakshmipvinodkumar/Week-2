"""
PDF Text Chunking Utility

This module provides functions to extract text from PDF files and chunk it
into smaller, manageable segments for further processing.
"""

import os
import PyPDF2
from typing import List, Dict, Union, Optional


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


def chunk_text_by_size(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Chunk text by character count with optional overlap between chunks.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk in characters
        overlap: Number of overlapping characters between chunks
        
    Returns:
        List of text chunks
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")
    
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        # Calculate end position for this chunk
        end = min(start + chunk_size, text_length)
        
        # If we're not at the end of the text, try to find a good breaking point
        if end < text_length:
            # Look for a space, newline, or punctuation to break at
            for i in range(end, max(start, end - 50), -1):
                if text[i] in " \n.!?;":
                    end = i + 1
                    break
        
        # Add this chunk to our list
        chunks.append(text[start:end])
        
        # Calculate the start of the next chunk, considering overlap
        start = end - overlap
    
    return chunks


def chunk_text_by_sentences(text: str, max_sentences: int = 5, 
                           max_chunk_size: Optional[int] = None) -> List[str]:
    """
    Chunk text by grouping sentences together.
    
    Args:
        text: The text to chunk
        max_sentences: Maximum number of sentences per chunk
        max_chunk_size: Optional maximum size of each chunk in characters
        
    Returns:
        List of text chunks
    """
    # Simple sentence splitting - can be improved with NLP libraries
    sentences = []
    for potential_sentence in text.replace('\n', ' ').split('. '):
        if potential_sentence:
            sentences.append(potential_sentence.strip() + '.')
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_size = len(sentence)
        
        # Check if adding this sentence would exceed our limits
        if (len(current_chunk) >= max_sentences or 
            (max_chunk_size and current_size + sentence_size > max_chunk_size)) and current_chunk:
            # Save current chunk and start a new one
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 0
        
        # Add sentence to current chunk
        current_chunk.append(sentence)
        current_size += sentence_size
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def chunk_pdf(pdf_path: str, method: str = 'size', **kwargs) -> Dict[str, Union[List[str], str]]:
    """
    Extract text from a PDF and chunk it using the specified method.
    
    Args:
        pdf_path: Path to the PDF file
        method: Chunking method ('size' or 'sentences')
        **kwargs: Additional parameters for the chunking method
        
    Returns:
        Dictionary containing the original text and the chunks
    """
    text = extract_text_from_pdf(pdf_path)
    
    if method == 'size':
        chunk_size = kwargs.get('chunk_size', 1000)
        overlap = kwargs.get('overlap', 100)
        chunks = chunk_text_by_size(text, chunk_size, overlap)
    elif method == 'sentences':
        max_sentences = kwargs.get('max_sentences', 5)
        max_chunk_size = kwargs.get('max_chunk_size', None)
        chunks = chunk_text_by_sentences(text, max_sentences, max_chunk_size)
    else:
        raise ValueError(f"Unknown chunking method: {method}")
    
    return {
        'original_text': text,
        'chunks': chunks,
        'num_chunks': len(chunks),
        'method': method
    }


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Chunk text from a PDF file')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--method', choices=['size', 'sentences'], default='size',
                        help='Chunking method to use')
    parser.add_argument('--chunk-size', type=int, default=1000,
                        help='Maximum size of each chunk in characters (for size method)')
    parser.add_argument('--overlap', type=int, default=100,
                        help='Number of overlapping characters between chunks (for size method)')
    parser.add_argument('--max-sentences', type=int, default=5,
                        help='Maximum number of sentences per chunk (for sentences method)')
    parser.add_argument('--output', help='Output file to save chunks (optional)')
    
    args = parser.parse_args()
    
    try:
        result = chunk_pdf(
            args.pdf_path,
            method=args.method,
            chunk_size=args.chunk_size,
            overlap=args.overlap,
            max_sentences=args.max_sentences
        )
        
        print(f"Successfully extracted and chunked text from {args.pdf_path}")
        print(f"Chunking method: {args.method}")
        print(f"Number of chunks: {result['num_chunks']}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                for i, chunk in enumerate(result['chunks']):
                    f.write(f"--- Chunk {i+1} ---\n{chunk}\n\n")
            print(f"Chunks saved to {args.output}")
        else:
            for i, chunk in enumerate(result['chunks']):
                print(f"\n--- Chunk {i+1} ---\n{chunk[:100]}...")
    
    except Exception as e:
        print(f"Error: {str(e)}")
