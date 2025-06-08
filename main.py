from fastapi import FastAPI
from pydantic import BaseModel
import config


app = FastAPI(title="API for video generation")

class script_data(BaseModel):
    title: str
    time: int


@app.post("/generate_script")
async def script_generate(data: script_data):

    idea = data.title
    duration = data.time
    script = config.generate_script(idea, duration)

    cleaned_script = config.clean_response(script)

    return cleaned_script


