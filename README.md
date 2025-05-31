# 🎬 AI-Powered Video Generation System

Generate short, engaging educational videos from simple text prompts — with no need for video editing!

## 🚀 Project Overview

This project is a full-stack AI-powered video generation pipeline designed for **YouTube Shorts** and **TikTok creators**. It allows users to input an idea or title, and automatically produces a 60-second video complete with:
- AI-generated script
- Voice-over narration
- Captions
- Stock images/videos
- Ready-to-share video link (via AWS S3)

Our goal is to **eliminate the need for video editing** and empower creators to focus on **content** instead of production.

---

## 🛠️ Features

- ✨ **Script Generation** using OpenAI models (e.g., GPT-4)
- 🎙️ **Voiceover Generation** using OpenAI Whisper (text-to-speech)
- 🎞️ **Video Compilation** using FFmpeg
- 🖼️ **Stock Media** from Pexels API (images + video clips)
- 🧠 **Captioning** with automated syncing
- ☁️ **AWS S3 Integration** for video storage and public access

---

## 🧩 Tech Stack

| Component              | Technology Used                 |
|------------------------|----------------------------------|
| Script Generation      | OpenAI GPT (e.g., gpt-4)         |
| Voiceover              | Whisper / Google Cloud TTS       |
| Media Fetching         | Pexels API                       |
| Video Editing          | FFmpeg                           |
| Backend API            | Python + FastAPI                 |
| File Hosting           | AWS S3                           |

---

## 💡 How It Works

1. **User Input:** User submits a topic/idea for a short video.
2. **Script Generation:** GPT model generates a short educational script.
3. **Voiceover:** The script is converted into an audio narration using Whisper or TTS.
4. **Media Matching:** Pexels API is used to fetch relevant stock visuals.
5. **Video Creation:** FFmpeg combines visuals, voiceover, and captions into a video.
6. **Delivery:** The final video is uploaded to an AWS S3 bucket and a shareable link is returned to the user.

---

## 📦 Installation

```bash
git clone https://github.com/Mwangiboyle/video_generation.git
cd video_generation
pip install -r requirements.txt
```

Set up environment variables for:
- OpenAI API key
- Pexels API key
- AWS credentials (S3 bucket info)

---

## 📌 Use Case

Ideal for:
- Educational content creators on TikTok, Instagram Reels, or YouTube Shorts
- Course creators needing promo content
- Marketers creating quick explainers
- Anyone who wants to generate short videos **without editing**

---

## 🧠 Future Improvements

- GUI-based editor with preview options
- Multilingual support (via Whisper translation)
- Analytics dashboard for video engagement
- More customizable voice and style options

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss your proposed changes.

---

## 📄 License

[MIT License](LICENSE)

---

## 📬 Contact

For feedback, support, or collaboration, reach out to:  
📧 mwangiboyle4@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/josephmwangiboyle)
