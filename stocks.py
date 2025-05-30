import requests
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env
load_dotenv(override=True)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_pexels_videos(query, num_results=7, max_duration=None):
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={num_results}"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    videos = response.json().get("videos", [])

    # Optional filtering by max_duration
    #f max_duration:
        #videos = [v for v in videos if v.get("duration", 0) <= max_duration]

    all_video_urls = []
    for video in videos:
        file_links = [file["link"] for file in video.get("video_files", [])]
        all_video_urls.extend(file_links)

    return all_video_urls

# Load the JSON script file
with open("cleaned_script2.json", "r") as f:
    data = json.load(f)
results = []
# Loop over each scene
for i, scene in enumerate(data["scenes"], start=1):
    print(f"\n🎬 Scene {i}")
    keywords = scene.get("keywords", [])

    scene_videos = []

    for keyword in keywords:
        # Search 1 result per keyword, optionally filter by ~5 seconds
        result_urls = search_pexels_videos(keyword, num_results=7, max_duration=7)
        if result_urls:
            scene_videos.append(result_urls[0])  # First matching video
        else:
            print(f"⚠️ No video found for keyword: {keyword}")
    results.append(scene_videos)
    print(f"Keywords: {keywords}")
    print(f"Video URLs: {scene_videos}")


# Save to JSON file
with open("scene_video_results2.json", "w") as out_file:
    json.dump(results, out_file, indent=2)

print("✅ Video results saved to scene_video_results.json")

