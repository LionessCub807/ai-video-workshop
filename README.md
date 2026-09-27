# Video Editor Enhancer

**Video Editor Enhancer** is a tool designed to help video editors streamline the process of editing long-form videos.

It analyzes video content to identify important timestamps and suggests potential edits, including **why each edit may improve the video**.

## Project Goal

Editing long videos can require hours of manually reviewing footage to find moments that could benefit from sound effects, cuts, emphasis, or other enhancements.

Video Editor Enhancer aims to simplify this process by:

- Identifying key moments in a video
- Providing precise timestamps
- Suggesting potential edits
- Recommending appropriate sound effects
- Explaining the reasoning behind each suggestion

The goal is **not to replace the editor**, but to provide useful recommendations that make the editing workflow faster and easier.

## Supported Sound Effect Suggestions

The model can currently identify opportunities for the following sound effects:

| Sound Effect | Typical Use |
| --- | --- |
| **Vine Boom** | Emphasizing dramatic, surprising, or absurd moments |
| **Record Scratch** | Sudden interruptions, mistakes, or unexpected changes |
| **Ding** | Highlighting an idea, realization, or important point |
| **Crowd Cheer** | Celebrations, achievements, or exciting moments |
| **Buzzer** | Incorrect answers, failures, or negative outcomes |
| **Whoosh** | Transitions, movement, reveals, or quick changes |
| **No Sound Effect** | When the moment works better without an added effect |

## Example Output

The model could return suggestions in a format similar to:

| Timestamp | Suggested Edit | Reason |
| --- | --- | --- |
| `00:02:14` | Vine Boom | Emphasizes an unexpected statement |
| `00:05:32` | Ding | Highlights an important realization |
| `00:08:47` | Record Scratch | Fits the sudden interruption in the conversation |
| `00:12:05` | No Sound Effect | The natural pause already provides enough emphasis |
| `00:15:21` | Whoosh | Helps emphasize the transition into a new topic |

## How It Works

```text
Long Video
    ↓
Video / Transcript Analysis
    ↓
Identify Important Moments
    ↓
Evaluate Editing Opportunities
    ↓
Recommend Sound Effect / Edit
    ↓
Explain Recommendation
    ↓
Timestamped Editing Suggestions
```

Instead of manually searching through an entire video for editing opportunities, editors can use the generated suggestions as a starting point for their workflow.

## 🛠️ Tech Stack

Video Editor Enhancer uses a combination of AI, backend, and frontend technologies to analyze videos and present editing suggestions.

| Technology | Purpose |
| --- | --- |
| **Python** | Core backend language used for video processing and application logic |
| **FastAPI** | Provides the backend API and connects the frontend with the processing pipeline |
| **Whisper** | Transcribes video audio into timestamped text for analysis |
| **Ollama + Qwen** | Runs the language model locally to analyze transcripts and generate editing suggestions |
| **React** | Builds the interactive frontend interface |
| **Vite** | Provides the frontend development and build environment |

### Processing Pipeline

1. The user uploads or selects a video through the **React + Vite** frontend.
2. The frontend sends the video to the **FastAPI** backend.
3. **Whisper** transcribes the video's audio and generates timestamped text.
4. The transcript is passed to **Qwen**, running locally through **Ollama**.
5. Qwen analyzes the content and identifies moments that could benefit from an edit or sound effect.
6. The backend returns the timestamps, recommendations, and reasoning to the frontend.
7. The editor reviews the suggestions and decides which ones to use.

## Future Improvements

Potential additions include:

- Audio analysis
- Image analysis

## Project Status

> **Work in Progress**

Video Editor Enhancer is currently under development. Features, supported edits, and model capabilities may change as the project evolves.
