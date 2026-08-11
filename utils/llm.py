"""Shared OpenAI-compatible LLM client configuration."""

import os
from dataclasses import dataclass
from typing import Optional, Tuple

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class MissingAPIKeyError(Exception):
    """Raised when LLM_API_KEY is not configured."""


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: Optional[str]
    model: str


def get_llm_config() -> LLMConfig:
    """Load LLM settings from environment.

    Works with any OpenAI-compatible provider by changing .env only:
    - LLM_API_KEY
    - LLM_BASE_URL (optional; omit for official OpenAI)
    - LLM_MODEL
    """
    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key:
        raise MissingAPIKeyError(
            "LLM_API_KEY is missing. Copy .env.example to .env and set "
            "LLM_API_KEY, LLM_BASE_URL, and LLM_MODEL."
        )

    base_url = os.getenv("LLM_BASE_URL", "").strip() or None
    model = os.getenv("LLM_MODEL", "").strip()
    if not model:
        raise MissingAPIKeyError(
            "LLM_MODEL is missing. Set LLM_MODEL in .env (e.g. deepseek-chat)."
        )

    return LLMConfig(api_key=api_key, base_url=base_url, model=model)


def get_openai_client() -> Tuple[OpenAI, LLMConfig]:
    """Create an OpenAI-compatible client from config."""
    config = get_llm_config()
    client_kwargs = {"api_key": config.api_key}
    if config.base_url:
        client_kwargs["base_url"] = config.base_url
    return OpenAI(**client_kwargs), config
