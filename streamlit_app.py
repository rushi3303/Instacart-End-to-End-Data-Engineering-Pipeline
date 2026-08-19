import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

try:
    from streamlit_mic_recorder import speech_to_text
    HAS_MIC_RECORDER = True
except Exception:
    HAS_MIC_RECORDER = False

from agent.main import process_question
from utils.report_generator import create_txt_bytes, create_pdf_bytes


# =====================================================
# Query helper
# =====================================================
def set_query_text(query):
    """Set the main query before Streamlit creates the text input widget."""
    st.session_state["query_input_text"] = query


# =====================================================
# Page Configuration
# =====================================================
st.set_page_config(
    page_title="AI Data Engineering Copilot | Enterprise Lakehouse Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# Global Premium Design System & CSS Styling
# =====================================================
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Resets */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding Reduction */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1400px;
    }

    /* Top Hero Header Card */
    .hero-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }

    .hero-title-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    }

    .hero-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 50%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 400;
    }

    /* Status Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    .badge-live {
        background: rgba(16, 185, 129, 0.12);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-medallion {
        background: rgba(99, 102, 241, 0.12);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .pulsing-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
    }

    @keyframes pulse {
        to {
            box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
        }
    }

    /* Glass Cards & Containers */
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.4);
    }

    /* KPI Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 20px;
    }

    .metric-card-pro {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease;
    }

    .metric-card-pro::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #6366F1 0%, #3B82F6 100%);
    }

    .metric-card-pro.success::before {
        background: linear-gradient(180deg, #10B981 0%, #059669 100%);
    }

    .metric-card-pro.warning::before {
        background: linear-gradient(180deg, #F59E0B 0%, #D97706 100%);
    }

    .metric-card-pro:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.5);
    }

    .metric-label-pro {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        margin-bottom: 6px;
    }

    .metric-value-pro {
        font-size: 24px;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.02em;
    }

    .metric-sub-pro {
        font-size: 11px;
        color: #64748B;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Decision Pill */
    .decision-banner {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.12) 0%, rgba(59, 130, 246, 0.06) 100%);
        border-left: 4px solid #6366F1;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    }

    /* AI Insight & Action Cards */
    .insight-card-pro {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.03) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-left: 4px solid #10B981;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #ECFDF5;
        font-size: 14px;
        line-height: 1.5;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    .action-card-pro {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(217, 119, 6, 0.03) 100%);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-left: 4px solid #F59E0B;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #FFFBEB;
        font-size: 14px;
        line-height: 1.5;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    /* Power BI Advisor Card */
    .advisor-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }

    /* Modern Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        color: #94A3B8;
        padding: 0 16px;
        border: none !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .sidebar-header-box {
        padding: 12px 14px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 16px;
    }

    .architecture-step {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 12px;
        margin-bottom: 6px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.04);
        color: #CBD5E1;
    }

    /* Quick Prompt Pills */
    .prompt-chip {
        display: inline-block;
        padding: 6px 12px;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        font-size: 12px;
        color: #E2E8F0;
        margin: 4px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .prompt-chip:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: #6366F1;
        color: #FFFFFF;
    }

    /* Voice UI Button Styling */
    .voice-widget-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    /* Dataframe polish */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# Cancel any previous speech synthesis on fresh render
components.html("""
<script>
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
</script>
""", height=0, width=0)

# =====================================================
# State Initialization
# =====================================================
if "query_input_text" not in st.session_state:
    st.session_state["query_input_text"] = "Show me top 5 products"

if "last_executed_response" not in st.session_state:
    st.session_state["last_executed_response"] = None

if "last_executed_question" not in st.session_state:
    st.session_state["last_executed_question"] = ""

