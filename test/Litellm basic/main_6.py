import os
from litellm import Router

model_list = [
    {
        "model_name": "fast-cheap",
        "litellm_params": {
            "model": "groq/llama-3.3-70b-versatile",
            "api_key": os.getenv("GROQ_API_KEY"),
        },
    },
    {
        "model_name": "smart-coding",
        "litellm_params": {
            "model": "openai/gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
    },
    {
        "model_name": "balanced",
        "litellm_params": {
            "model": "openai/gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
    },
]

router = Router(model_list=model_list)

fast_response = router.completion(
    model="fast-cheap",
    messages=[
        {
            "role": "user",
            "content": "Summarize: AI is changing software.",
        }
    ],
)

code_response = router.completion(
    model="smart-coding",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to reverse a string.",
        }
    ],
)

print("⚡ Fast/cheap (Groq): ", fast_response.choices[0].message.content[:150])
print("\n🧠 Smart/coding (GPT-4o):\n", code_response.choices[0].message.content[:300])
