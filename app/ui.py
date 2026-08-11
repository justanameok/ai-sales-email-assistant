import sys
from pathlib import Path

import streamlit as st

# Allow imports from project root when running via `streamlit run app/ui.py`
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.email_analyzer import (  # noqa: E402
    EmailAnalysisError,
    MissingAPIKeyError,
    analyze_email,
)
from services.lead_scorer import LeadScoringError, score_lead  # noqa: E402
from services.reply_generator import ReplyGenerationError, generate_reply  # noqa: E402


def _render_bullet_list(items: list, empty_label: str = "None identified") -> None:
    if items:
        for item in items:
            st.write(f"- {item}")
    else:
        st.write(empty_label)


st.set_page_config(page_title="AI Sales Email Assistant", layout="centered")

st.title("AI Sales Email Assistant")
st.write(
    "Paste a customer email below to analyze intent, score the lead, "
    "and generate a suggested sales reply draft."
)

customer_email = st.text_area(
    "Customer email",
    height=200,
    placeholder="Paste the customer email here...",
)

if st.button("Analyze", type="primary"):
    if not customer_email.strip():
        st.warning("Please paste a customer email before analyzing.")
    else:
        try:
            with st.spinner("Analyzing email..."):
                analysis = analyze_email(customer_email)

            with st.spinner("Scoring lead..."):
                lead_score = score_lead(analysis)

            with st.spinner("Generating reply draft..."):
                reply = generate_reply(analysis, lead_score)

            st.subheader("Analysis results")

            st.markdown("**Customer Intent**")
            st.write(analysis.customer_intent)

            st.markdown("**Product Interest**")
            st.write(analysis.product_interest)

            st.markdown("**Quantity**")
            st.write(analysis.quantity or "Not specified")

            st.markdown("**Urgency**")
            st.write(analysis.urgency)

            st.markdown("**Missing Information**")
            _render_bullet_list(analysis.missing_information)

            st.markdown("**Recommended Actions**")
            _render_bullet_list(analysis.recommended_action)

            st.subheader("Lead Score")

            st.markdown("**Lead Score**")
            st.write(f"{lead_score.score}/100")

            st.markdown("**Priority**")
            st.write(lead_score.priority.upper())

            st.markdown("**Reasoning**")
            _render_bullet_list(lead_score.reasoning)

            st.markdown("**Recommended Next Steps**")
            _render_bullet_list(lead_score.recommended_next_step)

            st.subheader("Suggested Reply")

            st.markdown("**Subject**")
            st.write(reply.subject)

            st.markdown("**Email Body**")
            st.text(reply.email_body)

            st.markdown("**Key Points**")
            _render_bullet_list(reply.key_points)

        except MissingAPIKeyError as exc:
            st.error(str(exc))
        except EmailAnalysisError as exc:
            st.error(f"Analysis failed: {exc}")
        except LeadScoringError as exc:
            st.error(f"Lead scoring failed: {exc}")
        except ReplyGenerationError as exc:
            st.error(f"Reply generation failed: {exc}")
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
