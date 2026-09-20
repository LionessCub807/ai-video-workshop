from ollama import chat

response = chat(
    model="qwen3-vl:8b",
    messages=[
        {
            "role": "user",
            "content": (
                "Describe what is happening in this image. "
                "Focus on people, facial expressions, actions, "
                "objects, and anything visually unusual."
            ),
            "images": [
                "output/test_frame.jpg"
            ],
        }
    ],
)

print(response.message.content)