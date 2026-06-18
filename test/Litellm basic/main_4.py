import os
from dotenv import load_dotenv
from litellm import completion, completion_cost

load_dotenv()

response = completion(
    model=("openai/gpt-4o"),
    messages=[{"role": "user", "content": "Write a haiku about AI."}],
)

cost = completion_cost(completion_response=response)

print("Response:    ", response.choices[0].message.content)
print("\nInput tokens: ", response.usage.prompt_tokens)
print("Output tokens:", response.usage.completion_tokens)
print(f"Cost:         ${cost:.8f}")
