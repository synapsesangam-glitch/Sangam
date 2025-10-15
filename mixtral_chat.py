# File: mixtral_chat.py

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Mixtral API key and URL from .env file
API_KEY = os.getenv("MIXTRAL_API_KEY")
API_URL = os.getenv("MIXTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")

def get_mixtral_response(prompt):
    """Sends a prompt to the Mixtral AI and returns the response."""
    if not API_KEY:
        return "Error: MIXTRAL_API_KEY not found in .env file."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content'].strip()
        else:
            return f"Error: API returned status code {response.status_code}. Response: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("--- Mixtral AI Chat Interface ---")
    print("Type 'quit' to exit.")
    while True:
        user_prompt = input("\nYou: ")
        if user_prompt.lower() == 'quit':
            break
        ai_response = get_mixtral_response(user_prompt)
        print(f"Mixtral AI: {ai_response}")