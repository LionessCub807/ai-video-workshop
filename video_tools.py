"""
The helper function for FFmpeg/video processing. This program uses ffprobe
to describe the video via JSON, then extracts useful data from the raw JSON. 
It's going to report the width, height, codec, duration, and fps to the user.
"""
import json # helps python read JSON data
import subprocess # let's python run another program installed on the computer

# ffprobe is going to describe the video in a machine-friendly format(JSON)

def get_video_info(video_path):
    # commands for ffprobe
    command = [
        "ffprobe", # run ffprobe
        "-v", # hide unnecessary status messages
        "quiet",
        "-print_format", # return the information as JSON
        "json",
        "-show_format", # gives information about the file, such as duration
        "-show_streams", # gives information about the video and audio tracks
        video_path, # inspects whatever file was passed into the function
    ]

    # runs ffprobe
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    # load the result into a variable
    data = json.loads(result.stdout)

    # iterate through streams in data until "video" is found(extract the video data)
    video_stream = next(
        stream
        for stream in data["streams"]
        if stream["codec_type"] == "video"
    )

    # iterate through streams for "audio"
    audio_stream = next(
        (
            stream 
            for stream in data["streams"]
            if stream["codec_type"] == "audio"
        ),
        None,
    )

    # add duration
    duration = float(data["format"]["duration"])

    # average frame rate
    fps_string = video_stream["avg_frame_rate"]
    fps_string = fps_string.split("/")

    # get integer/decimal instead of fraction
    numerator = float(fps_string[0])
    denominator = float(fps_string[1])

    # calculate frames per second
    fps = numerator / denominator

    # print the width, height, and codec
    print("Width:", video_stream["width"])
    print("Height:", video_stream["height"])
    print("Codec:", video_stream["codec_name"])
    print("Duration:", duration, "seconds")
    print("FPS:", round(fps, 2))

    # check if there's audio
    if audio_stream:
        print("Audio codec:", audio_stream["codec_name"])
    else:
        print("Audio codec: None")


def extract_audio(video_path, output_path):

    # commands for ffmpeg
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        output_path,
    ]

    # run the commands
    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

# extract video frames
def extract_frame(video_path, timestamp, output_path):
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(timestamp),
        "-i",
        video_path,
        "-frames:v",
        "1",
        output_path,
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

def extract_moment_frames(
        video_path,
        start,
        end,
        output_prefix,
):
    middle = (start + end) / 2

    timestamps = [
        start,
        middle,
        end,
    ]

    frame_paths = []

    for index, timestamp in enumerate(timestamps):
        output_path = (
            f"{output_prefix}_{index}.jpg"
        )

        extract_frame(
            video_path,
            timestamp,
            output_path,
        )

        frame_paths.append(output_path)

    return frame_paths


    
        
    
