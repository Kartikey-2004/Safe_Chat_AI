import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

prompt = "Explain RAG in vector in one sentence"

provider = [
    ("openai", "openai/gpt-4o"),
    ("gemini", "gemini/gemini-2.5-flash"),
    ("groq", "groq/llama-3.1-8b-instant"),
]

for label, model in provider:
    try:
        r = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        print(f"{label:<15}:{r.choices[0].message.content}")
    except Exception as e:
        print(f"{label:<15}:error")
