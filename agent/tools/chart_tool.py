# =====================================================
# Chart Recommendation Tool
# =====================================================

def recommend_chart(intent, query=""):
    """
    Recommends the most suitable chart based on
    the data intent and user query.
    """

    q = query.lower()

    # =================================================
    # TOP PRODUCTS
    # =================================================
    if intent == "top_products":

        return {
            "chart_type": "bar",
            "x_axis": "Product Name",
            "y_axis": "Total Orders",
            "title": "Top Ordered Products"
        }

    # =================================================
    # SALES SUMMARY
    # =================================================
    elif intent == "sales_summary":

        if "trend" in q or "time" in q or "year" in q or "month" in q:

            return {
                "chart_type": "line",
                "x_axis": "Time",
                "y_axis": "Sales",
                "title": "Sales Trend"
            }

        return {
            "chart_type": "bar",
            "x_axis": "Department",
            "y_axis": "Items Sold",
            "title": "Sales by Department"
        }

    # =================================================
    # CUSTOMER SUMMARY
    # =================================================
    elif intent == "customer_summary":

        return {
            "chart_type": "bar",
            "x_axis": "Customer ID",
            "y_axis": "Total Orders",
            "title": "Top Customers"
        }

    # =================================================
    # DATA QUALITY
    # =================================================
    elif intent == "data_quality":

        return {
            "chart_type": "pie",
            "labels": ["Passed", "Failed"],
            "title": "Data Quality Status"
        }

    # =================================================
    # ETL HISTORY
    # =================================================
    elif intent == "etl_history":

        return {
            "chart_type": "line",
            "x_axis": "Run Date",
            "y_axis": "Records Processed",
            "title": "ETL Processing History"
        }

    # =================================================
    # ETL STATUS
    # =================================================
    elif intent == "etl_status":

        return {
            "chart_type": "bar",
            "x_axis": "Pipeline Stage",
            "y_axis": "Records Processed",
            "title": "ETL Pipeline Status"
        }

    # =================================================
    # PIPELINE STATUS
    # =================================================
    elif intent == "pipeline_status":

        return {
            "chart_type": "bar",
            "x_axis": "Pipeline",
            "y_axis": "Status",
            "title": "Pipeline Execution Status"
        }

    # =================================================
    # AIRFLOW
    # =================================================
    elif intent == "airflow":

        return {
            "chart_type": "bar",
            "x_axis": "Task",
            "y_axis": "Execution Status",
            "title": "Airflow DAG Status"
        }

    # =================================================
    # PROJECT KNOWLEDGE
    # =================================================
    elif intent == "project_knowledge":

        return {
            "chart_type": None,
            "title": "Project Knowledge"
        }

    # =================================================
    # DEFAULT
    # =================================================
    return {
        "chart_type": None,
        "title": "No chart recommended"
    }