import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

#load openai api keys 
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Function to create a file with the Files API
def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

# Getting the file ID
file_id = create_file("data/WhatsApp Image 2025-06-04 at 6.22.48 PM.jpeg")



response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "Extract the text in this image and return texts" },
                {
                    "type": "input_image",
                    "file_id": file_id,
                },
            ],
        }
    ],
)

print(response.output_text)
