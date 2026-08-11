"""Pydantic schemas for email analysis and reply generation."""

from typing import Optional

from pydantic import BaseModel, Field


class EmailAnalysis(BaseModel):
    """Structured result from analyzing a customer sales email."""

    customer_company: Optional[str] = Field(
        default=None, description="Customer company name if mentioned"
    )
    customer_name: Optional[str] = Field(
        default=None, description="Customer contact name if mentioned"
    )
    customer_country: Optional[str] = Field(
        default=None, description="Customer country or region if mentioned"
    )
    customer_intent: str = Field(description="Primary customer intent")
    product_interest: str = Field(description="Product or service the customer is interested in")
    quantity: Optional[str] = Field(
        default=None, description="Requested quantity or volume if mentioned"
    )
    urgency: str = Field(description="Urgency level, e.g. low, medium, high")
    missing_information: list[str] = Field(
        default_factory=list,
        description="Information still needed to move the deal forward",
    )
    recommended_action: list[str] = Field(
        default_factory=list,
        description="Recommended next sales actions",
    )


class LeadScore(BaseModel):
    """Sales opportunity quality score derived from EmailAnalysis."""

    score: int = Field(ge=0, le=100, description="Lead score from 0 to 100")
    priority: str = Field(description="Lead priority: HIGH, MEDIUM, or LOW")
    reasoning: list[str] = Field(
        default_factory=list,
        description="Reasons explaining the score and priority",
    )
    recommended_next_step: list[str] = Field(
        default_factory=list,
        description="Recommended next steps for the sales team",
    )


class SuggestedReply(BaseModel):
    """Suggested draft reply to a customer email."""

    subject: str = Field(description="Suggested email subject line")
    email_body: str = Field(description="Full suggested reply email body")
    tone: str = Field(description="Tone of the reply, e.g. professional, consultative")
    key_points: list[str] = Field(
        default_factory=list,
        description="Key points covered in the reply",
    )
