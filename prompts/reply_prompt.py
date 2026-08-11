"""Prompt templates for suggested sales replies."""

REPLY_PROMPT = """
You are a professional sales assistant. Draft a concise, helpful reply
based on the customer email and analysis below.

Customer email:
{email_text}

Analysis:
{analysis}

Write a polite reply that addresses the customer's intent and next steps.
""".strip()
