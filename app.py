# The main program that runs
from video_tools import get_video_info, extract_audio, extract_frame # goes into video_tools.py and brings the get_video_info function
import os


os.makedirs("output", exist_ok=True)
get_video_info("test_video.mp4")

print()
print("Extracting audio...")

# extract audio
extract_audio(
    "test_video.mp4",
    "output/audio.wav",
)

# extract video frames
extract_frame(
    "test_video.mp4",
    15.58,
    "output/test_frame.jpg",
)

print("Frame extracted!")

print("Done!")