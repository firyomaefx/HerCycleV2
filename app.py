import streamlit as st
from utils.data import add_entry

st.set_page_config(
    page_title="HerCycleV2",
    page_icon="🌸",
    layout="wide",
)

st.markdown(
    """
<style>
    :root {
        --primary-color: #E75480;
        --background-color: #FFF8F0;
        --secondary-background-color: #FFF0F5;
    }
    .stApp {
        background-color: #FFF8F0;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFF0F5;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #E75480;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-size: 1.5rem;
        font-weight: 700;
        color: #E75480;
    }
    .stButton > button {
        background-color: #E75480;
        color: white;
        border: none;
        border-radius: 1rem;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    .stButton > button:hover {
        background-color: #D43D6A;
        transform: scale(1.02);
    }
    .stButton > button:active {
        background-color: #C02A58;
    }
    [data-testid="stFormSubmitButton"] > button {
        background-color: #E75480;
        color: white;
        border: none;
        border-radius: 1rem;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        width: 100%;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #D43D6A;
        transform: scale(1.02);
    }
    [data-testid="stFormSubmitButton"] > button:active {
        background-color: #C02A58;
    }
    [data-testid="stDateInput"] input {
        border-radius: 0.75rem;
        border: 2px solid #F8C8D8;
    }
    [data-testid="stDateInput"] input:focus {
        border-color: #E75480;
        box-shadow: 0 0 0 2px rgba(231, 84, 128, 0.25);
    }
    [data-testid="stTextInput"] input {
        border-radius: 0.75rem;
        border: 2px solid #F8C8D8;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #E75480;
        box-shadow: 0 0 0 2px rgba(231, 84, 128, 0.25);
    }
    h1 {
        color: #E75480;
    }
    h2, h3 {
        color: #D43D6A;
    }
    .stSuccess {
        background-color: #FFF0F5;
        border-left: 4px solid #E75480;
    }
    .stError {
        background-color: #FFF0F0;
        border-left: 4px solid #E75480;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("# 🌸 HerCycleV2")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📝 Log Period", "📋 Edit History", "💾 Export/Backup"],
    label_visibility="collapsed",
)

if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.info("🚧 Coming soon! Track your cycle stats, phase insights, and predictions here.")

elif page == "📝 Log Period":
    st.title("📝 Log Period")

    with st.form("log_period_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date")
        with col2:
            end_date = st.date_input("End date (optional)", value=None)

        notes = st.text_input(
            "Notes",
            placeholder="Cramps, mood, etc.",
        )

        submitted = st.form_submit_button("💾 Save Entry", type="primary")

        if submitted:
            if end_date and end_date < start_date:
                st.error("End date must be on or after the start date.")
            else:
                entry = add_entry(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d") if end_date else None,
                    notes=notes,
                )
                nice_date = start_date.strftime("%B %d, %Y")
                st.success(f"Period logged for {nice_date}!")
                st.rerun()

elif page == "📋 Edit History":
    st.title("📋 Edit History")
    st.info("🚧 Coming soon! View and edit your past cycle entries here.")

elif page == "💾 Export/Backup":
    st.title("💾 Export/Backup")
    st.info("🚧 Coming soon! Export your data to CSV or import from a backup file.")
