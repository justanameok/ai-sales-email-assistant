# AI Sales Email Assistant

Demo application that shows how AI can automate sales email workflows.

Paste a customer email to:
- Analyze customer intent
- Extract structured information
- Score the lead
- Generate a suggested reply

## Setup

1. Create and activate a virtual environment:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
```

This project uses any OpenAI-compatible API. Edit only these values in `.env`:

```
LLM_API_KEY=your_key_here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

Examples:

| Provider | LLM_BASE_URL | LLM_MODEL |
|----------|--------------|-----------|
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| OpenAI | _(leave empty)_ | `gpt-4o-mini` |

DeepSeek keys: https://platform.deepseek.com/api_keys
## Run

```bash
streamlit run app/ui.py
```

## Project structure

```
ai-sales-email-assistant/
├── app/                  # Streamlit UI
├── services/             # Email analysis and reply generation
├── models/               # Pydantic schemas
├── prompts/              # Prompt templates
├── utils/                # Shared helpers
├── tests/                # Tests
├── reports/              # Generated reports
├── .env.example
├── requirements.txt
└── README.md
```
