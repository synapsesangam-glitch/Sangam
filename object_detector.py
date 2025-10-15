# File: object_detector.py
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont

def detect_objects(image_path, output_path="detected_objects.jpg"):
    """Finds objects in an image and saves a new image with boxes drawn on it."""
    try:
        # Load the pre-trained object detection model
        detector = pipeline("object-detection", model="facebook/detr-resnet-50")
        print(f"Detecting objects in '{image_path}'...")
        
        image = Image.open(image_path)
        results = detector(image)

        # Draw boxes on the image
        draw = ImageDraw.Draw(image)
        for result in results:
            box = result['box']
            label = result['label']
            score = round(result['score'] * 100, 2)
            
            # Define coordinates
            xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']
            
            # Draw rectangle and label
            draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="red", width=3)
            draw.text((xmin, ymin), f"{label} ({score}%)", fill="red")

        # Save the new image
        image.save(output_path)
        print(f"\n--- Object Detection Complete ---")
        print(f"Saved new image with detected objects to '{output_path}'")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # You can use an image of a street, a room, or a park.
    path_to_image = "sample_image.jpg"
    detect_objects(path_to_image)