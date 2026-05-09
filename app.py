from datetime import timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.data import add_entry, delete_entry, edit_entry, export_csv, get_all_entries, get_current_phase, get_cycle_stats, import_csv

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

    stats = get_cycle_stats()
    phase = get_current_phase()
    df = get_all_entries()

    if df.empty or stats["total_entries"] == 0:
        st.markdown(
            """
            <div style='text-align:center; padding:3rem 1rem;'>
                <h2>🌸 Welcome to HerCycleV2</h2>
                <p style='font-size:1.1rem; color:#888;'>
                    No period data yet. Head over to <strong>📝 Log Period</strong> to log your first entry!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        if phase["phase"]:
            st.markdown(
                f"""
                <div style='
                    background: linear-gradient(135deg, #FFF0F5, #FFE4EC);
                    border-radius: 1rem;
                    padding: 1.25rem 1.5rem;
                    margin-bottom: 1.5rem;
                    border-left: 5px solid #E75480;
                '>
                    <span style='font-size:2rem;'>{phase["emoji"]}</span>
                    <span style='font-size:1.4rem; font-weight:700; color:#E75480; margin-left:0.5rem;'>
                        Day {phase["day_in_cycle"]}
                    </span>
                    <span style='font-size:1.4rem; font-weight:700; color:#D43D6A; margin-left:0.5rem;'>
                        &mdash; {phase["phase"].capitalize()} Phase
                    </span>
                    <p style='margin-top:0.5rem; color:#666; font-size:0.95rem;'>
                        {phase["description"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col1, col2, col3, col4 = st.columns(4)
        avg_cycle = stats.get("avg_cycle")
        std_cycle = stats.get("std_cycle")
        with col1:
            st.metric(
                "Avg Cycle",
                f"{avg_cycle} days" if avg_cycle is not None else "—",
            )
        with col2:
            st.metric(
                "Variation",
                f"±{std_cycle} days" if std_cycle is not None else "—",
            )
        with col3:
            st.metric(
                "Next Period",
                stats.get("next_predicted", "—"),
            )
        with col4:
            st.metric(
                "Total Entries",
                stats["total_entries"],
            )

        if std_cycle and std_cycle > 7:
            st.warning(
                "Your cycles show significant variation (SD > 7 days). "
                "This may indicate irregular cycles. Consider consulting a healthcare provider "
                "if this pattern continues."
            )

        if df["start_date"].notna().sum() >= 2:
            valid = df[df["start_date"].notna()].sort_values("start_date")
            diffs = valid["start_date"].diff().dropna().dt.days

            if len(diffs) > 0:
                st.subheader("Cycle Length Trend")
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=valid["start_date"].iloc[1:],
                        y=diffs,
                        mode="lines+markers",
                        line={"color": "#E75480", "width": 2},
                        marker={"size": 8, "color": "#E75480"},
                        name="Cycle length",
                    )
                )
                if avg_cycle:
                    fig.add_hline(
                        y=avg_cycle,
                        line_dash="dash",
                        line_color="#999",
                        annotation_text=f"Avg: {avg_cycle} days",
                    )
                fig.update_layout(
                    xaxis_title="Period Start Date",
                    yaxis_title="Cycle Length (days)",
                    margin={"t": 10, "b": 40, "l": 40, "r": 10},
                    height=300,
                    hovermode="x unified",
                )
                st.plotly_chart(fig, use_container_width=True)

        if phase.get("fertile_window"):
            st.info(
                f"🌷 **Fertile window:** {phase['fertile_window']} &mdash; "
                "this is typically when ovulation occurs and conception is most likely."
            )

        pms_start = None
        if stats.get("next_predicted") and stats.get("avg_cycle"):
            next_date = pd.Timestamp(stats["next_predicted"])
            pms_start = (next_date - timedelta(days=7)).strftime("%b %d")
            pms_end = next_date.strftime("%b %d")

        if pms_start:
            st.warning(
                f"🩸 **PMS window:** {pms_start} &ndash; {pms_end} &mdash; "
                "you may experience mood swings, bloating, or fatigue as your period approaches."
            )

        st.subheader("Recent Entries")
        recent = df.head(10).copy()
        if not recent.empty:
            display_rows = []
            for _, row in recent.iterrows():
                start_str = row["start_date"].strftime("%Y-%m-%d") if pd.notna(row["start_date"]) else "-"
                end_str = row["end_date"].strftime("%Y-%m-%d") if pd.notna(row["end_date"]) else "—"
                dur = int(row["duration"]) if pd.notna(row["duration"]) else "-"
                notes_str = str(row["notes"]) if pd.notna(row["notes"]) and str(row["notes"]).strip() else "-"
                display_rows.append([start_str, end_str, f"{dur} days" if dur != "-" else "-", notes_str])

            st.dataframe(
                pd.DataFrame(display_rows, columns=["Start", "End", "Duration", "Notes"]),
                use_container_width=True,
                hide_index=True,
            )

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

    entries_df = get_all_entries()

    if "delete_id" in st.session_state:
        delete_entry(st.session_state.delete_id)
        del st.session_state.delete_id
        st.rerun()

    if entries_df.empty:
        st.info("No entries yet. Log a period to get started!")
    else:
        for _, row in entries_df.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 3, 1])

                entry_id = int(row["id"])
                start_str = row["start_date"].strftime("%Y-%m-%d") if pd.notna(row["start_date"]) else "-"
                end_str = row["end_date"].strftime("%Y-%m-%d") if pd.notna(row["end_date"]) else "Ongoing"
                duration_val = int(row["duration"]) if pd.notna(row["duration"]) else "-"
                duration_display = f"{duration_val} days" if duration_val != "-" else "-"
                notes_str = row["notes"] if pd.notna(row["notes"]) and str(row["notes"]).strip() else "-"

                with col1:
                    st.write(f"**{start_str}**")
                with col2:
                    st.write(end_str)
                with col3:
                    st.write(duration_display)
                with col4:
                    st.write(notes_str)
                with col5:
                    if st.button("🗑️", key=f"del_{entry_id}"):
                        st.session_state.delete_id = entry_id
                        st.rerun()

                st.divider()

    st.divider()
    st.subheader("Edit an Entry")

    if not entries_df.empty:
        entry_ids = [int(row["id"]) for _, row in entries_df.iterrows()]
        entry_labels = [
            f"{row['start_date'].strftime('%Y-%m-%d')} (ID: {int(row['id'])})"
            for _, row in entries_df.iterrows()
        ]

        selected_label = st.selectbox("Select entry to edit", entry_labels)
        selected_idx = entry_labels.index(selected_label)
        selected_id = entry_ids[selected_idx]
        selected_row = entries_df[entries_df["id"] == selected_id].iloc[0]

        with st.form("edit_history_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_start = st.date_input("Start date", value=selected_row["start_date"])
            with col2:
                has_end = pd.notna(selected_row["end_date"])
                new_end = st.date_input("End date (optional)", value=selected_row["end_date"] if has_end else None)

            new_notes = st.text_input("Notes", value=str(selected_row["notes"]) if pd.notna(selected_row["notes"]) else "")

            submitted = st.form_submit_button("✏️ Update Entry")

            if submitted:
                if new_end and new_end < new_start:
                    st.error("End date must be on or after the start date.")
                else:
                    edit_entry(
                        entry_id=selected_id,
                        start_date=new_start.strftime("%Y-%m-%d"),
                        end_date=new_end.strftime("%Y-%m-%d") if new_end else None,
                        notes=new_notes,
                    )
                    st.success(f"Entry {selected_id} updated!")
                    st.rerun()

elif page == "💾 Export/Backup":
    st.title("💾 Export/Backup")

    all_entries = get_all_entries()
    st.metric("Total Entries", len(all_entries))

    st.divider()
    st.subheader("Export Data")
    csv_path = export_csv()
    with open(csv_path, "r") as f:
        csv_data = f.read()
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="hercyclev2_backup.csv",
        mime="text/csv",
    )

    st.divider()
    st.subheader("Import Data")
    uploaded = st.file_uploader("Choose a CSV backup file", type=["csv"])
    if uploaded is not None:
        try:
            imported_count = import_csv(uploaded)
            st.success(f"Successfully imported {imported_count} entries!")
            st.rerun()
        except Exception as e:
            st.error(f"Import failed: {e}")
