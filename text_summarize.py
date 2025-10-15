# File: gemini_summarizer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def summarize_with_gemini(text_to_summarize):
    """
    Sends text to the Gemini API with a specific prompt to get a summary.

    Args:
        text_to_summarize (str): The long text you want to summarize.

    Returns:
        str: The AI-generated summary.
    """
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        return "Error: GOOGLE_API_KEY not found. Please check your .env file."

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-flash-lite-latest')

        # This is the crucial instruction we give to the AI.
        # We tell it its role and what to do with the text.
        prompt = f"""
        You are an expert summarizer. 
        Please provide a concise, easy-to-read summary of the following text in about 2-3 sentences.

        --- TEXT ---
        {text_to_summarize}
        --- END ---
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    long_text = """
    Uttar Pradesh, located in the northern part of India, is the most populous state in the country and holds
    significant cultural and historical importance. The state is home to numerous holy sites, including the
    city of Varanasi on the banks of the Ganges River, considered one of the oldest continuously inhabited
    cities in the world. Its capital, Lucknow, is renowned for its rich history of arts, cuisine, and courtly
    manners from the Mughal era. Uttar Pradesh's economy is diverse, with agriculture being the primary
    occupation for a majority of the population, while cities like Noida and Ghaziabad have become major hubs
    for the IT and manufacturing industries. The state's vast plains are irrigated by the Ganges and Yamuna
    rivers, making it a crucial contributor to India's food grain production.
    """

    summary = summarize_with_gemini(long_text)

    print("\n--- Original Text ---")
    print(long_text)
    print("\n--- Gemini AI Summary ---")
    print(summary)