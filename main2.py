import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


image_url = "https://imgur.com/a/xi6RoUW"



response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "Extract the text in this image and return texts" },
                {
                    "type": "input_image",
                    "image_url": image_url,
                },
            ],
        }
    ],
)

print(response.output_text)