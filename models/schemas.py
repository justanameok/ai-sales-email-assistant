"""Pydantic schemas for email analysis and reply generation."""

from pydantic import BaseModel, Field


class EmailAnalysis(BaseModel):
    """Structured result from analyzing a customer email."""

    intent: str = Field(description="Detected customer intent")
    extracted_info: dict = Field(
        default_factory=dict, description="Key details extracted from the email"
    )
    lead_score: int = Field(ge=0, le=100, description="Lead score from 0 to 100")
    summary: str = Field(default="", description="Brief summary of the email")


class SuggestedReply(BaseModel):
    """Suggested reply to a customer email."""

    subject: str = Field(default="", description="Suggested email subject")
    body: str = Field(description="Suggested reply body")
