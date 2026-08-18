import streamlit as st
import pandas as pd
import plotly.express as px
import html
import streamlit.components.v1 as components

from agent.main import process_question


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Lakehouse Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "question" not in st.session_state:
    st.session_state.question = ""


# =========================================================
# THEME COLORS
# =========================================================

if st.session_state.dark_mode:

    BG = "#07111F"
    SIDEBAR_BG = "#081321"
    CARD = "#101C2D"
    CARD_2 = "#0C1727"
    BORDER = "#22324A"

    TEXT = "#E8EEF8"
    MUTED = "#94A3B8"

    ACCENT = "#7C5CFC"
    GREEN = "#58D68D"
    RED = "#FF5C5C"

else:

    BG = "#F4F7FB"
    SIDEBAR_BG = "#FFFFFF"
    CARD = "#FFFFFF"
    CARD_2 = "#F8FAFC"
    BORDER = "#D9E2EC"

    TEXT = "#182230"
    MUTED = "#64748B"

    ACCENT = "#6D4AFF"
    GREEN = "#22A06B"
    RED = "#E5484D"


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    f"""
<style>

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

.block-container {{
    padding-top: 1.2rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}}

h1, h2, h3, h4, h5, p, span, label {{
    color: {TEXT};
}}

.small-muted {{
    color: {MUTED};
    font-size: 14px;
}}

.logo-title {{
    font-size: 25px;
    font-weight: 800;
    color: {TEXT};
}}

.sidebar-subtitle {{
    color: {MUTED};
    font-size: 13px;
}}

.section-title {{
    font-size: 13px;
    font-weight: 700;
    color: {MUTED};
    letter-spacing: 0.8px;
    margin-top: 10px;
    margin-bottom: 10px;
}}

.agent-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 13px;
    margin-bottom: 9px;
}}

.agent-name {{
    font-weight: 700;
    color: {TEXT};
    font-size: 16px;
}}

.agent-desc {{
    color: {MUTED};
    font-size: 12px;
    margin-top: 3px;
}}

.health-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 15px;
    padding: 15px;
}}

.hero {{
    background: linear-gradient(
        135deg,
        {CARD},
        {CARD_2}
    );
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 15px;
}}

.metric-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 18px;
    min-height: 120px;
}}

.metric-label {{
    font-size: 11px;
    font-weight: 700;
    color: {MUTED};
    letter-spacing: 0.7px;
}}

.metric-value {{
    font-size: 25px;
    font-weight: 800;
    color: {TEXT};
    margin-top: 8px;
}}

.metric-growth {{
    color: {GREEN};
    font-size: 13px;
    margin-top: 6px;
}}

.question-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 17px 20px;
    margin-bottom: 16px;
}}

.response-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px;
}}

.insight-box {{
    background: {CARD_2};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
}}

.status-online {{
    display: inline-block;
    color: {GREEN};
    background: rgba(50, 200, 120, 0.10);
    border: 1px solid rgba(50, 200, 120, 0.20);
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 11px;
    font-weight: 700;
}}

div.stButton > button {{
    border-radius: 10px;
    min-height: 42px;
    border: 1px solid {BORDER};
    background: {CARD};
    color: {TEXT};
    font-weight: 600;
}}

div.stButton > button:hover {{
    border-color: {ACCENT};
    color: {TEXT};
}}

.stTextInput input {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

.stTextInput input::placeholder {{
    color: {MUTED};
}}

[data-testid="stTabs"] button {{
    color: {MUTED};
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {TEXT};
}}

.footer {{
    text-align: center;
    color: {MUTED};
    padding: 20px;
    font-size: 13px;
}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SPEAK ANSWER
# =========================================================

def speak_answer(text):

    safe_text = html.escape(str(text))

    components.html(
        f"""
        <script>
        const text = `{safe_text}`;

        window.speechSynthesis.cancel();

        const speech = new SpeechSynthesisUtterance(text);

        speech.rate = 1;
        speech.pitch = 1;
        speech.volume = 1;

        window.speechSynthesis.speak(speech);
        </script>
        """,
        height=0
    )


# =========================================================
# CREATE CHART
# =========================================================

def create_chart(result):

    if not result:
        return None

    agent_type = result.get("type")
    data = result.get("data")

    if not data:
        return None

    try:

        # ---------------------------------------------
        # TOP PRODUCTS
        # ---------------------------------------------

        if agent_type == "top_products":

            df = pd.DataFrame(
                data,
                columns=[
                    "Product ID",
                    "Product Name",
                    "Total Orders"
                ]
            )

            fig = px.bar(
                df,
                x="Product Name",
                y="Total Orders",
                text="Total Orders",
                title="Top Products by Total Orders"
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside"
            )

            fig.update_layout(
                height=430,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=TEXT,
                xaxis_title="Products",
                yaxis_title="Total Orders"
            )

            return fig

        # ---------------------------------------------
        # CUSTOMER SUMMARY
        # ---------------------------------------------

        elif agent_type == "customer_summary":

            if len(data[0]) >= 2:

                df = pd.DataFrame(
                    data
                )

                df.columns = [
                    "Customer ID",
                    "Total Orders"
                ][:len(df.columns)]

                fig = px.bar(
                    df,
                    x=df.columns[0],
                    y=df.columns[1],
                    title="Top Customers by Orders"
                )

                fig.update_layout(
                    height=430,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color=TEXT
                )

                return fig

        # ---------------------------------------------
        # SALES SUMMARY
        # ---------------------------------------------

        elif agent_type == "sales_summary":

            df = pd.DataFrame(
                data
            )

            if len(df.columns) >= 2:

                fig = px.bar(
                    df,
                    x=df.columns[0],
                    y=df.columns[1],
                    title="Sales by Department"
                )

                fig.update_layout(
                    height=430,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color=TEXT
                )

                return fig

        # ---------------------------------------------
        # ETL HISTORY
        # ---------------------------------------------

        elif agent_type == "etl_history":

            df = pd.DataFrame(data)

            if len(df.columns) >= 2:

                fig = px.bar(
                    df,
                    x=df.columns[0],
                    y=df.columns[-1],
                    title="ETL Processing History"
                )

                fig.update_layout(
                    height=430,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color=TEXT
                )

                return fig

    except Exception:
        return None

    return None


# =========================================================
# FORMAT DATA
# =========================================================

def format_data(data):

    if not data:
        return "No data available."

    formatted = ""

    for i, row in enumerate(data, start=1):

        if isinstance(row, (list, tuple)):
            formatted += f"{i}. " + " | ".join(
                str(x) for x in row
            ) + "\n\n"

        else:
            formatted += f"{i}. {row}\n\n"

    return formatted


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo-title">
        ⚡ LAKEHOUSE COPILOT
        </div>

        <div class="sidebar-subtitle">
        Instacart Analytics Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="section-title">PIPELINE HEALTH</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="health-card">

        🟢 PostgreSQL DWH
        <span style="float:right;color:{GREEN};font-weight:700;">
        LIVE
        </span>

        <br><br>

        🟢 Airflow DAG
        <span style="float:right;color:{GREEN};font-weight:700;">
        ACTIVE
        </span>

        <br><br>

        📊 Multi-Agent System
        <span style="float:right;color:#60A5FA;font-weight:700;">
        READY
        </span>

        <br><br>

        🛡️ Data Quality
        <span style="float:right;color:{GREEN};font-weight:700;">
        CHECKED
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">AI AGENTS (7)</div>',
        unsafe_allow_html=True
    )

    agents = [
        ("⚙️", "Pipeline Agent", "Pipeline Monitoring"),
        ("🛟", "Support Agent", "Project Guidance"),
        ("📊", "Data Agent", "Query & Data Retrieval"),
        ("💡", "Insight Agent", "Business Intelligence"),
        ("🎯", "Action Agent", "Recommendations"),
        ("📄", "Report Agent", "Report Generation"),
        ("🧠", "ML Agent", "Predictions & ML")
    ]

    for icon, name, desc in agents:

        st.markdown(
            f"""
            <div class="agent-card">

            <div class="agent-name">
            {icon} {name}
            </div>

            <div class="agent-desc">
            {desc}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">MEDALLION ARCHITECTURE</div>',
        unsafe_allow_html=True
    )

    architecture = [
        ("🥉", "Bronze Layer", "Raw Data Ingestion"),
        ("🥈", "Silver Layer", "Cleaned & Transformed"),
        ("🥇", "Gold Layer", "Analytics & Business Layer")
    ]

    for icon, name, desc in architecture:

        st.markdown(
            f"""
            <div class="agent-card">

            <div class="agent-name">
            {icon} {name}
            </div>

            <div class="agent-desc">
            {desc}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode
    )

    if dark_mode != st.session_state.dark_mode:

        st.session_state.dark_mode = dark_mode
        st.rerun()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.history = []
        st.session_state.result = None
        st.session_state.question = ""

        st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        f"""
        <div class="hero">

        <div style="font-size:31px;font-weight:800;color:{TEXT};">
        🤖 AI Data Engineering Copilot
        </div>

        <div style="color:{MUTED};margin-top:8px;">
        Instacart Data Pipeline • PostgreSQL • Airflow •
        Medallion Architecture • Multi-Agent AI
        </div>

        <br>

        <span class="status-online">
        ● SYSTEM ONLINE
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        f"""
        <div class="hero" style="text-align:center;">

        <div style="font-size:20px;font-weight:700;">
        ⚙️ 7 AGENTS
        </div>

        <div style="color:{MUTED};font-size:12px;margin-top:8px;">
        Ready to Assist
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("👥", "TOTAL ORDERS", "3.4M+", "+12.5% vs dataset"),
    ("👨‍👩‍👧", "TOTAL CUSTOMERS", "206K+", "Active users"),
    ("💡", "TOTAL PRODUCTS", "49K+", "Available products"),
    ("⚙️", "AI SYSTEM", "7 Agents", "Multi-Agent Ready")
]

for col, metric in zip([m1, m2, m3, m4], metrics):

    icon, label, value, growth = metric

    with col:

        st.markdown(
            f"""
            <div class="metric-card">

            <div style="font-size:24px;">
            {icon}
            </div>

            <div class="metric-label">
            {label}
            </div>

            <div class="metric-value">
            {value}
            </div>

            <div class="metric-growth">
            {growth}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


st.write("")


# =========================================================
# QUESTION INPUT
# =========================================================

left, right = st.columns([3, 1])

with left:

    st.markdown(
        f"""
        <h2 style="color:{TEXT};margin-bottom:0;">
        Ask the Copilot
        </h2>

        <div class="small-muted">
        Ask anything about your Instacart Data Engineering Project
        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input(
        "Question",
        placeholder="Example: Show me top products",
        label_visibility="collapsed",
        key="question_input"
    )

    st.write("")

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("🏆 Top Products", use_container_width=True):
            question = "Show me top products"

    with q2:
        if st.button("👥 Top Customers", use_container_width=True):
            question = "Show me top customers"

    with q3:
        if st.button("⚡ ETL Status", use_container_width=True):
            question = "Show me ETL status"

    q4, q5, q6 = st.columns(3)

    with q4:
        if st.button("🛡️ Data Quality", use_container_width=True):
            question = "Show me data quality status"

    with q5:
        if st.button("💡 Insights", use_container_width=True):
            question = "Give me insights about top products"

    with q6:
        if st.button("🥉 Bronze Layer", use_container_width=True):
            question = "Explain the Bronze Layer"

    st.write("")

    ask = st.button(
        "⚡ Ask Copilot",
        type="primary",
        use_container_width=True
    )


with right:

    st.markdown(
        f"""
        <div class="response-card">

        <h3 style="margin-top:0;">
        🎙️ Voice Input
        </h3>

        <div class="small-muted">
        Use microphone to ask your question
        </div>

        <br>

        <div style="
        border:1px solid {BORDER};
        border-radius:10px;
        padding:14px;
        color:{MUTED};
        ">

        🎤 Voice input can be added here

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if ask and question.strip():

    try:

        result = process_question(question)

        st.session_state.result = result

        st.session_state.history.insert(
            0,
            question
        )

        st.session_state.question = question

    except Exception as e:

        st.error(
            f"Error while processing question: {str(e)}"
        )


# =========================================================
# RESPONSE AREA
# =========================================================

if st.session_state.result:

    result = st.session_state.result

    selected_agent = result.get(
        "selected_agent",
        "unknown"
    )

    formatted_text = result.get(
        "formatted_text",
        ""
    )

    raw_result = result.get(
        "result",
        {}
    )

    st.write("")

    # -----------------------------------------------------
    # USER QUESTION
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="question-card">

        <div class="metric-label">
        USER QUESTION
        </div>

        <div style="
        font-size:20px;
        font-weight:700;
        margin-top:8px;
        color:{TEXT};
        ">

        {st.session_state.question}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # AGENT TITLE
    # -----------------------------------------------------

    agent_names = {

        "pipeline_agent": "⚙️ Pipeline Agent",
        "support_agent": "🛟 Support Agent",
        "data_agent": "📊 Data Agent",
        "insight_agent": "💡 Insight Agent",
        "action_agent": "🎯 Action Agent",
        "report_agent": "📄 Report Agent",
        "ml_agent": "🧠 ML Agent"

    }

    st.markdown(
        f"""
        <h2 style="color:{TEXT};">
        {agent_names.get(selected_agent, "🤖 AI Agent")}
        </h2>

        <div class="small-muted">
        Selected Agent: {selected_agent}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "💬 Response",
            "📊 Data",
            "💡 Insights",
            "🎯 Actions",
            "📄 Report"
        ]
    )

    # -----------------------------------------------------
    # RESPONSE TAB
    # -----------------------------------------------------

    with tab1:

        col_response, col_chart = st.columns(
            [1, 1]
        )

        with col_response:

            # IMPORTANT:
            # इथे रिकामा rectangle नाही.
            # Content असल्यावरच card दिसेल.

            if formatted_text:

                st.markdown(
                    '<div class="response-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    formatted_text
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    "🔊 Speak Answer",
                    key="speak_answer"
                ):

                    speak_answer(
                        formatted_text
                    )

        with col_chart:

            chart = None

            if isinstance(raw_result, dict):

                chart = create_chart(
                    raw_result
                )

            if chart is not None:

                st.markdown(
                    '<div class="response-card">',
                    unsafe_allow_html=True
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="response-card"
                    style="min-height:250px;display:flex;
                    align-items:center;justify-content:center;
                    text-align:center;">

                    <div>

                    <div style="font-size:35px;">
                    📊
                    </div>

                    <div style="
                    color:{MUTED};
                    margin-top:10px;
                    ">

                    Chart is displayed only when
                    the data is suitable for visualization.

                    </div>

                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # -----------------------------------------------------
    # DATA TAB
    # -----------------------------------------------------

    with tab2:

        if isinstance(raw_result, dict):

            data = raw_result.get("data")

            if data:

                st.markdown(
                    '<div class="response-card">',
                    unsafe_allow_html=True
                )

                try:

                    if isinstance(data, list):

                        df = pd.DataFrame(
                            data
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                    else:

                        st.write(data)

                except Exception:

                    st.code(
                        str(data)
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            else:

                st.info(
                    "No structured data available for this response."
                )

    # -----------------------------------------------------
    # INSIGHTS TAB
    # -----------------------------------------------------

    with tab3:

        if isinstance(raw_result, dict):

            insights = raw_result.get(
                "insights"
            )

            if insights:

                for insight in insights:

                    st.markdown(
                        f"""
                        <div class="insight-box">
                        💡 {insight}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No additional insights generated."
                )

        else:

            st.info(
                "Insights are generated by the Insight Agent."
            )

    # -----------------------------------------------------
    # ACTIONS TAB
    # -----------------------------------------------------

    with tab4:

        if isinstance(raw_result, dict):

            actions = raw_result.get(
                "actions"
            )

            if actions:

                for action in actions:

                    st.markdown(
                        f"""
                        <div class="insight-box">
                        🎯 {action}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No recommended actions available."
                )

        else:

            st.info(
                "Actions are generated by the Action Agent."
            )

    # -----------------------------------------------------
    # REPORT TAB
    # -----------------------------------------------------

    with tab5:

        if isinstance(raw_result, dict):

            report = raw_result.get(
                "report"
            )

            if report:

                st.markdown(
                    '<div class="response-card">',
                    unsafe_allow_html=True
                )

                if isinstance(report, dict):

                    st.markdown(
                        f"## 📄 {report.get('title', 'Report')}"
                    )

                    if report.get("insights"):

                        st.markdown(
                            "### 💡 Insights"
                        )

                        for item in report["insights"]:
                            st.write(
                                f"• {item}"
                            )

                    if report.get(
                        "recommended_actions"
                    ):

                        st.markdown(
                            "### 🎯 Recommended Actions"
                        )

                        for item in report[
                            "recommended_actions"
                        ]:
                            st.write(
                                f"• {item}"
                            )

                else:

                    st.write(report)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            else:

                st.info(
                    "No report generated for this question."
                )


# =========================================================
# CONVERSATION HISTORY
# =========================================================

if st.session_state.history:

    st.write("")
    st.divider()

    st.markdown(
        f"""
        <h3 style="color:{TEXT};">
        🕘 Conversation History
        </h3>
        """,
        unsafe_allow_html=True
    )

    for i, item in enumerate(
        st.session_state.history[:5],
        start=1
    ):

        st.markdown(
            f"""
            <div class="insight-box">
            {i}. {item}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

    Built with ❤️ using Streamlit
    • Instacart Data Engineering Project
    • Multi-Agent AI System

    </div>
    """,
    unsafe_allow_html=True
)