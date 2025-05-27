from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Get API Key
GEMINI_API_KEY = os.getenv("GEMMA_API_KEY")

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY)

# Sandwich scene dictionary
sandwich_scenes = {
    "idea": "preparing sandwich at home",
    "environment": "Cozy Home Kitchen",
    "scene1": "Overhead shot: Hands selecting fresh ingredients—artisan bread, deli meats, vibrant vegetables, and cheese—from a sunlit kitchen counter.",
    "scene2": "Close-up: A hand carefully lays two slices of sourdough bread side-by-side on a rustic wooden cutting board.",
    "scene3": "Mid-shot: A knife, gleaming with a thin layer of creamy mayonnaise, poised mid-spread over a slice of bread. Soft kitchen light.",
    "scene4": "Detailed shot: Crisp, green lettuce leaves being gently placed onto the mayonnaise-covered bread, forming a fresh bed.",
    "scene5": "Close-up: Slices of sharp cheddar cheese carefully layered over the lettuce, their edges slightly overlapping, catching the light.",
    "scene6": "Macro shot: Thinly sliced, juicy tomato rounds being arranged artfully on top of the cheese, droplets of moisture visible.",
    "scene7": "Mid-shot: Folded slices of smoked turkey being generously stacked onto the tomatoes, creating height and texture.",
    "scene8": "Close-up: A drizzle of honey mustard being artfully applied to the underside of the top slice of bread, held above the sandwich.",
    "scene9": "Action shot, frozen: The top slice of bread, mustard-side down, just milliseconds before making contact, completing the sandwich structure.",
    "scene10": "Dynamic angle: A sharp chef's knife, held firmly, mid-slice, cutting diagonally through the towering sandwich with precision.",
    "scene11": "Close-up: The two perfectly cut halves of the sandwich resting on the cutting board, showcasing their vibrant, stacked layers invitingly.",
    "scene12": "Final shot: The beautifully crafted sandwich halves plated neatly, perhaps with a side of chips, ready to be enjoyed. Soft focus background."
}

environment = sandwich_scenes["environment"]

# Loop through each scene
for key, scene in sandwich_scenes.items():
    if not key.startswith("scene"):
        continue

    prompt = f"Generate an image of this scene: {scene} in the environment: {environment}"

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-preview-image-generation',
            contents=[
                types.Content(
                    role='user',
                    parts=[
                        types.Part.from_text(text=prompt)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        # Save image response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                filename = f"{key}.png"
                image.save(filename)
                print(f"[✓] Saved {filename}")
                time.sleep(1)  # Be nice to the API
    except Exception as e:
        print(f"[!] Error generating {key}: {e}")
