![Python](https://img.shields.io/badge/built_with-python-blue?logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

# Audio-to-Video-Generator
A Python-based tool that converts written scripts into narrated videos using AI voiceovers and stock footage — fully automated from PDF to MP4.


## 🚀 Features
- Extracts text from PDF input
- Converts text to speech (TTS)
- Fetches relevant stock videos
- Merges video + audio + captions
- Outputs ready-to-share MP4 videos

## 📁 Folder Structure
- `/video_bot`: Python modules handling audio, video, and automation
- `/audio_output`: Stores generated audio files
- `/video_output`: Final and intermediate video files
- `/fonts`: Custom fonts for subtitles
- `/pdf_input`: Source PDF scripts

## ⚙️ Tech Stack
- Python
- PyDub
- FFMPEG
- OpenAI / ElevenLabs API (TTS)
- Pexels API (video)

## 📦 Setup
```bash
pip install -r requirements.txt
