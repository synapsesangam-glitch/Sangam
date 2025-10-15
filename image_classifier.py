# File: gemini_vision.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

def analyze_image(image_path, prompt):
    """
    Sends an image and a text prompt to the Gemini Pro Vision model.
    
    Args:
        image_path (str): The path to the image file.
        prompt (str): The question you want to ask about the image.
        
    Returns:
        str: The AI's text response.
    """
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        return "Error: GOOGLE_API_KEY not found in .env file."
    
    try:
        # Configure the API key and load the vision model
        genai.configure(api_key=API_KEY)
        vision_model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("Analyzing image with Gemini Vision...")
        
        # Open the image file
        img = Image.open(image_path)
        
        # Send the image and prompt to the model
        response = vision_model.generate_content([prompt, img])
        
        return response.text

    except FileNotFoundError:
        return f"Error: The file '{image_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # You can change the image path and the prompt to ask different questions!
    path_to_image = "sample_image.jpg"
    
    # --- Example Prompts ---
    # To classify the image: "What is the main subject of this image? Respond with one or two words."
    # To describe the image: "Describe this image in detail."
    # To ask a specific question: "Are there any buildings in this picture?"
    
    user_prompt = "What is in this image? Describe it in one sentence."
    
    ai_response = analyze_image(path_to_image, user_prompt)
    
    print("\n--- Gemini Vision Response ---")
    print(ai_response)
    print("----------------------------")