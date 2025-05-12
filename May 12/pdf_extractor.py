import fitz  # PyMuPDF

def extract_pdf_text(filepath):
    """
    Extract all text from a PDF file using PyMuPDF.
    
    Args:
        filepath (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Open the PDF file
        doc = fitz.open(filepath)
        
        # Initialize an empty string to store the text
        text = ""
        
        # Iterate through each page and extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        # Close the document
        doc.close()
        
        return text
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Example usage
if __name__ == "__main__":
    # Replace with the path to your PDF file
    sample_pdf_path = "sample.pdf"
    try:
        extracted_text = extract_pdf_text(sample_pdf_path)
        print(f"Extracted {len(extracted_text)} characters of text")
        print("Sample of extracted text:")
        print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
        # Save the extracted text to a file
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print("Extracted text saved to 'extracted_text.txt'")
    except Exception as e:
        print(f"Error in example usage: {e}")
