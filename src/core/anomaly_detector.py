import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv() # Load environment variables

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini Vision model
# 'gemini-1.5-flash' is suitable for multimodal inputs (text + image)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

def detect_visual_anomaly(image_bytes, anomaly_prompt_text="Describe any defects, irregularities, or anomalies you observe in this image. Assume it's a product or item that should look uniform or perfect. If it looks normal, state that."):
    """
    Analyzes an image using Google Gemini Vision API to detect anomalies
    based on the provided prompt.

    Args:
        image_bytes (bytes): The byte content of the image.
        anomaly_prompt_text (str): The text prompt/question for Gemini,
                                   guiding it to look for anomalies.

    Returns:
        str: The AI's analysis regarding anomalies.
    """
    if not image_bytes:
        return "No image provided for analysis."

    # Open image using Pillow from bytes
    image = Image.open(io.BytesIO(image_bytes))

    # Construct the content for Gemini.
    content_parts = [
        anomaly_prompt_text,
        image
    ]

    try:
        response = vision_model.generate_content(content_parts)
        # Check if response.text is empty or contains specific error indicators
        if not response.text.strip():
            return "AI did not provide a specific anomaly detection result. The image might be too complex, or the prompt too vague."
        return response.text
    except Exception as e:
        # More specific error handling could be added based on Gemini API errors
        return f"An error occurred during anomaly detection: {e}. Please ensure your API key is correct and the image content is appropriate."

# Example Usage (for testing - remove or comment out for deployment)
if __name__ == "__main__":
    print("This module is designed to be imported by app.py for Streamlit functionality.")
    print("To test locally, you'd typically run the app.py file.")
    # Example of how you might test it if you had a local image file:
    # try:
    #     with open("path/to/your/image_with_defect.jpg", "rb") as f:
    #         test_image_bytes = f.read()
    #     result = detect_visual_anomaly(test_image_bytes, "Does this product have any defects? Describe them.")
    #     print(result)
    # except FileNotFoundError:
    #     print("Test image not found. Please provide a path to a test image.")
    # except Exception as e:
    #     print(f"Error during test: {e}")