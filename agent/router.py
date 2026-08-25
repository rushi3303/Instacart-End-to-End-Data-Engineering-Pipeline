def detect_intent(question):
    """
    Detects which agent should handle
    the user's question.

    Agents:
    1. Support Agent
    2. Data Agent
    3. Insight Agent
    4. Action Agent
    5. Report Agent
    6. ML Agent
    7. Pipeline Agent
    """

    q = question.lower().strip()

    # =====================================================
    # PIPELINE AGENT ⚙️
    # Priority: Highest
    # =====================================================

    if any(phrase in q for phrase in [

        # Pipeline status
        "pipeline status",
        "pipeline health",
        "pipeline run",
        "pipeline execution",
        "pipeline failed",
        "pipeline success",
        "pipeline scheduled",
        "pipeline schedule",

        # ETL
        "etl status",
        "etl pipeline",
        "etl execution",
        "etl failed",
        "etl success",

        # Airflow
        "airflow",
        "airflow status",
        "airflow running",
        "is airflow running",

        # DAG
        "dag id",
        "dag name",
        "dag status",
        "dag run",
        "dag task",
        "dag tasks",

        # Latest / Last run
        "latest run",
        "latest pipeline run",
        "last run",
        "last pipeline run",
        "latest execution",
        "last execution",

        # Tasks
        "failed task",
        "failed tasks",
        "successful task",
        "successful tasks",
        "running task",
        "running tasks",
        "pipeline task",
        "pipeline tasks",
        "number of tasks",
        "total tasks",

        # Task flow
        "task flow",
        "pipeline flow",

        # Pipeline execution questions
        "is pipeline running",
        "did the pipeline succeed",
        "was the pipeline successful",
        "pipeline successful",

        # Execution status
        "execution status",
        "execution failed",
        "execution success"

    ]):

        return "pipeline_agent"


    # =====================================================
    # REPORT AGENT 📄
    # Priority: High
    # =====================================================

    elif any(word in q for word in [

        "report",
        "generate report",
        "create report",
        "full report",
        "summary report"

    ]):

        return "report_agent"


    # =====================================================
    # ACTION AGENT 🎯
    # Priority: High
    # =====================================================

    elif any(word in q for word in [

        "action",
        "actions",
        "recommend action",
        "recommended action",
        "what should we do",
        "what should i do",
        "business action",
        "recommendation",
        "recommendations"

    ]):

        return "action_agent"


    # =====================================================
    # INSIGHT AGENT 💡
    # Priority: High
    # =====================================================

    elif any(word in q for word in [

        "insight",
        "insights",
        "business insight",
        "business insights",
        "analyze",
        "analysis",
        "trend",
        "trends"

    ]):

        return "insight_agent"


    # =====================================================
    # ML AGENT 🧠
    # =====================================================

    elif any(word in q for word in [

        "predict",
        "prediction",
        "forecast",
        "machine learning",
        "ml",
        "model",
        "anomaly",
        "classification",
        "regression"

    ]):

        return "ml_agent"


    # =====================================================
    # DATA AGENT 📊
    # =====================================================

    elif any(word in q for word in [

        "sales",
        "revenue",
        "product",
        "products",
        "customer",
        "customers",
        "order",
        "orders",

        "data quality",
        "validation",
        "rejected",

        "database",
        "postgresql",

        "chart",
        "graph",
        "visualization"

    ]):

        return "data_agent"


    # =====================================================
    # SUPPORT AGENT 🤝
    # =====================================================

    elif any(phrase in q for phrase in [

        "explain",
        "how does",
        "how do",
        "what is",
        "what are",
        "architecture",
        "bronze",
        "silver",
        "gold",
        "medallion",
        "technology",
        "technologies",
        "project",
        "overview",
        "data flow",
        "scd",
        "about"

    ]):

        return "support_agent"


    # =====================================================
    # DEFAULT
    # =====================================================

    else:

        return "support_agent"