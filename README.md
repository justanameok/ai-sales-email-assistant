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

Add your OpenAI API key to `.env`:

```
OPENAI_API_KEY=your_key_here
```

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
