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


class SuggestedReply(BaseModel):
    """Suggested reply to a customer email."""

    subject: str = Field(default="", description="Suggested email subject")
    body: str = Field(description="Suggested reply body")