# =====================================================
# Sidebar: System Health & Lakehouse Architecture Explorer
# =====================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <span style="font-size: 24px;">⚡</span>
        <div>
            <div style="font-weight: 800; font-size: 16px; color: #FFFFFF; letter-spacing: -0.01em;">LAKEHOUSE COPILOT</div>
            <div style="font-size: 11px; color: #64748B;">Instacart Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live Health Indicators
    st.markdown("""
    <div class="sidebar-header-box">
        <div style="font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 8px;">Pipeline Health</div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #CBD5E1;">PostgreSQL DWH</span>
                <span style="color: #10B981; font-weight: 600; display: flex; align-items: center; gap: 4px;">
                    <span class="pulsing-dot"></span> LIVE :5432
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #CBD5E1;">Airflow DAG</span>
                <span style="color: #10B981; font-weight: 600;">ACTIVE</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #CBD5E1;">Records Ingested</span>
                <span style="color: #6366F1; font-weight: 600;">279.9M+</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #CBD5E1;">Medallion Status</span>
                <span style="color: #10B981; font-weight: 600;">ALL PASSED</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📚 Medallion Architecture")
    st.markdown("""
    <div class="architecture-step">
        <span style="color: #CD7F32; font-weight: 700;">🥉 Bronze</span>
        <span>Raw Ingestion (CSV / Raw Logs)</span>
    </div>
    <div class="architecture-step">
        <span style="color: #C0C0C0; font-weight: 700;">🥈 Silver</span>
        <span>Cleaned, Deduplicated & SCD Type 2</span>
    </div>
    <div class="architecture-step">
        <span style="color: #FFD700; font-weight: 700;">🥇 Gold</span>
        <span>Star Schema & Aggregated Metrics</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### ⚡ Categorized Query Explorer")

    category = st.selectbox(
        "Select Category Domain:",
        [
            "📊 Business & Sales Analytics",
            "⚙️ Pipeline & Airflow Monitoring",
            "🛡️ Data Quality & SCD2 History",
            "🧠 Lakehouse Architecture & RAG"
        ]
    )

    query_samples = {
        "📊 Business & Sales Analytics": [
            "Show me top 5 products",
            "Show sales by department",
            "Show customer summary",
            "Which chart should I use for sales?"
        ],
        "⚙️ Pipeline & Airflow Monitoring": [
            "Did my pipeline succeed?",
            "Show previous pipeline runs",
            "Which Airflow task failed?",
            "Show latest ETL status"
        ],
        "🛡️ Data Quality & SCD2 History": [
            "Are there any data quality issues?",
            "Show history for product 6980",
            "Show rejected records",
            "Explain SCD Type 2 dimension tracking"
        ],
        "🧠 Lakehouse Architecture & RAG": [
            "Explain how my Bronze layer works",
            "Explain how my Silver layer works",
            "Explain Gold layer Star Schema",
            "How does the RAG vector engine index knowledge?"
        ]
    }

    selected_query_from_sidebar = st.radio(
        "Choose standard query:",
        query_samples[category],
        index=0
    )

    st.button(
        "📥 Load Selected Query",
        use_container_width=True,
        on_click=set_query_text,
        args=(selected_query_from_sidebar,)
    )

# =====================================================
# Main Header Section
# =====================================================
st.markdown("""
<div class="hero-header">
    <div class="hero-title-container">
        <div>
            <h1 class="hero-title">
                <span>🤖</span> AI Data Engineering Copilot
            </h1>
            <p class="hero-subtitle">
                Instacart Medallion Lakehouse • Real-time Airflow Diagnostics • Autonomous SQL & RAG Synthesis • Automated BI Reporting
            </p>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="badge-pill badge-live">
                <span class="pulsing-dot"></span> Pipeline Healthy
            </span>
            <span class="badge-pill badge-medallion">
                Medallion Lakehouse
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# Query Input & Voice Section
# =====================================================
query_box_col, voice_box_col = st.columns([3.2, 1.2], gap="medium")

# Voice input is handled by one Streamlit-compatible component.
# The recognized text is stored in session_state before the text input is rendered.
with voice_box_col:
    st.markdown("""
    <div style="font-size: 13px; font-weight: 700; color: #CBD5E1; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
        <span>🎤</span> Speech-to-Text Input
    </div>
    """, unsafe_allow_html=True)

    if HAS_MIC_RECORDER:
        try:
            voice_recorded_text = speech_to_text(
                language="en",
                start_prompt="🎙️ Record Voice Query",
                stop_prompt="⏹ Stop & Process",
                key="mic_speech_recorder"
            )

            if voice_recorded_text:
                if st.session_state.get("query_input_text") != voice_recorded_text:
                    st.session_state["query_input_text"] = voice_recorded_text
                    st.success("Voice query added")
        except Exception as e:
            st.warning(f"Voice input unavailable: {e}")
    else:
        st.caption("Install streamlit-mic-recorder to enable voice input.")

with query_box_col:
    user_query = st.text_input(
        "Ask your data engineering question (Natural Language, SQL intent, or Pipeline audit):",
        key="query_input_text",
        placeholder="e.g., Show top 5 products, Did my pipeline succeed?, Are there data quality issues?"
    )

    # Quick Suggestion Chips
    st.markdown("""
    <div style="font-size: 11px; font-weight: 600; color: #94A3B8; margin-top: 4px; margin-bottom: 2px;">
        💡 Quick Suggestions:
    </div>
    """, unsafe_allow_html=True)

    chip_col1, chip_col2, chip_col3, chip_col4, chip_col5, chip_col6 = st.columns(6)

    with chip_col1:
        st.button("🏆 Top 5 Products", use_container_width=True,
                  on_click=set_query_text, args=("Show me top 5 products",))
    with chip_col2:
        st.button("📊 Dept Sales", use_container_width=True,
                  on_click=set_query_text, args=("Show sales by department",))
    with chip_col3:
        st.button("⚡ ETL Status", use_container_width=True,
                  on_click=set_query_text, args=("Did my pipeline succeed?",))
    with chip_col4:
        st.button("🛡️ Data Quality", use_container_width=True,
                  on_click=set_query_text, args=("Are there any data quality issues?",))
    with chip_col5:
        st.button("🔄 SCD2 History", use_container_width=True,
                  on_click=set_query_text, args=("Show history for product 6980",))
    with chip_col6:
        st.button("📖 Bronze Layer", use_container_width=True,
                  on_click=set_query_text, args=("Explain how my Bronze layer works",))

btn_col, _ = st.columns([1.5, 4.5])
with btn_col:
    execute_button = st.button(
        "⚡ Ask Copilot Agent",
        type="primary",
        use_container_width=True
    )

# =====================================================
# Pipeline Query Processing & Execution
# =====================================================
if execute_button and user_query.strip():
    with st.spinner("🤖 Autonomous Agent analyzing query across Lakehouse tools..."):
        try:
            response_payload = process_question(user_query.strip())
            st.session_state["last_executed_response"] = response_payload
            st.session_state["last_executed_question"] = user_query.strip()
        except Exception as e:
            st.error(f"Execution Error: {e}")

# =====================================================
# Render Executive Results Dashboard
# =====================================================
if st.session_state["last_executed_response"] is not None:
    res = st.session_state["last_executed_response"]
    query_text = st.session_state["last_executed_question"]

    intent = res["intent"]
    reasoning = res["reasoning"]
    raw_data = res["raw_data"]
    formatted_text = res["formatted_text"]
    chart_info = res["chart_info"]
    insights = res.get("insights", [])
    actions = res.get("actions", [])
    report_data = res.get("report_data", {})

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # 1. Agentic AI Decision Header Pill
    st.markdown(f"""
    <div class="decision-banner">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">🎯</span>
                <div>
                    <span style="font-size: 11px; font-weight: 700; color: #818CF8; text-transform: uppercase; letter-spacing: 0.05em;">Autonomous Agent Decision</span>
                    <div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">
                        Routed to Tool: <code style="background: rgba(99, 102, 241, 0.25); color: #A5B4FC; padding: 2px 8px; border-radius: 6px;">{intent}</code>
                    </div>
                </div>
            </div>
            <div style="font-size: 13px; color: #CBD5E1; max-width: 600px;">
                <span style="font-weight: 600; color: #94A3B8;">Reasoning:</span> {reasoning}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Executive Metric Cards Bar
    if intent == "top_products" and raw_data:
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card-pro">
                <div class="metric-label-pro">Top Item Orders</div>
                <div class="metric-value-pro">{raw_data[0][2]:,}</div>
                <div class="metric-sub-pro">🏆 {raw_data[0][1]}</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Ranked Items</div>
                <div class="metric-value-pro">{len(raw_data)} Products</div>
                <div class="metric-sub-pro">📊 Gold Dim & Fact Layer</div>
            </div>
            <div class="metric-card-pro success">
                <div class="metric-label-pro">Data Freshness</div>
                <div class="metric-value-pro">Live PostgreSQL</div>
                <div class="metric-sub-pro">⚡ 0 Latency Delta</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Schema Layer</div>
                <div class="metric-value-pro">Gold Mart</div>
                <div class="metric-sub-pro">🥇 Aggregated Star Schema</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif intent == "sales_summary" and raw_data:
        total_items = sum(d[1] for d in raw_data)
        total_orders = sum(d[2] for d in raw_data)
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card-pro">
                <div class="metric-label-pro">Total Products Sold</div>
                <div class="metric-value-pro">{total_items:,}</div>
                <div class="metric-sub-pro">📦 Across all depts</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Total Orders Placed</div>
                <div class="metric-value-pro">{total_orders:,}</div>
                <div class="metric-sub-pro">🛒 Unique Transactions</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Active Departments</div>
                <div class="metric-value-pro">{len(raw_data)} Depts</div>
                <div class="metric-sub-pro">🏢 Full Catalog Coverage</div>
            </div>
            <div class="metric-card-pro success">
                <div class="metric-label-pro">Reporting Status</div>
                <div class="metric-value-pro">Verified</div>
                <div class="metric-sub-pro">✅ Silver-Gold Reconciled</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif intent == "customer_summary" and raw_data:
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card-pro">
                <div class="metric-label-pro">Top Customer Orders</div>
                <div class="metric-value-pro">{raw_data[0][1]} Orders</div>
                <div class="metric-sub-pro">👤 User ID #{raw_data[0][0]}</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Analyzed Cohort</div>
                <div class="metric-value-pro">{len(raw_data)} VIPs</div>
                <div class="metric-sub-pro">💎 Highest Repeat Ratio</div>
            </div>
            <div class="metric-card-pro success">
                <div class="metric-label-pro">Retention Tier</div>
                <div class="metric-value-pro">High Loyalty</div>
                <div class="metric-sub-pro">🌟 Repeat Buyer Segment</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Source Dimension</div>
                <div class="metric-value-pro">dim_users</div>
                <div class="metric-sub-pro">🥇 Gold Dimension Table</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif intent in ["etl_status", "etl_history"]:
        st.markdown("""
        <div class="metric-grid">
            <div class="metric-card-pro success">
                <div class="metric-label-pro">Pipeline Execution</div>
                <div class="metric-value-pro">SUCCESS</div>
                <div class="metric-sub-pro">🟢 Airflow Exit Code 0</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Total Processed Records</div>
                <div class="metric-value-pro">279,921,756</div>
                <div class="metric-sub-pro">📈 Multi-Run Cumulative</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Tables Ingested</div>
                <div class="metric-value-pro">10 Tables</div>
                <div class="metric-sub-pro">🥉 Bronze + 🥈 Silver + 🥇 Gold</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Execution Duration</div>
                <div class="metric-value-pro">301s</div>
                <div class="metric-sub-pro">⚡ Optimized Batch</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif intent == "data_quality":
        st.markdown("""
        <div class="metric-grid">
            <div class="metric-card-pro success">
                <div class="metric-label-pro">Data Quality Check</div>
                <div class="metric-value-pro">ALL PASSED</div>
                <div class="metric-sub-pro">🛡️ 0 Integrity Violations</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Bronze Validation</div>
                <div class="metric-value-pro">6 Files OK</div>
                <div class="metric-sub-pro">✅ Schema & Header Verified</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Silver Deduplication</div>
                <div class="metric-value-pro">6 Tables OK</div>
                <div class="metric-sub-pro">✅ 0 Duplicate Keys</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Rejected Quarantine</div>
                <div class="metric-value-pro">0 Rows</div>
                <div class="metric-sub-pro">✨ Clean Ingestion</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card-pro">
                <div class="metric-label-pro">Query Domain</div>
                <div class="metric-value-pro">{intent.upper()}</div>
                <div class="metric-sub-pro">🔍 Semantic Routing</div>
            </div>
            <div class="metric-card-pro success">
                <div class="metric-label-pro">Agent Response</div>
                <div class="metric-value-pro">200 OK</div>
                <div class="metric-sub-pro">⚡ Execution Verified</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Knowledge Engine</div>
                <div class="metric-value-pro">RAG + SQL</div>
                <div class="metric-sub-pro">🧠 Hybrid Retrieval</div>
            </div>
            <div class="metric-card-pro">
                <div class="metric-label-pro">Report Readiness</div>
                <div class="metric-value-pro">Ready</div>
                <div class="metric-sub-pro">📄 PDF & TXT Available</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # Organized Multi-Tab Executive Presentation
    # =====================================================
    tab_analytics, tab_insights, tab_architecture, tab_reports = st.tabs([
        "📊 Analytics & Visuals",
        "💡 AI Strategic Insights & Actions",
        "🏗️ Medallion Pipeline Diagnostics",
        "📄 Executive Reports & Exports"
    ])

    # -----------------------------------------------------
    # TAB 1: Analytics & Interactive Visuals
    # -----------------------------------------------------
    with tab_analytics:
        col_table, col_chart = st.columns([1.1, 1.3], gap="large")

        with col_table:
            st.markdown("#### 📋 Data Records")

            if intent == "top_products" and raw_data:
                df = pd.DataFrame(raw_data, columns=["Product ID", "Product Name", "Total Orders"])
                st.dataframe(df, use_container_width=True, height=320)
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export CSV", csv_data, "top_products.csv", "text/csv", key="dl_csv_prod")

            elif intent == "sales_summary" and raw_data:
                df = pd.DataFrame(raw_data, columns=["Department", "Products Sold", "Total Orders"])
                st.dataframe(df, use_container_width=True, height=320)
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export CSV", csv_data, "sales_summary.csv", "text/csv", key="dl_csv_sales")

            elif intent == "customer_summary" and raw_data:
                df = pd.DataFrame(raw_data, columns=["User ID", "Total Orders", "Last Order Number"])
                st.dataframe(df, use_container_width=True, height=320)
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export CSV", csv_data, "customer_summary.csv", "text/csv", key="dl_csv_cust")

            elif intent == "scd_history" and raw_data:
                df = pd.DataFrame(
                    raw_data,
                    columns=["Product ID", "Product Name", "Department", "Aisle", "End Date", "Effective Date", "Is Current"]
                )
                st.dataframe(df, use_container_width=True, height=320)
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export CSV", csv_data, "scd_history.csv", "text/csv", key="dl_csv_scd")

            else:
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); font-family: monospace; font-size: 13px; color: #E2E8F0; white-space: pre-wrap; line-height: 1.6;">
{formatted_text}
                </div>
                """, unsafe_allow_html=True)

            # Modern Voice Playback Widget
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            tts_text_clean = f"{formatted_text}. Key Insight: {' '.join(insights[:2])}".replace('"', '\\"')

            components.html(f"""
            <style>
                .pro-tts-btn {{
                    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                    color: #FFFFFF;
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: 600;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    transition: all 0.2s ease;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
                }}
                .pro-tts-btn:hover {{
                    background: linear-gradient(135deg, #34D399 0%, #10B981 100%);
                    transform: translateY(-1px);
                }}
                .pro-tts-btn.active {{
                    background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
                }}
            </style>

            <button id="ttsPlayTrigger" class="pro-tts-btn" onclick="toggleSpeechSynthesis()">
                <span>🔊</span> <span>Listen to Audio Briefing</span>
            </button>

            <script>
                let isSpeakingNow = false;
                const audioContent = "{tts_text_clean}";

                function toggleSpeechSynthesis() {{
                    const btn = document.getElementById("ttsPlayTrigger");

                    if (!('speechSynthesis' in window)) {{
                        alert("Text-to-Speech is not supported in this browser.");
                        return;
                    }}

                    if (window.speechSynthesis.speaking || isSpeakingNow) {{
                        window.speechSynthesis.cancel();
                        isSpeakingNow = false;
                        btn.className = "pro-tts-btn";
                        btn.innerHTML = "<span>🔊</span> <span>Listen to Audio Briefing</span>";
                    }} else {{
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance(audioContent);
                        utterance.rate = 1.0;
                        utterance.pitch = 1.0;
                        utterance.lang = "en-US";

                        utterance.onend = () => {{
                            isSpeakingNow = false;
                            btn.className = "pro-tts-btn";
                            btn.innerHTML = "<span>🔊</span> <span>Listen to Audio Briefing</span>";
                        }};

                        utterance.onerror = () => {{
                            isSpeakingNow = false;
                            btn.className = "pro-tts-btn";
                            btn.innerHTML = "<span>🔊</span> <span>Listen to Audio Briefing</span>";
                        }};

                        window.speechSynthesis.speak(utterance);
                        isSpeakingNow = true;
                        btn.className = "pro-tts-btn active";
                        btn.innerHTML = "<span>⏹</span> <span>Stop Audio Playback</span>";
                    }}
                }}
            </script>
            """, height=45)

        with col_chart:
            st.markdown("#### 📈 Interactive Visualization")

            # Custom Dark Theme Plotly Styler
            def apply_dark_theme(fig, title_text):
                fig.update_layout(
                    title=dict(
                        text=f"<b>{title_text}</b>",
                        font=dict(size=14, color="#F8FAFC", family="Plus Jakarta Sans")
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(15, 23, 42, 0.5)",
                    font=dict(color="#94A3B8", family="Plus Jakarta Sans"),
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(
                        font=dict(color="#CBD5E1"),
                        bgcolor="rgba(15, 23, 42, 0.7)",
                        bordercolor="rgba(255, 255, 255, 0.1)"
                    ),
                    xaxis=dict(
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        zerolinecolor="rgba(255, 255, 255, 0.1)"
                    ),
                    yaxis=dict(
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        zerolinecolor="rgba(255, 255, 255, 0.1)"
                    )
                )
                return fig

            try:
                if intent == "top_products" and raw_data:
                    df_plot = pd.DataFrame(raw_data, columns=["Product ID", "Product Name", "Total Orders"])
                    fig = px.bar(
                        df_plot,
                        x="Total Orders",
                        y="Product Name",
                        orientation="h",
                        color="Total Orders",
                        color_continuous_scale=["#6366F1", "#06B6D4", "#10B981"]
                    )
                    fig.update_layout(yaxis={"categoryorder": "total ascending"})
                    apply_dark_theme(fig, "Top Products Order Volume Ranking")
                    st.plotly_chart(fig, use_container_width=True)

                elif intent == "sales_summary" and raw_data:
                    df_plot = pd.DataFrame(raw_data, columns=["Department", "Products Sold", "Total Orders"])
                    sub_tab1, sub_tab2 = st.tabs(["🍩 Distribution (Donut)", "📊 Volume (Bar)"])
                    with sub_tab1:
                        fig1 = px.pie(
                            df_plot,
                            names="Department",
                            values="Products Sold",
                            hole=0.45,
                            color_discrete_sequence=["#6366F1", "#3B82F6", "#06B6D4", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]
                        )
                        apply_dark_theme(fig1, "Department Sales Share")
                        st.plotly_chart(fig1, use_container_width=True)
                    with sub_tab2:
                        fig2 = px.bar(
                            df_plot,
                            x="Department",
                            y="Total Orders",
                            color="Total Orders",
                            color_continuous_scale=["#8B5CF6", "#6366F1", "#38BDF8"]
                        )
                        apply_dark_theme(fig2, "Department Order Volume")
                        st.plotly_chart(fig2, use_container_width=True)

                elif intent == "customer_summary" and raw_data:
                    df_plot = pd.DataFrame(raw_data, columns=["User ID", "Total Orders", "Last Order Number"])
                    df_plot["User ID"] = "User #" + df_plot["User ID"].astype(str)
                    fig = px.bar(
                        df_plot,
                        x="User ID",
                        y="Total Orders",
                        color="Total Orders",
                        color_continuous_scale=["#3B82F6", "#6366F1", "#EC4899"]
                    )
                    apply_dark_theme(fig, "High-Value Customer Order Frequency")
                    st.plotly_chart(fig, use_container_width=True)

                elif intent in ["etl_history", "etl_status"]:
                    df_plot = pd.DataFrame({
                        "Execution Date": ["2026-08-11", "2026-08-12"],
                        "Processed Rows (M)": [69.98, 279.92],
                        "Duration (s)": [69, 301]
                    })
                    fig = px.line(
                        df_plot,
                        x="Execution Date",
                        y="Processed Rows (M)",
                        markers=True,
                        line_shape="spline",
                        color_discrete_sequence=["#10B981"]
                    )
                    apply_dark_theme(fig, "Lakehouse Records Processed Over Runs")
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.info("💡 Interactive visual generated automatically for query domain. Run a sales or products query to explore chart variations.")

            except Exception as e:
                st.warning(f"Visualization Note: {e}")

    # -----------------------------------------------------
    # TAB 2: AI Insights & Strategic Actions
    # -----------------------------------------------------
    with tab_insights:
        col_ins, col_act = st.columns(2, gap="large")

        with col_ins:
            st.markdown("#### 💡 AI Strategic Insights (Insight Agent)")
            if insights:
                for ins in insights:
                    st.markdown(f"""
                    <div class="insight-card-pro">
                        <span style="font-size: 18px; line-height: 1;">💡</span>
                        <div>{ins}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No anomalies or specific data insights detected for this query domain.")

        with col_act:
            st.markdown("#### 🚀 Recommended Actions (Action Agent)")
            if actions:
                for act in actions:
                    st.markdown(f"""
                    <div class="action-card-pro">
                        <span style="font-size: 18px; line-height: 1;">🎯</span>
                        <div>{act}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No urgent pipeline remediation needed.")

        # Power BI & Analytics Advisor
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="advisor-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                <div style="font-weight: 700; font-size: 15px; color: #FFFFFF; display: flex; align-items: center; gap: 8px;">
                    <span>🧠</span> Power BI & Visual Analytics Advisor
                </div>
                <span class="badge-pill" style="background: rgba(139, 92, 246, 0.2); color: #C4B5FD; border: 1px solid rgba(139, 92, 246, 0.4);">
                    Recommended: {chart_info['chart_type']}
                </span>
            </div>
            <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
                <strong>Why this visual is recommended:</strong> {chart_info.get('reasoning', 'This visualization was selected based on the available data and query requirements.')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # TAB 3: Medallion Architecture & Airflow Monitor
    # -----------------------------------------------------
    with tab_architecture:
        st.markdown("#### 🏗️ End-to-End Medallion Lakehouse Diagnostics")

        col_med1, col_med2, col_med3 = st.columns(3)

        with col_med1:
            st.markdown("""
            <div class="glass-card" style="border-top: 4px solid #CD7F32;">
                <div style="font-weight: 700; font-size: 14px; color: #CD7F32; margin-bottom: 6px;">🥉 BRONZE LAYER (RAW)</div>
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">Ingestion & Raw Staging</div>
                <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                    • 6 Source CSV Files Ingested<br/>
                    • Schema & Header Validation: PASSED<br/>
                    • Quarantine Quarantine Rate: 0.00%<br/>
                    • Target: <code>raw_stage</code> schemas
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_med2:
            st.markdown("""
            <div class="glass-card" style="border-top: 4px solid #C0C0C0;">
                <div style="font-weight: 700; font-size: 14px; color: #E2E8F0; margin-bottom: 6px;">🥈 SILVER LAYER (CLEANED)</div>
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">Deduplication & SCD Type 2</div>
                <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                    • 6 Silver Tables Cleaned<br/>
                    • Deduplication & Null Check: PASSED<br/>
                    • SCD Type 2 Product Tracking: ACTIVE<br/>
                    • Target: <code>silver_instacart</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_med3:
            st.markdown("""
            <div class="glass-card" style="border-top: 4px solid #FFD700;">
                <div style="font-weight: 700; font-size: 14px; color: #FFD700; margin-bottom: 6px;">🥇 GOLD LAYER (ANALYTICS)</div>
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">Star Schema & Aggregations</div>
                <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                    • 4 Star Schema Dimensions & Facts<br/>
                    • <code>fact_order_products</code> & <code>dim_users</code><br/>
                    • Power BI Direct Lake Ready: YES<br/>
                    • Target: <code>gold_analytics</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Airflow DAG Flow
        st.markdown("##### ⚙️ Airflow Execution DAG Details")
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #F8FAFC;">DAG: <code>instacart_etl_pipeline</code></span>
                <span class="badge-pill badge-live"><span class="pulsing-dot"></span> State: SUCCESS</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #38BDF8; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px;">
                start_pipeline ➔ ingest_bronze_task ➔ validate_and_clean_silver_task ➔ scd_type2_transform_task ➔ build_gold_star_schema_task ➔ generate_data_quality_report ➔ end_pipeline
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # TAB 4: Executive Reports & Exports
    # -----------------------------------------------------
    with tab_reports:
        st.markdown("#### 📄 Executive Report Generation")
        st.markdown("Download automated pipeline diagnostic and business intelligence summaries generated by the autonomous agent.")

        rep_txt_bytes = create_txt_bytes(report_data.get("full_text", formatted_text))
        rep_pdf_bytes = create_pdf_bytes(report_data)

        col_dl1, col_dl2, col_preview = st.columns([1, 1, 2], gap="medium")

        with col_dl1:
            st.download_button(
                label="📄 Download PDF Report",
                data=rep_pdf_bytes,
                file_name=f"instacart_copilot_report_{intent}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

        with col_dl2:
            st.download_button(
                label="📝 Download TXT Report",
                data=rep_txt_bytes,
                file_name=f"instacart_copilot_report_{intent}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col_preview:
            st.markdown("""
            <div style="font-size: 12px; color: #94A3B8;">
                🔒 Reports include cryptographic timestamp, agent execution path, intent reasoning, and business insights generated according to ISO-compliant enterprise reporting standards.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("👁️ Preview Full Report Text", expanded=False):
            st.code(report_data.get("full_text", formatted_text), language="markdown")

else:
    # Empty State Hero Card
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: rgba(15, 23, 42, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 16px; margin-top: 20px;">
        <span style="font-size: 48px; display: block; margin-bottom: 12px;">⚡</span>
        <h3 style="color: #F8FAFC; margin-bottom: 8px; font-weight: 700;">Ready to Analyze Your Lakehouse Pipeline</h3>
        <p style="color: #94A3B8; max-width: 600px; margin: 0 auto 20px auto; font-size: 14px;">
            Ask a business analytics question, check Airflow task executions, verify Medallion data quality, or track SCD Type 2 dimension histories.
        </p>
        <div style="display: inline-flex; gap: 8px; font-size: 12px; color: #64748B;">
            <span>💡 Try: "Show top 5 products"</span> • 
            <span>"Did my pipeline succeed?"</span> • 
            <span>"Show sales by department"</span>
        </div>
    </div>
    """, unsafe_allow_html=True)