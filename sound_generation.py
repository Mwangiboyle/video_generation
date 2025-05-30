from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)

API_KEY =os.getenv('OPENAI_API_KEY')

with open('data.json', 'r') as file:
    data = json.load(file)

narration = ' '.join(item['narration'] for item in data)

print(narration)

client = OpenAI(api_key=API_KEY)
speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input=narration,
    instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(speech_file_path)