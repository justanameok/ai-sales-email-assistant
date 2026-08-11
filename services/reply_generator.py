"""Generate suggested sales email replies."""

import json

from models.schemas import EmailAnalysis, LeadScore, SuggestedReply
from prompts.reply_prompt import REPLY_SYSTEM_PROMPT, REPLY_USER_PROMPT
from utils.llm import MissingAPIKeyError, get_openai_client

__all__ = ["MissingAPIKeyError", "ReplyGenerationError", "generate_reply"]


class ReplyGenerationError(Exception):
    """Raised when the LLM reply generation call or parse fails."""


def generate_reply(
    email_analysis: EmailAnalysis,
    lead_score: LeadScore,
) -> SuggestedReply:
    """Generate a draft sales reply from analysis and lead score."""
    if email_analysis is None:
        raise ValueError("email_analysis is required.")
    if lead_score is None:
        raise ValueError("lead_score is required.")

    client, config = get_openai_client()
    schema = json.dumps(SuggestedReply.model_json_schema(), ensure_ascii=False, indent=2)
    user_prompt = REPLY_USER_PROMPT.format(
        email_analysis_json=email_analysis.model_dump_json(indent=2),
        lead_score_json=lead_score.model_dump_json(indent=2),
    )
    system_prompt = (
        f"{REPLY_SYSTEM_PROMPT}\n\n"
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
            temperature=0.4,
        )
    except MissingAPIKeyError:
        raise
    except Exception as exc:
        raise ReplyGenerationError(f"Failed to generate reply: {exc}") from exc

    content = completion.choices[0].message.content
    if not content:
        raise ReplyGenerationError("Model returned an empty reply.")

    try:
        return SuggestedReply.model_validate_json(content)
    except Exception as exc:
        raise ReplyGenerationError(
            f"Model returned invalid reply JSON: {exc}"
        ) from exc
