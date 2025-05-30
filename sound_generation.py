from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)

API_KEY =os.getenv('OPENAI_API_KEY')

with open("cleaned_script2.json", "r") as f:
    data = json.load(f)

narration = ' '.join(scene['narration'] for scene in data['scenes'])

print(narration)

client = OpenAI(api_key=API_KEY)
speech_file_path = Path(__file__).parent / "speech2.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="echo",
    input=narration,
    instructions="Speak in a positive tone.",
) as response:
    response.stream_to_file(speech_file_path)