# Safe Chat AI

Safe Chat AI is a lightweight chatbot prototype that routes user requests across
multiple LiteLLM models while masking personally identifiable information before
messages reach the model provider.

The project includes:

- Presidio-based PII detection and masking.
- LiteLLM proxy integration for OpenAI, Gemini, and Groq models.
- Simple task classification for `code`, `summary`, and `general` prompts.
- Model fallback chains for higher availability.
- A terminal chat interface and a Streamlit web interface.
- Basic latency, model, task, and cost metadata on each response.

## Project Structure

```text
.
├── config.yaml               # LiteLLM proxy model and guardrail config
├── pyproject.toml            # Project metadata and dependencies
├── requirements.txt          # Exported dependency lock for pip workflows
├── src
│   ├── app.py                # Streamlit chat UI
│   ├── main.py               # ChatBot class and terminal interface
│   ├── presidio_guardrail.py # Local Presidio PII masking helper
│   └── tool.py               # LiteLLM proxy calls, routing, and cost helpers
└── test                      # Experimental LiteLLM/LangChain examples
```

## Requirements

- Python 3.13 or newer.
- `uv` recommended for dependency management.
- API keys for any models you want to use through LiteLLM.
- A database URL for the LiteLLM proxy, if required by your proxy setup.

## Environment Variables

Create a `.env` file in the project root:

```bash
LITELLM_MASTER_KEY=your-master-key
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
DATABASE_URL=your-database-url
```

`src/tool.py` reads `LITELLM_MASTER_KEY` from `.env`. The LiteLLM proxy reads
the provider keys and database URL referenced in `config.yaml`.

## Installation

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the LiteLLM Proxy

Start the proxy from the project root:

```bash
uv run litellm --config config.yaml --port 4000
```

The application expects the proxy at:

```text
http://localhost:4000
```

## Running the Chatbot

Terminal interface:

```bash
uv run python src/main.py
```

Streamlit interface:

```bash
uv run streamlit run src/app.py
```

## How Routing Works

Each user prompt is first masked by Presidio. The masked prompt is then
classified into one of three task types:

- `code`
- `summary`
- `general`

The selected task determines the model fallback order:

| Task | Fallback Order |
| --- | --- |
| `code` | `gpt-4o` -> `groq-llama` -> `gemini-flash` |
| `summary` | `gpt-4o` -> `gemini-flash` -> `groq-llama` |
| `general` | `gemini-flash` -> `groq-llama` -> `gpt-4o` |

If a model call fails, the next model in the chain is attempted.

## Notes

- PII masking is performed locally before the prompt is added to chat history.
- The terminal and Streamlit apps share the same `ChatBot` implementation.
- Cost reporting uses LiteLLM's `completion_cost`; if pricing metadata is not
  available, the app displays `n/a`.
- The `test/` directory contains exploratory scripts rather than a formal test
  suite.
