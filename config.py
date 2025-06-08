from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()



def generate_script(title: str, duration: int):

    api_key = os.getenv("OPENAPI_KEY")


    client = OpenAI(api_key=api_key)


    openai_prompt = f"""
    You are an advanced AI script generator tasked with creating detailed video scripts based on a given title and time duration.

    Please output the result in **strict JSON format**, like this:

    {{
    "scenes": [
        {{
        "narration": "Scene narration here.",
        "keywords": ["keyword1", "keyword2"],
        "visuals": "Visual description here."
        }}
    ]
    }}

    Ensure:
    1. Each scene includes a keyword array.
    2. Final scene has a call to action.
    3. JSON must start with '{{' and be parsable by Python's json module.

    Input:
    - Title: {title}
    - Time_duration: {duration} seconds
"""
    responses = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": openai_prompt}
    ]
)
    response = responses.choices[0].message.content.strip()
    return response

def clean_response(response: str):
    repr(response)

    # Remove markdown formatting
    if response.startswith("```json"):
        response = response[7:]
    if response.endswith("```"):
        cleaned_response = response[:-3]

    return cleaned_response