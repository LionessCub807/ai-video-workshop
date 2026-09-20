from faster_whisper import WhisperModel
import json

# configure the whisper model
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)

# tells which files to transcribe
segments, info = model.transcribe(
    "output/audio.wav",
    word_timestamps=True,
)

print("Detected language:", info.language)

transcript = []

# print the transcript
for segment in segments:
    # for every word in a segment
    words = []

    # print each word
    for word in segment.words:
        words.append(
            {
                "word": word.word.strip(),
                "start": round(word.start, 2),
                "end": round(word.end, 2),
                "confidence": round(word.probability, 2)
            }
        )

    confidence_scores = [
        word["confidence"]
        for word in words
    ]

    if words:
        lowest_confidence_word = min(
            words,
            key=lambda word: word["confidence"],
        )
    else:
        lowest_confidence_word = None

    if lowest_confidence_word:
        lowest_score = lowest_confidence_word["confidence"]

        if lowest_score >= 0.50:
            reliability = "high"
        elif lowest_score >= 0.30:
            reliability = "medium"
        else:
            reliability = "low"
    else:
        reliability = "low"

    if confidence_scores:
        average_confidence = (
            sum(confidence_scores)
            / len(confidence_scores)
        )
    else:
        average_confidence = 0

    # print the transcript segments
    print(
        round(segment.start, 2),
        "->",
        round(segment.end, 2),
        segment.text,
    )

    # construct transcript
    transcript.append(
        {
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip(),
            "confidence": round(average_confidence, 2),
            "words": words,
            "lowest_word": (
                lowest_confidence_word["word"]
                if lowest_confidence_word
                else None
            ),
            "lowest_word_confidence": (
                lowest_confidence_word["confidence"]
                if lowest_confidence_word
                else 0
            ),
            "words": words,
            "reliability": reliability,
        }
    )

# print it to a file
with open("output/transcript.json", "w", encoding="utf-8") as file:
    json.dump(
        transcript, 
        file,
        indent=2,
        ensure_ascii=False,
    )

