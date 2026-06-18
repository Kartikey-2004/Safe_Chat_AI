import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

response = completion(
    model=("gemini/gemini-1.5-flash"),
    messages=[
        {
            "role": "user",
            "content": "What is an LLM Gateway?",
        }
    ],
    fallbacks=[
        "gpt-4o-mini",
        "groq/llama-3.3-70b-versatile",
    ],
)

print(
    "Response:",
    response.choices[0].message.content[:200],
    "...",
)

print(
    "\nWhich model actually answered?",
    response.model,
)
