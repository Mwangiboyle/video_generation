from mistralai import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

#load api key
api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)


responses = client.chat.complete(
    model = "mistral-large-latest", 
    messages=[
        {
            "role": "user",
            "content" :"What is the best cheese for baking?"
        }
    ],

)

print(responses.choices[0].message)