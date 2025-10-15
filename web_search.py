from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) #
def get_groq_model_compound_beta(input_text):
    """
    Generates a response using Groq's compound-beta model (non-streaming).
    Note: This function currently prints the response but returns an empty string.

    Args:
        input_text (str): The input prompt for the model.

    Returns:
        str: An empty string (consider returning the actual response).
    """
    print("\n--- Groq Compound Beta ---")
    try:
        completion = client.chat.completions.create(
            model="compound-beta",
            messages=[
                {
                    "role": "user",
                    "content": input_text
                }
            ],
            # Add other parameters like temperature, max_tokens if needed
        )

        response_content = completion.choices[0].message.content
        tool_calls = completion.choices[0].message.tool_calls

        print("Response Content:", response_content)
        # Print all tool calls if any
        if tool_calls:
            print("Tool Calls:", tool_calls)
        else:
            print("No Tool Calls.")

        # Consider returning the actual content or handling tool calls
        # return response_content
        return response_content 

    except Exception as e:
        print(f"\nError calling Groq API (Compound Beta): {e}")
        return ""

if __name__ == "__main__":
    while True:
        user_input = input("Enter your prompt for Groq Compound Beta: ")
        if user_input.lower() == 'quit':
            print("Exiting...")
            break
        elif user_input:
            response = get_groq_model_compound_beta(user_input)
            print("\n--- Groq Response ---")
            print(response)
        else:
            print("No input provided.")