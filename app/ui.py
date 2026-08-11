import streamlit as st

st.set_page_config(page_title="AI Sales Email Assistant", layout="centered")

st.title("AI Sales Email Assistant")
st.write(
    "Paste a customer email below to analyze intent, extract key details, "
    "score the lead, and generate a suggested reply."
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
        st.subheader("Analysis results")
        st.info("Placeholder — AI analysis not implemented yet.")

        st.markdown("**Intent**")
        st.write("—")

        st.markdown("**Extracted information**")
        st.write("—")

        st.markdown("**Lead score**")
        st.write("—")

        st.markdown("**Suggested reply**")
        st.write("—")
