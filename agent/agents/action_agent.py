# =====================================================
# Action Agent - Actionable Business Recommendations
# =====================================================

from agent.agents.data_agent import data_agent


def generate_actions(intent, data):
    """
    Generates actionable recommendations based on
    the actual data returned by the Data Agent.
    """

    actions = []

    if not data:
        return ["No data available to generate actions."]

    # =================================================
    # TOP PRODUCTS
    # =================================================
    if intent == "top_products" and isinstance(data, list):

        if len(data) > 0:

            top_product = data[0]

            actions.append(
                f"Inventory Action: Maintain sufficient stock for "
                f"'{top_product[1]}' because it has the highest demand "
                f"with {top_product[2]:,} orders."
            )

        actions.append(
            "Supply Chain Action: Prioritize procurement and replenishment "
            "for high-demand products."
        )

        actions.append(
            "Business Action: Use top-performing products in promotions "
            "and cross-selling strategies."
        )

    # =================================================
    # SALES SUMMARY
    # =================================================
    elif intent == "sales_summary" and isinstance(data, list):

        if len(data) > 0:

            top_department = max(data, key=lambda x: x[1])
            low_department = min(data, key=lambda x: x[1])

            actions.append(
                f"Growth Action: Continue investment in "
                f"'{top_department[0]}' because it has the strongest sales volume."
            )

            actions.append(
                f"Improvement Action: Review '{low_department[0]}' "
                f"to identify opportunities for pricing, promotion, "
                f"or product assortment improvements."
            )

        actions.append(
            "Management Action: Monitor department-level performance "
            "regularly to detect sales changes early."
        )

    # =================================================
    # CUSTOMER SUMMARY
    # =================================================
    elif intent == "customer_summary" and isinstance(data, list):

        if len(data) > 0:

            top_customer = data[0]

            actions.append(
                f"Retention Action: Reward high-value customer "
                f"User ID {top_customer[0]} through loyalty programs "
                f"or personalized offers."
            )

        actions.append(
            "Customer Action: Create targeted campaigns for repeat customers."
        )

        actions.append(
            "Analytics Action: Identify customers with declining order "
            "frequency and run retention campaigns."
        )

    # =================================================
    # DATA QUALITY
    # =================================================
    elif intent == "data_quality":

        actions.append(
            "Monitoring Action: Continue automated validation checks "
            "across Bronze, Silver, and Gold layers."
        )

        actions.append(
            "Prevention Action: Add alerts when rejected records "
            "or validation failures increase."
        )

    # =================================================
    # ETL STATUS
    # =================================================
    elif intent == "etl_status":

        actions.append(
            "Pipeline Action: Continue monitoring ETL execution status "
            "and processing duration."
        )

        actions.append(
            "Performance Action: Investigate transformation steps "
            "with the highest execution time."
        )

    # =================================================
    # ETL HISTORY
    # =================================================
    elif intent == "etl_history":

        actions.append(
            "Monitoring Action: Compare historical pipeline execution "
            "times to detect performance degradation."
        )

        actions.append(
            "Optimization Action: Review pipelines with increasing "
            "processing duration."
        )

    # =================================================
    # AIRFLOW
    # =================================================
    elif intent == "airflow":

        actions.append(
            "Orchestration Action: Monitor failed or delayed Airflow tasks."
        )

        actions.append(
            "Reliability Action: Configure retry and alert mechanisms "
            "for critical pipeline tasks."
        )

    # =================================================
    # DEFAULT
    # =================================================
    else:

        actions.append(
            "Review the available data and identify the next business action."
        )

    return actions


def action_agent(query):
    """
    Action Agent:

    1. Receives the user question
    2. Calls the Data Agent
    3. Gets actual database/tool data
    4. Generates actionable recommendations
    """

    data_result = data_agent(query)

    intent = data_result.get("type")
    data = data_result.get("data")

    # Generate actions from actual data
    actions = generate_actions(intent, data)

    return {
        "agent": "Action Agent",
        "type": intent,
        "data": data,
        "actions": actions,
        "message": "Action recommendations generated successfully."
    }