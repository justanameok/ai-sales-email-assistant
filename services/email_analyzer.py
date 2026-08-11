"""Analyze customer emails for intent, structured data, and next actions."""

import json

from models.schemas import EmailAnalysis
from prompts.email_analysis_prompt import (
    EMAIL_ANALYSIS_SYSTEM_PROMPT,
    EMAIL_ANALYSIS_USER_PROMPT,
)
from utils.llm import MissingAPIKeyError, get_openai_client

# Re-export so the UI can keep importing from this module.
__all__ = ["MissingAPIKeyError", "EmailAnalysisError", "analyze_email"]


class EmailAnalysisError(Exception):
    """Raised when the LLM analysis call or parse fails."""


def analyze_email(email_text: str) -> EmailAnalysis:
    """Send a customer email to the LLM and return structured analysis."""
    if not email_text or not email_text.strip():
        raise ValueError("Email text is empty.")

    client, config = get_openai_client()
    schema = json.dumps(EmailAnalysis.model_json_schema(), ensure_ascii=False, indent=2)
    user_prompt = EMAIL_ANALYSIS_USER_PROMPT.format(email_text=email_text.strip())
    system_prompt = (
        f"{EMAIL_ANALYSIS_SYSTEM_PROMPT}\n\n"
        "Respond with a single JSON object that matches this schema:\n"
        f"{schema}"
    )

    try:
        completion = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
    except MissingAPIKeyError:
        raise
    except Exception as exc:
        raise EmailAnalysisError(f"Failed to analyze email: {exc}") from exc

    content = completion.choices[0].message.content
    if not content:
        raise EmailAnalysisError("Model returned an empty analysis.")

    try:
        return EmailAnalysis.model_validate_json(content)
    except Exception as exc:
        raise EmailAnalysisError(
            f"Model returned invalid analysis JSON: {exc}"
        ) from exc
