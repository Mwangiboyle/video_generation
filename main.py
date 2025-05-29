from mistralai import Mistral
from dotenv import load_dotenv
import json
import os

load_dotenv()

#load api key
api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

title = input("Enter your idea here: ")

prompt = f'''You are a video scriptwriter for short educational YouTube videos.

Your job is to generate a concise and clear script for a short video based on the following :

eg. How to make money as a developer

Break the topic down into 5 to 7 actionable, logical steps. Each step should be written like a scene in a video: what the narrator would say and what the viewer would see.

Each step should be:
- Simple and clear (aimed at beginners)
- One sentence describing the narration
- One sentence describing the visual content
- Include 1–2 relevant keywords for stock footage

Format your output as a JSON array of steps like this:


  
   "narration": "Start by choosing a programming language to master.",
    "visual": "Show a developer browsing programming languages.",
    "keywords": ["programming", "developer"]
title: {title}


'''
responses = client.chat.complete(
    model = "mistral-large-latest", 
    messages=[
        {
            "role": "user",
            "content" : prompt
        }
    ],

)

reponse = responses.choices[0].message.content

import json
import re

def clean_llm_json_response(raw_response):
    # Step 1: Remove Markdown code block markers if they exist
    clean_str = re.sub(r"^```json\n|```$", "", raw_response.strip(), flags=re.MULTILINE)

    # Step 2: Unescape if it's a raw string literal
    try:
        clean_str = bytes(clean_str, "utf-8").decode("unicode_escape")
    except Exception as e:
        print("Warning: Unicode escape decoding failed, continuing.")

    # Step 3: Parse JSON
    try:
        data = json.loads(clean_str)
        return data
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return None
data = clean_llm_json_response(reponse)

print(data)
with open('data.json', 'w') as file:
    json.dump(data, file)