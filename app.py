from datetime import timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.data import add_entry, delete_entry, edit_entry, export_csv, get_all_entries, get_current_phase, get_cycle_stats, import_csv

st.set_page_config(
    page_title="HerCycleV2",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Modern CSS Design System ───────────────────────────────────────────────
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    /* ── Reset & Base ────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4EC 30%, #F0E6FF 60%, #FFF8F0 100%) !important;
        min-height: 100vh;
        animation: fadeIn 0.6s ease-out;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ── Custom Scrollbar ────────────────────────────────── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #FFF0F5; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #E75480, #D43D6A); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #D43D6A, #C02A58); }

    /* ── Typography ──────────────────────────────────────── */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #D43D6A !important;
        letter-spacing: -0.02em;
    }
    h1 { font-weight: 700 !important; }
    h2 { font-weight: 600 !important; }
    h3 { font-weight: 600 !important; }
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Glassmorphism Cards ─────────────────────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.35) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(231, 84, 128, 0.12) !important;
        padding: 24px !important;
        margin-bottom: 16px !important;
        transition: all 0.3s ease !important;
    }
    .glass-card:hover {
        box-shadow: 0 12px 40px rgba(231, 84, 128, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Sidebar ─────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2D1B33 0%, #4A2040 100%) !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8E0EC !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #FFB6C1 !important;
        text-shadow: 0 2px 8px rgba(231,84,128,0.3);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #F8E0EC !important;
        font-weight: 500 !important;
        padding: 10px 16px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(231, 84, 128, 0.3) !important;
        color: #fff !important;
    }
    section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, #E75480, #D43D6A) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(231, 84, 128, 0.5) !important;
    }

    /* ── Buttons ─────────────────────────────────────────── */
    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #E75480, #D43D6A) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(231, 84, 128, 0.4) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #D43D6A, #C02A58) !important;
        transform: scale(1.03) !important;
        box-shadow: 0 6px 20px rgba(231, 84, 128, 0.5) !important;
    }
    .stButton > button:active, [data-testid="stFormSubmitButton"] > button:active {
        background: linear-gradient(135deg, #C02A58, #A8204A) !important;
        transform: scale(0.98) !important;
        box-shadow: 0 2px 10px rgba(231, 84, 128, 0.3) !important;
    }

    /* ── Input Fields ────────────────────────────────────── */
    [data-testid="stDateInput"] input, [data-testid="stTextInput"] input, .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.6) !important;
        border-radius: 12px !important;
        border: 2px solid #F8C8D8 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stDateInput"] input:focus, [data-testid="stTextInput"] input:focus {
        border-color: #E75480 !important;
        box-shadow: 0 0 0 3px rgba(231, 84, 128, 0.2) !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }

    /* ── Metrics ─────────────────────────────────────────── */
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #E75480 !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #888 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.35) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(231, 84, 128, 0.1) !important;
        border-left: 4px solid #E75480 !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 8px 30px rgba(231, 84, 128, 0.18) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Alerts ──────────────────────────────────────────── */
    .stSuccess {
        background: linear-gradient(135deg, rgba(255,240,245,0.9), rgba(255,228,236,0.9)) !important;
        border-left: 5px solid #E75480 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(231,84,128,0.1) !important;
    }
    .stError {
        background: linear-gradient(135deg, rgba(255,240,240,0.9), rgba(255,220,220,0.9)) !important;
        border-left: 5px solid #D43D6A !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    .stWarning {
        background: linear-gradient(135deg, rgba(255,248,220,0.9), rgba(255,240,200,0.9)) !important;
        border-left: 5px solid #E7A854 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    .stInfo {
        background: linear-gradient(135deg, rgba(232,245,255,0.9), rgba(220,240,255,0.9)) !important;
        border-left: 5px solid #5B9BD5 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ── Dataframe ───────────────────────────────────────── */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ── Dividers ────────────────────────────────────────── */
    hr {
        border-color: rgba(231, 84, 128, 0.2) !important;
    }

    /* ── Phase Badge ─────────────────────────────────────── */
    .phase-badge {
        background: linear-gradient(135deg, rgba(255,240,245,0.95), rgba(255,228,236,0.95)) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;
        padding: 1.5rem 2rem !important;
        margin-bottom: 1.5rem !important;
        border-left: 6px solid #E75480 !important;
        box-shadow: 0 8px 32px rgba(231,84,128,0.15) !important;
        animation: fadeIn 0.5s ease-out !important;
    }

    /* ── Welcome Card ────────────────────────────────────── */
    .welcome-card {
        text-align: center !important;
        padding: 4rem 2rem !important;
        background: rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        box-shadow: 0 12px 40px rgba(231,84,128,0.12) !important;
    }

    /* ── Download Button ──────────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #E75480, #D43D6A) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(231,84,128,0.4) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ─── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.markdown("# 🌸 HerCycleV2")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📝 Log Period", "📋 Edit History", "💾 Export/Backup"],
    label_visibility="collapsed",
)

# ─── Dashboard ──────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")

    stats = get_cycle_stats()
    phase = get_current_phase()
    df = get_all_entries()

    if df.empty or stats["total_entries"] == 0:
        st.markdown(
            """
            <div class="welcome-card">
                <h2 style="font-family:'Playfair Display',serif; color:#D43D6A; margin-bottom:0.5rem;">🌸 Welcome to HerCycleV2</h2>
                <p style="font-size:1.1rem; color:#888; font-family:'Inter',sans-serif;">
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
                <div class="phase-badge">
                    <span style='font-size:2.5rem;'>{phase["emoji"]}</span>
                    <span style='font-family:"Playfair Display",serif; font-size:1.5rem; font-weight:700; color:#E75480; margin-left:0.5rem;'>
                        Day {phase["day_in_cycle"]}
                    </span>
                    <span style='font-family:"Playfair Display",serif; font-size:1.5rem; font-weight:700; color:#D43D6A; margin-left:0.5rem;'>
                        &mdash; {phase["phase"].capitalize()} Phase
                    </span>
                    <p style='margin-top:0.5rem; color:#666; font-size:0.95rem; font-family:"Inter",sans-serif;'>
                        {phase["description"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if phase["phase"] and stats.get("avg_cycle"):
                day = phase["day_in_cycle"]
                pct = min(day / stats["avg_cycle"], 1.0)
                radius = 48
                circumference = 2 * 3.14159265 * radius
                offset = circumference * (1 - pct)
                st.markdown(f"""
                <div style="display:flex; justify-content:center; margin-bottom:1.5rem;">
                    <svg width="120" height="120" viewBox="0 0 120 120" style="transform:rotate(-90deg);">
                        <circle cx="60" cy="60" r="{radius}" stroke="#F8C8D8" stroke-width="8" fill="none"/>
                        <circle cx="60" cy="60" r="{radius}" stroke="#E75480" stroke-width="8" fill="none"
                            stroke-linecap="round"
                            stroke-dasharray="{circumference}"
                            stroke-dashoffset="{offset}">
                            <animate attributeName="stroke-dashoffset" from="{circumference}" to="{offset}" dur="1s" fill="freeze"/>
                        </circle>
                        <text x="60" y="64" text-anchor="middle" dominant-baseline="middle"
                            font-family="Playfair Display, serif" font-size="28" font-weight="700"
                            fill="#E75480" transform="rotate(90, 60, 60)">
                            {day}
                        </text>
                    </svg>
                </div>
                """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        avg_cycle = stats.get("avg_cycle")
        std_cycle = stats.get("std_cycle")
        with col1:
            st.metric("🩸 Avg Cycle", f"{avg_cycle} days" if avg_cycle is not None else "—")
        with col2:
            st.metric("📊 Variation", f"±{std_cycle} days" if std_cycle is not None else "—")
        with col3:
            st.metric("📅 Next Period", stats.get("next_predicted", "—"))
        with col4:
            st.metric("📋 Entries", stats["total_entries"])

        if std_cycle and std_cycle > 7:
            st.warning(
                "⚠️ Your cycles show significant variation (SD > 7 days). "
                "This may indicate irregular cycles. Consider consulting a healthcare provider "
                "if this pattern continues."
            )

        if df["start_date"].notna().sum() >= 2:
            valid = df[df["start_date"].notna()].sort_values("start_date")
            diffs = valid["start_date"].diff().dropna().dt.days

            if len(diffs) > 0:
                st.subheader("📈 Cycle Length Trend")
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=valid["start_date"].iloc[1:],
                        y=diffs,
                        mode="lines+markers",
                        line={"color": "#E75480", "width": 2.5},
                        marker={"size": 9, "color": "#E75480", "line": {"width": 2, "color": "white"}},
                        fill="tozeroy",
                        fillcolor="rgba(231,84,128,0.08)",
                        name="Cycle length",
                    )
                )
                if avg_cycle:
                    fig.add_hline(
                        y=avg_cycle,
                        line_dash="dash",
                        line_color="#D43D6A",
                        line_width=1.5,
                        annotation_text=f"Avg: {avg_cycle} days",
                        annotation_font_color="#D43D6A",
                        annotation_font_family="Inter",
                    )
                fig.update_layout(
                    xaxis_title="Period Start Date",
                    yaxis_title="Cycle Length (days)",
                    margin={"t": 10, "b": 40, "l": 40, "r": 10},
                    height=320,
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_family="Inter",
                    xaxis=dict(gridcolor="rgba(231,84,128,0.1)"),
                    yaxis=dict(gridcolor="rgba(231,84,128,0.1)"),
                )
                st.plotly_chart(fig, use_container_width=True)

        if phase.get("fertile_window"):
            st.info(
                f"🌷 **Fertile window:** {phase['fertile_window']} — "
                "this is typically when ovulation occurs and conception is most likely."
            )

        pms_start = None
        if stats.get("next_predicted") and stats.get("avg_cycle"):
            next_date = pd.Timestamp(stats["next_predicted"])
            pms_start = (next_date - timedelta(days=7)).strftime("%b %d")
            pms_end = next_date.strftime("%b %d")

        if pms_start:
            st.warning(
                f"🩸 **PMS window:** {pms_start} – {pms_end} — "
                "you may experience mood swings, bloating, or fatigue as your period approaches."
            )

        st.subheader("📋 Recent Entries")
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

# ─── Log Period ─────────────────────────────────────────────────────────────
elif page == "📝 Log Period":
    st.title("📝 Log Period")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
                st.success(f"✨ Period logged for {nice_date}!")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Edit History ────────────────────────────────────────────────────────────
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
            entry_id = int(row["id"])
            start_str = row["start_date"].strftime("%Y-%m-%d") if pd.notna(row["start_date"]) else "-"
            end_str = row["end_date"].strftime("%Y-%m-%d") if pd.notna(row["end_date"]) else "Ongoing"
            duration_val = int(row["duration"]) if pd.notna(row["duration"]) else "-"
            duration_display = f"{duration_val} days" if duration_val != "-" else "-"
            notes_str = row["notes"] if pd.notna(row["notes"]) and str(row["notes"]).strip() else "-"

            st.markdown(
                f"""
                <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center; padding:12px 20px;">
                    <div style="flex:1;">
                        <strong style="font-family:'Inter',sans-serif; color:#D43D6A; font-size:1rem;">{start_str}</strong>
                        <span style="color:#888; margin-left:8px;">→ {end_str}</span>
                        <span style="background:linear-gradient(135deg,#E75480,#D43D6A); color:white; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin-left:8px;">{duration_display}</span>
                        <span style="color:#999; margin-left:12px; font-size:0.85rem;">{notes_str}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🗑️ Delete", key=f"del_{entry_id}"):
                st.session_state.delete_id = entry_id
                st.rerun()

    st.markdown("---")
    st.subheader("✏️ Edit an Entry")

    if not entries_df.empty:
        entry_ids = [int(row["id"]) for _, row in entries_df.iterrows()]
        entry_labels = [
            f"{row['start_date'].strftime('%Y-%m-%d')} (ID: {int(row['id'])})"
            for _, row in entries_df.iterrows()
        ]

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
                    st.success(f"✨ Entry {selected_id} updated!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Export/Backup ───────────────────────────────────────────────────────────
elif page == "💾 Export/Backup":
    st.title("💾 Export/Backup")

    all_entries = get_all_entries()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.metric("📋 Total Entries", len(all_entries))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📥 Export Data")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    csv_path = export_csv()
    with open(csv_path, "r") as f:
        csv_data = f.read()
    st.download_button(
        label="📥 Download CSV Backup",
        data=csv_data,
        file_name="hercyclev2_backup.csv",
        mime="text/csv",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📤 Import Data")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a CSV backup file", type=["csv"])
    if uploaded is not None:
        try:
            imported_count = import_csv(uploaded)
            st.success(f"✨ Successfully imported {imported_count} entries!")
            st.rerun()
        except Exception as e:
            st.error(f"Import failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)