from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Load API keys
open_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=open_api_key)

title = input("Enter your idea here: ")
time_duration = 100

# Prompt to generate structured JSON output
prompt = f"""
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
- Time_duration: {time_duration} seconds
"""

# Fetch response from model
responses = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt}
    ]
)

response = responses.choices[0].message.content.strip()

# Debug print
print("=== MODEL RESPONSE RAW ===")
print(repr(response))  # Shows escape characters

# Remove markdown formatting
if response.startswith("```json"):
    response = response[7:]
if response.endswith("```"):
    response = response[:-3]

# Try parsing cleaned response
try:
    cleaned_json = json.loads(response)
    print("✅ Cleaned JSON parsed successfully.")

    # Save to file
    with open("cleaned_script2.json", "w") as f:
        json.dump(cleaned_json, f, indent=2)
    print("✅ Saved to cleaned_script.json")

except json.JSONDecodeError as e:
    print("❌ JSON parsing failed:", e)
    with open("raw_output.txt", "w") as f:
        f.write(response)
    print("⚠️ Raw model response saved to raw_output.txt for inspection.")
