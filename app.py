import os
import uuid

from fastapi import FastAPI, File, Form, UploadFile

from video import extract_audio
from analyze import transcribe, analyze_transcript
from fastapi.middleware.cors import CORSMiddleware

# create a fast api
app = FastAPI()

# and make our working directory
os.makedirs(
    "output",
    exist_ok=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create an analysis endpoint
@app.post("/analyze")
async def analyze_video(
    video: UploadFile = File(...),
    description: str = Form(""),
):

    # give the upload its own folder
    job_id = str(uuid.uuid4())

    job_folder = os.path.join(
        "output",
        job_id,
    )

    os.makedirs(
        job_folder,
        exist_ok=True,
    )

    # save the uploaded video
    video_path = os.path.join(
        job_folder,
        "video.mp4",
    )

    audio_path = os.path.join(
        job_folder,
        "audio.wav",
    )

    with open(video_path, "wb") as file:
        content = await video.read()
        file.write(content)

    # extract the audio from the video
    extract_audio(
        video_path,
        audio_path,
    )

    transcript = transcribe(
        audio_path,
    )

    analysis = analyze_transcript(
        transcript,
        description,
    )

    return {
        "job_id": job_id,
        "analyze": analysis,
    }



