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

st.set_page_config(page_title="AI Sales Email Assistant", layout="centered")

st.title("AI Sales Email Assistant")
st.write(
    "Paste a customer email below to analyze intent, extract key details, "
    "and get recommended next sales actions."
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
            if analysis.missing_information:
                for item in analysis.missing_information:
                    st.write(f"- {item}")
            else:
                st.write("None identified")

            st.markdown("**Recommended Actions**")
            if analysis.recommended_action:
                for item in analysis.recommended_action:
                    st.write(f"- {item}")
            else:
                st.write("None identified")

        except MissingAPIKeyError as exc:
            st.error(str(exc))
        except EmailAnalysisError as exc:
            st.error(f"Analysis failed: {exc}")
        except Exception as exc:
            st.error(f"Unexpected error while analyzing the email: {exc}")
