from agent.tools.postgres_tool import (
    get_top_products,
    get_sales_summary,
    get_customer_summary,
    get_etl_status,
    get_etl_history,
    get_data_quality_status,
    get_rejected_records
)

from agent.tools.airflow_tool import (
    get_airflow_dag_info,
    get_airflow_execution_status
)

from agent.tools.chart_tool import recommend_chart


def data_agent(query):
    """
    Data Agent

    Handles data-related questions using:
    1. PostgreSQL
    2. Airflow
    3. Chart Recommendation
    """

    q = query.lower().strip()

    # ==================================================
    # 1. TOP PRODUCTS
    # ==================================================
    if (
        ("product" in q or "products" in q or "item" in q)
        and (
            "top" in q
            or "popular" in q
            or "best" in q
            or "most" in q
        )
    ):

        result = get_top_products(5)

        return {
            "agent": "Data Agent",
            "type": "top_products",
            "data": result,
            "chart": recommend_chart("top_products", query)
        }

    # ==================================================
    # 2. SALES / REVENUE SUMMARY
    # ==================================================
    elif (
        "sales" in q
        or "revenue" in q
        or "department sales" in q
    ):

        result = get_sales_summary()

        return {
            "agent": "Data Agent",
            "type": "sales_summary",
            "data": result,
            "chart": recommend_chart("sales_summary", query)
        }

    # ==================================================
    # 3. CUSTOMER SUMMARY
    # ==================================================
    elif (
        "customer" in q
        or "customers" in q
    ):

        result = get_customer_summary(10)

        return {
            "agent": "Data Agent",
            "type": "customer_summary",
            "data": result,
            "chart": recommend_chart("customer_summary", query)
        }

    # ==================================================
    # 4. REJECTED RECORDS
    # ==================================================
    elif (
        "rejected" in q
        or "reject" in q
        or "failed records" in q
    ):

        result = get_rejected_records()

        return {
            "agent": "Data Agent",
            "type": "rejected_records",
            "data": result
        }

    # ==================================================
    # 5. DATA QUALITY
    # ==================================================
    elif (
        "quality" in q
        or "validation" in q
        or "data issue" in q
        or "data issues" in q
    ):

        result = get_data_quality_status()

        return {
            "agent": "Data Agent",
            "type": "data_quality",
            "data": result,
            "chart": recommend_chart("data_quality", query)
        }

    # ==================================================
    # 6. ETL HISTORY
    # ==================================================
    elif (
        "etl history" in q
        or "pipeline history" in q
        or "previous run" in q
        or "past run" in q
    ):

        result = get_etl_history(5)

        return {
            "agent": "Data Agent",
            "type": "etl_history",
            "data": result,
            "chart": recommend_chart("etl_history", query)
        }

    # ==================================================
    # 7. AIRFLOW PIPELINE STATUS
    # ==================================================
    elif (
        "pipeline status" in q
        or "airflow status" in q
        or "dag status" in q
        or "latest run" in q
    ):

        result = get_airflow_execution_status()

        return {
            "agent": "Data Agent",
            "type": "pipeline_status",
            "data": result,
            "chart": recommend_chart("etl_status", query)
        }

    # ==================================================
    # 8. AIRFLOW DAG INFORMATION
    # ==================================================
    elif (
        "airflow" in q
        or "dag" in q
        or "pipeline tasks" in q
    ):

        result = get_airflow_dag_info()

        return {
            "agent": "Data Agent",
            "type": "airflow",
            "data": result,
            "chart": recommend_chart("airflow", query)
        }

    # ==================================================
    # 9. ETL STATUS
    # ==================================================
    elif (
        "etl status" in q
        or "etl" in q
        or "pipeline" in q
        or "processed" in q
        or "records" in q
    ):

        result = get_etl_status(10)

        return {
            "agent": "Data Agent",
            "type": "etl_status",
            "data": result,
            "chart": recommend_chart("etl_status", query)
        }

    # ==================================================
    # 10. CHART / VISUALIZATION REQUEST
    # ==================================================
    elif (
        "chart" in q
        or "graph" in q
        or "visualization" in q
        or "visualize" in q
    ):

        return {
            "agent": "Data Agent",
            "type": "chart_recommendation",
            "data": None,
            "message": (
                "Please specify the data you want to visualize. "
                "For example: sales, products, customers, or ETL history."
            )
        }

    # ==================================================
    # UNKNOWN
    # ==================================================
    else:

        return {
            "agent": "Data Agent",
            "type": "unknown",
            "data": None,
            "message": "Sorry, I could not understand the data request."
        }