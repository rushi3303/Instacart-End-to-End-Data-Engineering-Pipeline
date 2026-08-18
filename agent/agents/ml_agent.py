# =====================================================
# ML Agent
# =====================================================

def ml_agent(query):
    """
    Handles Machine Learning related questions.

    Supported tasks:
    1. Sales Prediction
    2. Demand Forecasting
    3. Anomaly Detection
    4. Recommendation
    """

    q = query.lower()

    # ==========================================
    # SALES PREDICTION
    # ==========================================
    if (
        "predict" in q
        or "prediction" in q
        or "future sales" in q
        or "sales forecast" in q
    ):

        return {
            "agent": "ML Agent",
            "type": "sales_prediction",
            "data": {
                "status": "ready",
                "message": (
                    "Sales prediction request detected. "
                    "The ML Agent can use historical sales data "
                    "to generate future sales predictions."
                )
            },
            "message": "Sales prediction analysis requested successfully."
        }

    # ==========================================
    # DEMAND FORECASTING
    # ==========================================
    elif (
        "forecast" in q
        or "demand" in q
        or "future demand" in q
    ):

        return {
            "agent": "ML Agent",
            "type": "demand_forecast",
            "data": {
                "status": "ready",
                "message": (
                    "Demand forecasting request detected. "
                    "Historical order and product data can be used "
                    "to forecast future demand."
                )
            },
            "message": "Demand forecasting analysis requested successfully."
        }

    # ==========================================
    # ANOMALY DETECTION
    # ==========================================
    elif (
        "anomaly" in q
        or "anomalies" in q
        or "unusual" in q
        or "outlier" in q
    ):

        return {
            "agent": "ML Agent",
            "type": "anomaly_detection",
            "data": {
                "status": "ready",
                "message": (
                    "Anomaly detection request detected. "
                    "The ML Agent can analyze data and identify "
                    "unusual patterns or abnormal values."
                )
            },
            "message": "Anomaly detection analysis requested successfully."
        }

    # ==========================================
    # RECOMMENDATION
    # ==========================================
    elif (
        "recommend" in q
        or "recommendation" in q
        or "suggest" in q
    ):

        return {
            "agent": "ML Agent",
            "type": "recommendation",
            "data": {
                "status": "ready",
                "message": (
                    "Recommendation request detected. "
                    "The ML Agent can analyze customer and product "
                    "patterns to generate recommendations."
                )
            },
            "message": "Recommendation analysis requested successfully."
        }

    # ==========================================
    # GENERAL ML QUERY
    # ==========================================
    elif (
        "machine learning" in q
        or " ml " in q
        or "model" in q
        or "classification" in q
        or "regression" in q
    ):

        return {
            "agent": "ML Agent",
            "type": "ml_analysis",
            "data": {
                "status": "ready",
                "message": (
                    "Machine Learning analysis request detected. "
                    "The ML Agent is responsible for prediction, "
                    "forecasting, anomaly detection, and recommendations."
                )
            },
            "message": "ML analysis request received successfully."
        }

    # ==========================================
    # UNKNOWN ML REQUEST
    # ==========================================
    return {
        "agent": "ML Agent",
        "type": "unknown",
        "data": None,
        "message": (
            "Sorry, I could not understand the Machine Learning request."
        )
    }