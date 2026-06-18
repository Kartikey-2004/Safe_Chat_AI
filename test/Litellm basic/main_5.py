import os
import time
import litellm
from dotenv import load_dotenv
from litellm import completion
from litellm.caching import Cache

load_dotenv()

litellm.cache = Cache(type="local")

prompt = "What does LLM stand for? Answer in one line."

start = time.time()
r1 = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    caching=True,
)
t1 = time.time() - start
print(f"❄️  First call (API):   {t1:.2f}s — {r1.choices[0].message.content}")

start = time.time()
r2 = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    caching=True,
)
t2 = time.time() - start
print(f"⚡ Second call (cache): {t2:.4f}s — {r2.choices[0].message.content}")

print(f"\n🚀 Speedup: {t1/t2:.1f}x faster, and ZERO cost on the second call!")
