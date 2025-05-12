from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf(output_path="sample.pdf"):
    """
    Create a sample PDF file with some text content.
    
    Args:
        output_path (str): Path where the PDF will be saved
    """
    # Create a canvas with letter size
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Set font and size
    c.setFont("Helvetica", 12)
    
    # Add a title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Sample PDF Document")
    
    # Add some paragraphs
    c.setFont("Helvetica", 12)
    
    paragraphs = [
        "This is a sample PDF document created for testing the PDF text extraction function.",
        "",
        "Vector databases are specialized database systems designed to store and efficiently query high-dimensional vector embeddings.",
        "These embeddings are numerical representations of data that capture semantic meaning.",
        "",
        "Retrieval Augmented Generation (RAG) combines retrieval systems with generative AI to enhance the quality and accuracy of generated content.",
        "",
        "Agentic RAG takes this further by incorporating autonomous decision-making capabilities into the retrieval and generation process.",
        "This allows the system to independently determine what information to retrieve and how to use it effectively."
    ]
    
    y_position = height - 100
    for paragraph in paragraphs:
        c.drawString(72, y_position, paragraph)
        y_position -= 20
    
    # Add a second page
    c.showPage()
    
    # Add content to the second page
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 72, "Additional Information")
    
    c.setFont("Helvetica", 12)
    more_paragraphs = [
        "This is the second page of our sample PDF document.",
        "",
        "ChromaDB is an open-source embedding database that makes it easy to build AI applications with embeddings.",
        "",
        "PyMuPDF (fitz) is a Python binding for MuPDF, which is a lightweight PDF renderer.",
        "It's useful for extracting text, images, and other content from PDF documents.",
        "",
        "This sample PDF was created using ReportLab, a library for generating PDFs with Python."
    ]
    
    y_position = height - 100
    for paragraph in more_paragraphs:
        c.drawString(72, y_position, paragraph)
        y_position -= 20
    
    # Save the PDF
    c.save()
    print(f"Sample PDF created at {output_path}")

if __name__ == "__main__":
    create_sample_pdf()
