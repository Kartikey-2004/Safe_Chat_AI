import os
import time
from litellm import Router
from collections import Counter

model_list = [
    {
        "model_name": "chat",
        "litellm_params": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
        "model_info": {"id": "🔵 OpenAI"},
    },
    {
        "model_name": "chat",
        "litellm_params": {
            "model": "groq/llama-3.3-70b-versatile",
            "api_key": os.getenv("GROQ_API_KEY"),
        },
        "model_info": {"id": "🟢 Groq"},
    },
]


# -----------------------------------least busy-------------------------------


# router = Router(
#     model_list=model_list,
#     routing_strategy="least-busy",
# )

# hits = Counter()
# for i in range(8):
#     r = router.completion(
#         model="chat",
#         messages=[{"role": "user", "content": f"Say 'OK' #{i}"}],
#         max_tokens=5,
#     )
#     hits[r._hidden_params.get("model_id", "?")] += 1
#     print(f"Request {i+1} → {r._hidden_params.get('model_id', '?')}")

# print("\n🎯 Distribution:")
# for k, v in hits.most_common():
#     print(f"   {k}: {'█' * v} ({v})")


# -----------------------------latency-based-routing---------------------------


# router = Router(
#     model_list=model_list,
#     routing_strategy="latency-based-routing",  # 👈 picks the fastest
# )

# # Send 10 requests and watch which deployments get picked over time
# print(f"{'Req':<6}{'Deployment':<32}{'Latency':<10}")
# print("-" * 50)

# for i in range(10):
#     start = time.time()
#     r = router.completion(
#         model="chat",
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Reply with exactly: OK",
#             }
#         ],
#         max_tokens=5,
#     )
#     latency_ms = (time.time() - start) * 1000
#     deployment = r._hidden_params.get("model_id", "?")
#     print(f"#{i+1:<5}{deployment:<32}{latency_ms:>6.0f} ms")
