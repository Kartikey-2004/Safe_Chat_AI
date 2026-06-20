import os
import re
from dotenv import load_dotenv
from litellm import completion, completion_cost

load_dotenv()

PROXY_URL = "http://localhost:4000"
PROXY_KEY = os.getenv("LITELLM_MASTER_KEY")
REQUEST_TIMEOUT = float(os.getenv("LITELLM_REQUEST_TIMEOUT", "30"))

CODE_HINTS = re.compile(
    r"\b("
    r"code|debug|bug|error|exception|traceback|function|class|api|python|"
    r"javascript|typescript|java|sql|html|css|react|node|fastapi|flask|"
    r"streamlit|docker|kubernetes|git|regex|script|compile|refactor"
    r")\b",
    re.IGNORECASE,
)
SUMMARY_HINTS = re.compile(
    r"\b("
    r"summarize|summary|brief|tldr|tl;dr|recap|outline|extract|condense|"
    r"key points|main points"
    r")\b",
    re.IGNORECASE,
)


def proxy_completion(**kwargs):
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    return completion(
        api_base=PROXY_URL,
        api_key=PROXY_KEY,
        custom_llm_provider="openai",
        **kwargs,
    )


def classify_task(user_query: str) -> str:
    """Fast local classifier used for routing."""
    if CODE_HINTS.search(user_query):
        return "code"
    if SUMMARY_HINTS.search(user_query):
        return "summary"
    return "general"


def call_with_fallbacks(model_chain, messages):
    """Try models in order until one succeeds."""
    last_error = None
    for model in model_chain:
        try:
            return proxy_completion(
                model=model,
                messages=messages,
            )
        except Exception as e:
            print(f"---- {model} failed ({type(e).__name__})")
            last_error = e
    if last_error:
        raise last_error


def calculate_cost(response):
    try:
        return f"${completion_cost(completion_response=response):.6f}"
    except Exception:
        return "n/a"
