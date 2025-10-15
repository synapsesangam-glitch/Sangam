# File: information_finder.py
import wikipediaapi

def get_web_information(topic):
    """
    Searches Wikipedia for a given topic and returns a summary.

    Args:
        topic (str): The topic you want to search for (e.g., "Kanpur", "black hole").

    Returns:
        str: A summary of the topic or an error message.
    """
    try:
        # Create a Wikipedia API object. It's good practice to set a custom user agent.
        # Replace 'MyAppName' and the email with your app's name and your contact info.
        wiki_api = wikipediaapi.Wikipedia(
            user_agent='SangamSynapseProject (user@example.com)',
            language='en'
        )

        # Get the Wikipedia page for the given topic
        page = wiki_api.page(topic)

        if page.exists():
            # The .summary contains the whole summary. We split it by newline
            # and take the first paragraph to keep it short and clean.
            first_paragraph = page.summary.split('\n')[0]
            return first_paragraph
        else:
            return f"Sorry, I could not find a Wikipedia page for '{topic}'."

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Ask the user what they want to search for
    search_topic = input("What information are you looking for? > ")
    
    if search_topic:
        print(f"\nSearching for '{search_topic}'...")
        information = get_web_information(search_topic)
        print("\n--- Information Found ---")
        print(information)
    else:
        print("No topic entered.")