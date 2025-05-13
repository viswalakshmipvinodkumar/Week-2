"""
Gemini API Demo - Final Version

A simple demonstration of calling the Google Gemini API.
"""

import google.generativeai as genai

# Your API key
API_KEY = "AIzaSyCKSusHxt4fiO_ZGVwYo4fgPkDnQE56ZaA"

def main():
    # Configure the API
    genai.configure(api_key=API_KEY)
    
    print("=" * 50)
    print("GEMINI API DEMONSTRATION")
    print("=" * 50)
    
    # Create the model
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    # Set a very simple prompt
    prompt = "Hello, what can you do?"
    
    print(f"Prompt: {prompt}")
    print("-" * 50)
    
    # Generate the response
    try:
        response = model.generate_content(prompt)
        print("Response:")
        print("-" * 50)
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
