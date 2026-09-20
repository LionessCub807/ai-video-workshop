import json
import os

from ollama import chat
from video_tools import extract_moment_frames

os.makedirs(
    "output/frames",
    exist_ok=True,
)

# load your detected moments
with open(
    "output/moments.json",
    "r",
    encoding="utf-8",
) as file:
    data = json.load(file)

moments = data["moments"]

moment = moments[0]

print(
    "Analyzing:",
    moment["start"],
    "->",
    moment["end"],
)

frame_paths = extract_moment_frames(
    "test_video.mp4",
    moment["start"],
    moment["end"],
    "output/frames/moment_0",
)

print("Frames:")

for path in frame_paths:
    print(path)

prompt = f"""
You are verifying a moment detected in a video.

The earlier text model classified this moment as:

Type: {moment['type']}
Confidence: {moment['confidence']}
Description: {moment['description']}

The moment occurs from:
{moment['start']} -> {moment['end']}

You are also given one video frame from the middle of this moment.

Your job is to decide whether the visual evidence supports
the existing classification.

Return:

- visual_description: what is visibly happening
- supports_classification: true or false
- confidence: number from 0.0 to 1.0
- reason: short explanation

Be conservative.

If the frame does not provide enough evidence, set
supports_classification to false.

Return ONLY valid JSON.
"""

response = chat(
    model="qwen3-vl:8b",
    messages=[
        {
            "role": "user",
            "content": prompt,
            "images": [frame_paths[1]],
        }
    ],
    format="json",
    options={
        "num_predict": 300,
    },
)

raw_response = response.message.content

if not raw_response:
    print("No visual response returned.")
    raise SystemExit

visual_result = json.loads(raw_response)

print()
print("Visual description:")
print(visual_result["visual_description"])

print()
print("Supports classification:")
print(visual_result["supports_classification"])

print()
print("Visual confidence:")
print(visual_result["confidence"])

print()
print("Reason:")
print(visual_result["reason"])
