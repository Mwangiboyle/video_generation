import os
import openai
import subprocess
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

# === Set Up OpenAI Client ===
client = openai.OpenAI(api_key=openai_api_key)

# === File Paths ===
video_files = ['videos/video1.mp4', 'videos/video4.mp4', 'videos/video5.mp4', 'videos/video3.mp4','videos/video2.mp4']
audio_file = 'speech.mp3'
combined_video = 'combined.mp4'
trimmed_video = 'trimmed_video.mp4'
final_video = 'final_output_with_subs.mp4'
srt_file = 'transcript.srt'
concat_list_file = 'videos.txt'
normalized_dir = 'normalized_videos'
os.makedirs(normalized_dir, exist_ok=True)

# === STEP 1: Normalize all videos to ensure FFmpeg concat compatibility ===
print("🔧 Normalizing input videos...")
normalized_files = []
for i, video in enumerate(video_files):
    output_path = os.path.join(normalized_dir, f"video_{i}.mp4")
    subprocess.run([
        'ffmpeg', '-y', '-i', video,
        '-vf', 'scale=1280:720,fps=30',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k',
        output_path
    ], check=True)
    normalized_files.append(output_path)

# === STEP 2: Create concat list ===
with open(concat_list_file, 'w') as f:
    for file in normalized_files:
        f.write(f"file '{os.path.abspath(file)}'\n")

# === STEP 3: Concatenate the videos ===
print("🔄 Concatenating normalized videos...")
subprocess.run([
    'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
    '-i', concat_list_file,
    '-c', 'copy',
    combined_video
], check=True)
# === Step 3: Get MP3 audio duration ===
def get_audio_duration(audio_path):
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        audio_path
    ], capture_output=True, text=True)
    return float(result.stdout.strip())

audio_duration = get_audio_duration(audio_file)
print(f"🕒 Audio duration: {audio_duration:.2f} seconds")

# === Step 4: Trim video to match audio length ===
print("✂️ Trimming video to match audio duration...")
subprocess.run([
    'ffmpeg', '-y', '-i', combined_video, '-i', audio_file,
    '-t', str(audio_duration),
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-c:a', 'aac',
    '-shortest', trimmed_video
], check=True)

# === Step 5: Transcribe audio using OpenAI Whisper ===
print("🧠 Transcribing audio with OpenAI Whisper...")
audio_file = open("speech.mp3", "rb")
transcript = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json"
    )

segments = transcript.segments

# === Step 6: Generate SRT subtitle file ===
print("💾 Saving transcript to SRT file...")
def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open(srt_file, "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments):
        f.write(f"{i + 1}\n")
        f.write(f"{format_srt_time(segment.start)} --> {format_srt_time(segment.end)}\n")
        f.write(f"{segment.text.strip()}\n\n")

# === Step 7: Burn subtitles into final video ===
print("🔥 Burning subtitles into final video...")
subprocess.run([
    'ffmpeg', '-y', '-i', trimmed_video, '-vf', f"subtitles={srt_file}",
    '-c:a', 'copy', final_video
], check=True)

print(f"✅ Final video with subtitles saved as: {final_video}")
