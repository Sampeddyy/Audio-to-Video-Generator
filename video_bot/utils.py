import os
import random

def get_random_video(folder):
    videos = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.mov', '.mkv'))]
    if not videos:
        raise FileNotFoundError("No video clips in video_input/")
    return os.path.join(folder, random.choice(videos))
