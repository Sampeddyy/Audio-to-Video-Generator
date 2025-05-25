# video_fetcher.py (Pixabay video + Freesound music)

import os
import random
import requests

from dotenv import load_dotenv
load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")

PIXABAY_VIDEO_ENDPOINT = "https://pixabay.com/api/videos/"
FREESOUND_SEARCH_ENDPOINT = "https://freesound.org/apiv2/search/text/"
FREESOUND_DOWNLOAD_BASE = "https://freesound.org/data/previews"

def fetch_random_video(output_path, query="people", min_duration=15):
    print("🎬 Fetching from Pixabay...")
    queries = [query, "war","explosion","fire"]

    for q in queries:
        print(f"🔍 Trying query: '{q}' with minimum duration {min_duration}s")
        params = {
            "key": PIXABAY_API_KEY,
            "q": q,
            "video_type": "film",
            "per_page": 50,
        }
        res = requests.get(PIXABAY_VIDEO_ENDPOINT, params=params)
        res.raise_for_status()
        hits = res.json().get("hits", [])

        filtered = [hit for hit in hits if hit.get("duration", 0) >= min_duration]
        if not filtered:
            continue

        selected = random.choice(filtered)
        video_url = selected["videos"]["large"]["url"]
        print(f"⬇ Downloading: {video_url}")
        video_data = requests.get(video_url)
        with open(output_path, "wb") as f:
            f.write(video_data.content)
        print(f"✅ Video saved to {output_path}")
        print(f"✅ Downloaded from query: '{q}'")
        return

    raise RuntimeError("❌ No suitable video found on Pixabay.")

def fetch_random_music(output_path, mood="uplifting", min_duration=30):
    print(f"🎶 Fetching music from Freesound with mood='{mood}' and duration ≥ {min_duration}s")
    headers = {"Authorization": f"Token {FREESOUND_API_KEY}"}
    params = {
        "query": mood,
        "filter": f"duration:[{min_duration} TO 120]",
        "fields": "id,duration,previews",
        "page_size": 20,
    }
    res = requests.get(FREESOUND_SEARCH_ENDPOINT, headers=headers, params=params)
    res.raise_for_status()
    data = res.json()
    results = data.get("results", [])

    if not results:
        raise RuntimeError("❌ No matching music found on Freesound.")

    selected = random.choice(results)
    preview_url = selected["previews"].get("preview-hq-mp3")
    print(f"🎵 Downloading from: {preview_url}")
    track_data = requests.get(preview_url)
    with open(output_path, "wb") as f:
        f.write(track_data.content)
    print(f"✅ Saved background track to {output_path}")
