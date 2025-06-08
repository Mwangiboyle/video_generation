from fastapi import FastAPI
from pydantic import BaseModel
import config
import json


app = FastAPI(title="API for video generation")

class script_data(BaseModel):
    title: str
    time: int


@app.post("/generate_script")
async def script_generate(data: script_data):

    idea = data.title
    duration = data.time
    script = config.generate_script(idea, duration)

    response = config.clean_response(script)
    cleaned_script = json.loads(response)
    return cleaned_script

@app.post("/generate images")

async def generate_images():
    response = await script_generate




