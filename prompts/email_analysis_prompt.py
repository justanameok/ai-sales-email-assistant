"""Prompt templates for customer email analysis."""

EMAIL_ANALYSIS_PROMPT = """
You are a sales email analyst. Analyze the customer email below.

Extract:
1. Customer intent
2. Key structured information (name, company, product interest, timeline, budget if mentioned)
3. A lead score from 0 to 100
4. A brief summary

Customer email:
{email_text}
""".strip()
