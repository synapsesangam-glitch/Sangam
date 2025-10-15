# File: gemini_chat.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Google API Key from .env file
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_gemini_response(prompt):
    """Sends a prompt to the Gemini AI and returns the response."""
    if not API_KEY:
        return "Error: GOOGLE_API_KEY not found in .env file."
    
    try:
        # Configure the API key
        genai.configure(api_key=API_KEY)
        
        # Create the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Get the response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("--- Gemini AI Chat Interface ---")
    print("Type 'quit' to exit.")
    while True:
        user_prompt = input("\nYou: ")
        if user_prompt.lower() == 'quit':
            break
        ai_response = get_gemini_response(user_prompt)
        print(f"Gemini AI: {ai_response}")