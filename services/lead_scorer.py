"""Score sales lead quality from structured email analysis."""

import json

from models.schemas import EmailAnalysis, LeadScore
from prompts.lead_scoring_prompt import (
    LEAD_SCORING_SYSTEM_PROMPT,
    LEAD_SCORING_USER_PROMPT,
)
from utils.llm import MissingAPIKeyError, get_openai_client

__all__ = ["MissingAPIKeyError", "LeadScoringError", "score_lead"]


class LeadScoringError(Exception):
    """Raised when the LLM lead scoring call or parse fails."""


def score_lead(email_analysis: EmailAnalysis) -> LeadScore:
    """Score a sales lead from EmailAnalysis and return LeadScore."""
    if email_analysis is None:
        raise ValueError("email_analysis is required.")

    client, config = get_openai_client()
    schema = json.dumps(LeadScore.model_json_schema(), ensure_ascii=False, indent=2)
    analysis_json = email_analysis.model_dump_json(indent=2)
    user_prompt = LEAD_SCORING_USER_PROMPT.format(email_analysis_json=analysis_json)
    system_prompt = (
        f"{LEAD_SCORING_SYSTEM_PROMPT}\n\n"
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
        raise LeadScoringError(f"Failed to score lead: {exc}") from exc

    content = completion.choices[0].message.content
    if not content:
        raise LeadScoringError("Model returned an empty lead score.")

    try:
        return LeadScore.model_validate_json(content)
    except Exception as exc:
        raise LeadScoringError(f"Model returned invalid lead score JSON: {exc}") from exc
