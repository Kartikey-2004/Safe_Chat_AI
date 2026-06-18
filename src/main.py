import time

from presidio_guardrail import mask_pii
from tool import (
    classify_task,
    call_with_fallbacks,
    calculate_cost,
)

class ChatBot:
    def __init__(self):
        self.chat_history = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Maintain context from previous messages."
                ),
            }
        ]

    def smart_chat(self, user_query: str):
        total_start = time.time()

        # Applying guardrail
        safe_query = mask_pii(user_query)

        task = classify_task(safe_query)

        routing = {
            "code": [
                "gpt-4o",
                "groq-llama",
                "gemini-flash",
            ],
            "summary": [
                "gpt-4o",
                "gemini-flash",
                "groq-llama",
            ],
            "general": [
                "gemini-flash",
                "groq-llama",
                "gpt-4o",
            ],
        }

        model_chain = routing.get(
            task,
            routing["general"],
        )

        # safe query
        self.chat_history.append(
            {
                "role": "user",
                "content": safe_query,
            }
        )

        model_start = time.time()

        response = call_with_fallbacks(
            model_chain=model_chain,
            messages=self.chat_history,
        )

        latency = time.time() - model_start
        total_latency = time.time() - total_start
        answer = response.choices[0].message.content

        self.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return {
            "detected_task": task,
            "model_used": response.model,
            "answer": answer,
            "latency_sec": round(latency, 2),
            "total_latency_sec": round(total_latency, 2),
            "cost_usd": calculate_cost(response),
            "safe_query": safe_query,
        }


def main():
    """Terminal Interface"""
    bot = ChatBot()

    print("\n🤖 AI Chat Started")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("👤 You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye!")
            break

        try:
            result = bot.smart_chat(user_input)

            # Print a warning if the guardrail masked anything
            if result["safe_query"] != user_input:
                print("\n🛡️  [Guardrail] PII detected and masked before processing.")

            print(f"\n🤖 Assistant: {result['answer']}")
            print(
                f"\n[Model={result['model_used']} | "
                f"Task={result['detected_task']} | "
                f"Model latency={result['latency_sec']}s | "
                f"Total latency={result['total_latency_sec']}s | "
                f"Cost={result['cost_usd']}]"
            )
            print("\n" + "-" * 50 + "\n")

        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
