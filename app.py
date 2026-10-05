import streamlit as st

from IT_Ticket_Classifier import analyze_ticket


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="IT Support AI",
    page_icon="🛠️",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.html("""
<style>
.card {
    background: #1e2129;
    border: 1px solid #2d313a;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    min-height: 155px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-icon {
    font-size: 30px;
    margin-bottom: 10px;
}

.card-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #aeb4c0;
    margin-bottom: 10px;
}

.card-value {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
}

.card-subtitle {
    font-size: 12px;
    color: #89909d;
    margin-top: 8px;
}
</style>
""")

# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.title("🛠️ IT Support AI")

    st.markdown("---")

    st.subheader("System Status")

    st.success("🟢 Jev AI Connected")

    st.markdown("---")

    st.subheader("About the Product")

    st.write(
    """
    **AI-Powered IT Support Ticket Analyzer**

    This application uses **Jev AI** to classify IT support tickets,
    assess their urgency, and provide confidence and probability
    insights for faster and more consistent support triage.

    **Developed by:**  
    [Dhanushka Gunasinghe](https://www.linkedin.com/in/dhanushka-gunasinghe/)
    """
)

    st.markdown("---")

    st.caption("Jev AI and Streamlit")


# =========================================================
# Header
# =========================================================

st.html("""
<style>

.main-title {
    padding: 10px 0 18px 0;
}

.main-title h1 {
    margin: 0;

    font-size: 36px;

    font-weight: 800;

    color: #f8fafc;

    letter-spacing: -0.8px;
}

.title-accent {
    width: 70px;

    height: 4px;

    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    );

    border-radius: 10px;

    margin: 12px 0;
}

.main-title p {
    margin: 0;

    color: #94a3b8;

    font-size: 15px;
}

</style>

<div class="main-title">

    <h1>🛠️ IT Support Ticket Analyzer</h1>

    <div class="title-accent"></div>

    <p>
        Intelligent ticket classification and urgency assessment powered by Jev AI
    </p>

</div>
""")


# =========================================================
# Ticket Input
# =========================================================

st.subheader("🎫 Support Ticket")

sample_ticket = st.text_area(
    "Describe the user's problem:",
    value="Unable to log in to my company account.",
    height=150,
    placeholder=(
        "Example: My laptop cannot connect to "
        "the company VPN."
    )
)


# =========================================================
# Analyse Button
# =========================================================

analyse = st.button(
    "🔍 Analyse Ticket",
    type="primary",
    use_container_width=True
)


# =========================================================
# Analyse
# =========================================================

if analyse:

    if not sample_ticket.strip():

        st.warning(
            "Please enter an IT support ticket."
        )

    else:

        try:

            with st.spinner(
                "🤖 Jev is analysing the ticket..."
            ):

                result = analyze_ticket(
                    sample_ticket
                )


            # =================================================
            # Get results
            # =================================================

            category = result["category"]

            category_confidence = (
                result["category_confidence"]
            )

            category_probabilities = (
                result["category_probabilities"]
            )

            urgency_score = (
                result["urgency_score"]
            )

            urgency_label = (
                result["urgency_label"]
            )

            urgency_confidence = (
                result["urgency_confidence"]
            )

            urgency_probabilities = (
                result["urgency_probabilities"]
            )


            # =================================================
            # Success
            # =================================================

            st.success(
                "✅ Analysis completed!"
            )

            st.markdown("---")

            st.subheader(
                "📊 Analysis Results"
            )


            # =================================================
            # Result Cards
            # =================================================

            col1, col2, col3 = st.columns(3)


            # Category
            with col1:

                    st.html(f"""
                    <div class="card">
                        <div class="card-icon">📂</div>
                        <div class="card-title">Issue Category</div>
                        <div class="card-value">{category.title()}</div>
                        <div class="card-subtitle">AI Classification</div>
                    </div>
                    """)




            # Urgency
            with col2:

                    st.html(f"""
                    <div class="card">
                        <div class="card-icon">🚨</div>
                        <div class="card-title">Urgency</div>
                        <div class="card-value">{urgency_label}</div>
                        <div class="card-subtitle">Priority Assessment</div>
                    </div>
                    """)
            # Confidence
            with col3:
                        st.html(f"""
            <div class="card">
                <div class="card-icon">🎯</div>
                <div class="card-title">Category Confidence</div>
                <div class="card-value">{category_confidence:.1%}</div>
                <div class="card-subtitle">Classification Confidence</div>
            </div>
            """)
            # =================================================
            # Submitted Ticket
            # =================================================

            st.subheader(
                "🎫 Submitted Ticket"
            )

            st.markdown(
    f"""
    <div class="ticket-box">
        {sample_ticket}
    </div>
    """,
    unsafe_allow_html=True
)


            # =================================================
            # Probability Charts
            # =================================================

            col1, col2 = st.columns(2)


            # Category probabilities
            with col1:

                st.subheader(
                    "📂 Category Probabilities"
                )

                st.bar_chart(
                    category_probabilities
                )


            # Urgency probabilities
            with col2:

                st.subheader(
                    "🚨 Urgency Probabilities"
                )

                urgency_levels = [
                    "Low",
                    "Medium",
                    "High",
                    "Critical"
                ]

                urgency_chart = {}

                for level, probability in (
                    urgency_probabilities.items()
                ):

                    label = urgency_levels[
                        int(level)
                    ]

                    urgency_chart[label] = (
                        probability
                    )

                st.bar_chart(
                    urgency_chart
                )


            # =================================================
            # Urgency Score
            # =================================================

            st.markdown("---")

            st.subheader(
                "📈 Urgency Score"
            )

            st.metric(
                "Probability-weighted score",
                f"{urgency_score:.2f}"
            )

            st.progress(
                min(
                    max(
                        urgency_score / 3,
                        0
                    ),
                    1
                )
            )

            st.caption(
                "0 = Low | 1 = Medium | "
                "2 = High | 3 = Critical"
            )


            # =================================================
            # Confidence
            # =================================================

            st.markdown("---")

            st.subheader(
                "🎯 Confidence"
            )

            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    "Category confidence"
                )

                st.progress(
                    category_confidence
                )

                st.write(
                    f"{category_confidence:.2%}"
                )


            with col2:

                st.write(
                    "Urgency confidence"
                )

                st.progress(
                    urgency_confidence
                )

                st.write(
                    f"{urgency_confidence:.2%}"
                )


            # =================================================
            # Technical Details
            # =================================================

            with st.expander(
                "🔧 Technical Details"
            ):

                st.write(
                    "Category probabilities"
                )

                st.json(
                    category_probabilities
                )

                st.write(
                    "Urgency probabilities"
                )

                st.json(
                    urgency_probabilities
                )

                st.write(
                    "Urgency score"
                )

                st.write(
                    urgency_score
                )


            # =================================================
            # Complete Result
            # =================================================

            with st.expander(
                "📋 Complete Analysis Result"
            ):

                st.json(
                    result
                )


        except Exception as e:

            st.error(
                f"❌ Error analysing ticket: {e}"
            )