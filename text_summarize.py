# File: text_summarizer.py
from transformers import pipeline

def summarize_text(text_to_summarize):
    """Summarizes a long piece of text using a pre-trained model."""
    try:
        print("Loading summarization model...")
        # Load the pre-trained summarization model
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        
        print("Generating summary...")
        # Generate the summary
        summary = summarizer(text_to_summarize, max_length=50, min_length=25, do_sample=False)
        
        print("\n--- Summary ---")
        print(summary[0]['summary_text'])
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Students can replace this text with any article or paragraph.
    long_text = """
    Artificial intelligence (AI) is rapidly changing the world, from how we interact with technology 
    to how businesses operate. In the field of agriculture, AI is used to monitor crop health and predict 
    yields, helping farmers make better decisions. For urban communities, AI can optimize traffic flow 
    and improve public services. In education, it offers personalized learning experiences for students. 
    By processing vast amounts of data, AI models can identify patterns and provide insights that were 
    previously impossible for humans to find, opening up new possibilities for innovation and progress.
    """
    summarize_text(long_text)