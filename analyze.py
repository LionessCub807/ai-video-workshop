import json

from faster_whisper import WhisperModel
from ollama import chat

whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)

def transcribe(audio_path):
    segments, _ = whisper_model.transcribe(
        audio_path,
    )

    transcript = []

    for segment in segments:
        transcript.append(
            {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip(),
            }
        )

    return transcript

def analyze_transcript(transcript, video_description):
    transcript_text = ""

    for segment in transcript:
        transcript_text += (
            f"{segment['start']} -> {segment['end']}\n"
            f"{segment['text']}\n\n"
        )

    prompt = f"""
    You analyze videos for content creators.

    VIDEO CONTEXT:
    {video_description}

    Your job is to identify moments that may be useful
    during video editing.

    For each meaningful moment, perform these steps:

    1. Understand what is happening.
    2. Determine the sentiment or emotional tone.
    3. Decide whether an edit would improve the moment.
    4. Decide whether a sound effect would improve the moment.

    SENTIMENTS:

    - funny
    - surprising
    - exciting
    - positive
    - negative
    - awkward
    - neutral

    EDIT SUGGESTIONS:

    Examples include:

    - quick zoom
    - punch in
    - freeze frame
    - replay
    - text emphasis
    - reaction cut
    - no edit

    SOUND EFFECT SUGGESTIONS:

    Examples include:

    - vine boom
    - record scratch
    - ding
    - crowd cheer
    - buzzer
    - whoosh
    - no sound effect

    RULES:

    1. Only use timestamps that appear in the transcript.

    2. Do not invent moments.

    3. Do not classify confusing or unusual transcript wording
    as funny or surprising simply because it sounds strange.

    4. Only suggest an edit when it meaningfully improves
    the moment.

    5. Only suggest a sound effect when it meaningfully
    improves the moment.

    6. "no edit" and "no sound effect" are valid answers.

    7. Keep descriptions and suggestions short.

    8. Consider the video context when making suggestions.

    9. Prefer a small number of useful moments over many
    weak suggestions.

    Return ONLY valid JSON:

    {{
        "moments": [
            {{
                "start": 12.4,
                "end": 15.8,
                "sentiment": "funny",
                "description": "The speaker realizes they made a mistake.",
                "edit_suggestion": "Quick zoom on the reaction.",
                "sound_effect_suggestion": "record scratch"
            }}
        ]
    }}

    TRANSCRIPT:

    {transcript_text}
    """

    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
        think=False,
    )

    raw_response = response.message.content

    if not raw_response:
        raise ValueError(
            "Qwen returned anempty response."
        )

    result = json.loads(raw_response)
    '''
    if "moments" not in result:
            raise ValueError(
                "Qwen response is missing 'moments'."
            )
    '''
    

    return result
        