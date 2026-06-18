import os
from dotenv import load_dotenv

load_dotenv()

from litellm import completion

response_openai = completion(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=("openai/gpt-4o"),
    messages=[{"role": "user", "content": "what is RAG in one sentence"}],
)

print(" 👀 openai: ", response_openai.choices[0].message.content)


response_groq = completion(
    api_key=os.getenv("GROQ_API_KEY"),
    model=("groq/llama-3.1-8b-instant"),
    messages=[{"role": "user", "content": "what is RAG in one sentence"}],
)

print(" 👀 groq: ", response_groq.choices[0].message.content)
