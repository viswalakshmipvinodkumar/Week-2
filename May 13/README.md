# May 13 Project: Prompt Engineering and Gemini API

This project contains various components related to prompt engineering, text chunking, and the Gemini API.

## Contents

1. **Prompt Engineering Note** (`prompt_engineering_note.txt`)
   - A comprehensive explanation of what prompt engineering is and its importance in AI interactions

2. **Chunking Note** (`chunking_note.txt`)
   - An overview of text chunking in natural language processing and its applications

3. **PDF Chunker** (`pdf_chunker.py`)
   - A utility for extracting text from PDF files and chunking it into manageable segments
   - Supports multiple chunking strategies (by size or by sentences)

4. **Gemini API Demo** (`gemini_api_demo.py`)
   - A demonstration of how to use Google's Gemini API for text generation and chat
   - Includes interactive chat functionality

## Setup and Usage

### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### PDF Chunker

Extract and chunk text from a PDF file:

```bash
python pdf_chunker.py path/to/your/file.pdf --method size --chunk-size 1000 --overlap 100 --output chunks.txt
```

Options:
- `--method`: Chunking method (`size` or `sentences`)
- `--chunk-size`: Maximum size of each chunk in characters (for size method)
- `--overlap`: Number of overlapping characters between chunks (for size method)
- `--max-sentences`: Maximum number of sentences per chunk (for sentences method)
- `--output`: Output file to save chunks (optional)

### Gemini API Demo

To use the Gemini API demo, you'll need an API key from Google's Makersuite:

1. Get your API key from https://makersuite.google.com/app/apikey
2. Create a `.env` file with `GEMINI_API_KEY=your_api_key` or pass it as a command-line argument

Run the demo:

```bash
python gemini_api_demo.py --prompt "Write a poem about artificial intelligence"
```

For interactive chat:

```bash
python gemini_api_demo.py --chat
```

Options:
- `--api-key`: Your Gemini API key (if not using .env file)
- `--model`: Model to use (default: gemini-pro)
- `--prompt`: Prompt for text generation
- `--chat`: Start an interactive chat session
