# File: image_classifier.py
from transformers import pipeline
from PIL import Image

def classify_image(image_path):
    """Identifies the contents of an image using a pre-trained model."""
    try:
        # Load the pre-trained image classification model
        classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
        print(f"Analyzing '{image_path}'...")
        # Open the image
        image = Image.open(image_path)
        # Get the results
        results = classifier(image)
        print("\n--- Image Analysis Results ---")
        for result in results:
            label = result['label']
            score = round(result['score'] * 100, 2)
            print(f"- Found: {label} (Confidence: {score}%)")
        return results[0]['label'] # Return the top result
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # You can change this to any image file you have.
    # Try images of plants, animals, or local landmarks!
    path_to_image = "sample_image.jpg" 
    classify_image(path_to_image)