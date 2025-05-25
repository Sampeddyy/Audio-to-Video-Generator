import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from video_bot.video_maker import make_video

# Change these based on your actual files
make_video("one_script.pdf", "one_script_20250518_005530.mp3")
