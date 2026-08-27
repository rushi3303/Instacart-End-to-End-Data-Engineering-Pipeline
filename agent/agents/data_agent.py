from agent.gemini_service import GeminiService

from agent.tools.postgres_tool import (
    get_top_products,
    get_sales_summary,
    get_customer_summary,
    get_etl_status,
    get_etl_history,
    get_data_quality_status,
    get_rejected_records,
    execute_read_only_query
)

from agent.tools.airflow_tool import (
    get_airflow_dag_info,
    get_airflow_execution_status
)

from agent.tools.chart_tool import recommend_chart


# ============================================================
# Gemini Service
# ============================================================

gemini = GeminiService()


# ============================================================
# Gold Schema
# ============================================================

GOLD_SCHEMA = """
Gold schema of the Instacart project:

1. gold.customer_summary
   - user_id
   - total_orders
   - last_order_number

2. gold.order_fact
   - order_id
   - user_id
   - order_number
   - order_dow
   - order_hour_of_day
   - eval_set
   - product_id
   - product_name
   - add_to_cart_order
   - reordered

3. gold.product_dimension
   - product_id
   - product_name
   - aisle
   - department
   - effective_date
   - end_date
   - is_current

4. gold.product_dimension_history
   - history_id
   - product_id
   - product_name
   - department
   - aisle
   - effective_date
   - end_date
   - is_current

5. gold.sales_summary
   - department
   - total_products_sold
   - total_orders

6. gold.etl_metadata
   - run_id
   - process_name
   - layer
   - status
   - execution_time
"""


# ============================================================
# Generate SQL using Gemini
# ============================================================

def generate_sql(question):
    """
    Converts a natural-language data question
    into one read-only PostgreSQL query.
    """

    prompt = f"""
You are a PostgreSQL SQL expert for an
Instacart End-to-End Data Engineering project.

Your task is to convert the user's natural-language
question into ONE valid PostgreSQL query.

{GOLD_SCHEMA}

IMPORTANT RULES:

1. Generate ONLY SQL.
2. Do not generate explanations.
3. Do not use markdown code blocks.
4. Use only the tables and columns provided above.
5. Only SELECT or WITH queries are allowed.
6. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER, TRUNCATE, CREATE, GRANT or REVOKE.
7. Do not invent tables.
8. Do not invent columns.
9. If counting users, use DISTINCT user_id where appropriate.
10. Use correct JOIN conditions when multiple tables are required.
11. Return exactly ONE SQL query.

Examples:

Question:
How many users are there?

SQL:
SELECT COUNT(DISTINCT user_id)
FROM gold.customer_summary

Question:
How many orders are there?

SQL:
SELECT COUNT(DISTINCT order_id)
FROM gold.order_fact

Question:
Which department has the most orders?

SQL:
SELECT department, total_orders
FROM gold.sales_summary
ORDER BY total_orders DESC
LIMIT 1

User Question:
{question}
"""

    response = gemini.generate_response(prompt)

    sql = response.strip()

    # Remove markdown fences if Gemini returns them
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


# ============================================================
# Generic LLM → SQL Data Query
# ============================================================

def handle_generic_data_query(query):
    """
    Handles natural-language data questions
    that are not covered by the existing predefined tools.
    """

    try:

        # ----------------------------------------------------
        # STEP 1: Generate SQL
        # ----------------------------------------------------

        sql = generate_sql(query)

        print("\nGenerated SQL:")
        print(sql)

        # ----------------------------------------------------
        # STEP 2: Execute safe read-only SQL
        # ----------------------------------------------------

        result = execute_read_only_query(sql)

        # ----------------------------------------------------
        # STEP 3: Handle SQL error
        # ----------------------------------------------------

        if not result.get("success"):

            return {
                "agent": "Data Agent",
                "type": "sql_error",
                "data": None,
                "sql": sql,
                "message": result.get(
                    "error",
                    "Unable to execute the generated SQL query."
                )
            }

        # ----------------------------------------------------
        # STEP 4: Return live PostgreSQL result
        # ----------------------------------------------------

        return {
            "agent": "Data Agent",
            "type": "sql_query",
            "data": result.get("data"),
            "sql": sql
        }

    except Exception as e:

        return {
            "agent": "Data Agent",
            "type": "sql_error",
            "data": None,
            "message": f"Unable to process the data question: {str(e)}"
        }


# ============================================================
# DATA AGENT
# ============================================================

def data_agent(query):
    """
    Data Agent

    Handles data-related questions using:

    1. Existing predefined PostgreSQL tools
    2. Airflow tools
    3. Chart recommendation
    4. Generic LLM-to-SQL fallback
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
            "chart": recommend_chart(
                "top_products",
                query
            )
        }

    # ==================================================
    # 2. REVENUE NOT AVAILABLE
    # ==================================================

    elif "revenue" in q:

        return {
            "agent": "Data Agent",
            "type": "revenue_not_available",
            "data": None,
            "message": (
                "Revenue is not available in the current "
                "Instacart data model, so total revenue "
                "cannot be calculated from the available data."
            )
        }

    # ==================================================
    # 3. SALES SUMMARY
    # ==================================================

    elif (
        "sales" in q
        or "department sales" in q
    ):

        result = get_sales_summary()

        return {
            "agent": "Data Agent",
            "type": "sales_summary",
            "data": result,
            "chart": recommend_chart(
                "sales_summary",
                query
            )
        }

    # ==================================================
    # 4. CUSTOMER SUMMARY
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
            "chart": recommend_chart(
                "customer_summary",
                query
            )
        }

    # ==================================================
    # 5. REJECTED RECORDS
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
    # 6. DATA QUALITY
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
            "chart": recommend_chart(
                "data_quality",
                query
            )
        }

    # ==================================================
    # 7. ETL HISTORY
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
            "chart": recommend_chart(
                "etl_history",
                query
            )
        }

    # ==================================================
    # 8. AIRFLOW PIPELINE STATUS
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
            "chart": recommend_chart(
                "etl_status",
                query
            )
        }

    # ==================================================
    # 9. AIRFLOW DAG INFORMATION
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
            "chart": recommend_chart(
                "airflow",
                query
            )
        }

    # ==================================================
    # 10. ETL STATUS
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
            "chart": recommend_chart(
                "etl_status",
                query
            )
        }

    # ==================================================
    # 11. CHART / VISUALIZATION REQUEST
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
                "For example: sales, products, customers, "
                "orders, or ETL history."
            )
        }

    # ==================================================
    # 12. GENERIC LLM → SQL FALLBACK
    # ==================================================

    else:

        return handle_generic_data_query(query)