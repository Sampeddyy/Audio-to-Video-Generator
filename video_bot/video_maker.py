# video_maker.py (final fix for audio sync + BGM trimming)

import os
import ffmpeg
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    CompositeAudioClip,
    ImageClip,
)
from moviepy.video.fx.loop import loop
from moviepy.audio.fx.volumex import volumex
from video_bot.video_fetcher import fetch_random_video, fetch_random_music
from audio_bot.pdf_processor import PDFProcessor
import textwrap

def create_line_caption(line, start_time, duration, video_size, font_path):
    width, height = video_size
    font_size = 70

    img = Image.new("RGBA", (width, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
    x = (width - text_width) // 2
    y = (200 - text_height) // 2
    draw.text((x, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")

    img_clip = (
        ImageClip(np.array(img))
        .set_duration(duration)
        .set_start(start_time)
        .set_position(("center", "center"))
    )
    return img_clip

def generate_caption_clips(text, video_size, total_duration, font_path):
    lines = textwrap.wrap(text, width=35)
    duration_per_line = total_duration / len(lines)
    clips = []

    for i, line in enumerate(lines):
        start_time = i * duration_per_line
        clip = create_line_caption(line, start_time, duration_per_line, video_size, font_path)
        clips.append(clip)

    return clips

def make_video(pdf_filename: str, audio_filename: str):
    base = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(base, "pdf_input", pdf_filename)
    audio_path = os.path.join(base, "audio_output", audio_filename)
    temp_video_path = os.path.join(base, "video_output", "temp_video.mp4")
    raw_video_path = os.path.join(base, "video_output", "raw_video.mp4")
    audio_out_path = os.path.join(base, "video_output", "temp_audio.m4a")
    final_output_path = os.path.join(base, "video_output", f"{os.path.splitext(pdf_filename)[0]}_final.mp4")
    font_path = os.path.join(base, "fonts", "Oswald-SemiBold.ttf")
    bgm_path = os.path.join(base, "audio_output", "bgm_track.mp3")

    print("🎬 Downloading video from Pixabay...")
    fetch_random_video(temp_video_path, query="meme")

    print("🎶 Fetching background music from Freesound...")
    fetch_random_music(bgm_path, mood="uplifting", min_duration=30)

    print("📄 Extracting subtitle text...")
    text = PDFProcessor.extract_text(pdf_path)

    print("🎧 Loading video and audio...")
    narration_audio = AudioFileClip(audio_path)
    narration_duration = narration_audio.duration

    background_audio = AudioFileClip(bgm_path)
    if background_audio.duration > narration_duration:
        background_audio = background_audio.subclip(0, narration_duration)
    background_audio = background_audio.volumex(0.3)

    print("🎥 Formatting video for Shorts/Reels...")
    original_clip = VideoFileClip(temp_video_path)
    target_width, target_height = 1080, 1920
    resized = original_clip.resize(height=target_height)

    if resized.w > target_width:
        x_center = resized.w // 2
        video_clip = resized.crop(
            x1=x_center - target_width // 2,
            x2=x_center + target_width // 2,
            y1=0,
            y2=target_height,
        )
    else:
        padding = (target_width - resized.w) // 2
        video_clip = resized.margin(
            left=padding,
            right=(target_width - resized.w - padding),
            color=(0, 0, 0)
        )

    if video_clip.duration < narration_duration:
        video_clip = loop(video_clip, duration=narration_duration)
    else:
        video_clip = video_clip.subclip(0, narration_duration)

    print("💬 Rendering line-by-line captions...")
    caption_clips = generate_caption_clips(text, video_clip.size, narration_duration, font_path)

    print("📼 Exporting raw video (no audio)...")
    if os.path.exists(raw_video_path):
        os.remove(raw_video_path)

    final = CompositeVideoClip([video_clip] + caption_clips)
    final.write_videofile(raw_video_path, codec="libx264", fps=24)

    print("🔊 Exporting audio...")
    if os.path.exists(audio_out_path):
        os.remove(audio_out_path)

    mixed_audio = CompositeAudioClip([
        narration_audio.set_start(0),
        background_audio.set_start(0)
    ])
    mixed_audio = mixed_audio.set_duration(narration_duration)
    mixed_audio.write_audiofile(audio_out_path, fps=44100, codec="aac")

    print("🛠 Merging video + audio with FFmpeg...")
    if os.path.exists(final_output_path):
        os.remove(final_output_path)

    ffmpeg.output(
        ffmpeg.input(raw_video_path),
        ffmpeg.input(audio_out_path),
        final_output_path,
        vcodec="libx264",
        pix_fmt="yuv420p",
        acodec="aac",
        strict="experimental",
    ).run(
        cmd="C:\\ffmpeg-2025-05-15-git-12b853530a-essentials_build\\bin\\ffmpeg.exe",
        overwrite_output=True,
    )

    print(f"✅ Final video saved to: {final_output_path}")
