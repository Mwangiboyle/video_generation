import requests
from dotenv import load_dotenv
import os
    

# Load environment variables from a .env file if available
load_dotenv(override=True)

# It's best to keep API keys secret and in .env file
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_pexels_videos(query, num_results=1, max_duration=None):
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={num_results}"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return {}
    videos = response.json().get("videos", [])

    all_video_urls = []
    for video in videos:
        file_links = [file["link"] for file in video.get("video_files", [])]
        all_video_urls.extend(file_links)

    return all_video_urls


keywords = ["warm-up", "stretches"]


for word in keywords:
    full_response = search_pexels_videos(word)
    print(f"\nFull response for '{word}':")
    print(full_response)

