# =====================================================
# Report Agent - Complete Data & Business Report
# =====================================================

from agent.agents.data_agent import data_agent
from agent.agents.insight_agent import generate_insights
from agent.agents.action_agent import generate_actions


# =====================================================
# Create Complete Report
# =====================================================

def create_report(data):
    """
    Creates a complete business report using:

    1. Actual data from Data Agent
    2. Insights from Insight Agent
    3. Recommended actions from Action Agent
    """

    # Generate insights from collected data
    insights = generate_insights(
        "summary_report",
        data
    )

    # Generate recommended actions
    actions = generate_actions(
        "summary_report",
        data
    )

    return {
        "title": "Instacart Business Summary Report",
        "data": data,
        "insights": insights,
        "recommended_actions": actions
    }


# =====================================================
# REPORT AGENT
# =====================================================

def report_agent(query):
    """
    Report Agent workflow:

        User Question
             ↓
        Report Agent
             ↓
        Data Agent
             ↓
        Multiple Data Sources
             ↓
        Insight Agent
             ↓
        Action Agent
             ↓
        Complete Report
    """

    try:

        # =================================================
        # STEP 1: Collect Top Products
        # =================================================

        products_result = data_agent(
            "Show me the top 5 products by order count."
        )

        # =================================================
        # STEP 2: Collect Sales Summary
        # =================================================

        sales_result = data_agent(
            "Show me department sales."
        )

        # =================================================
        # STEP 3: Collect Customer Summary
        # =================================================

        customer_result = data_agent(
            "Show me the most active customers based on order frequency."
        )

        # =================================================
        # STEP 4: Collect ETL Status
        # =================================================

        etl_result = data_agent(
            "Show me the ETL status."
        )

        # =================================================
        # STEP 5: Combine Data
        # =================================================

        combined_data = {
            "top_products": products_result.get(
                "data"
            ),

            "sales_summary": sales_result.get(
                "data"
            ),

            "customer_summary": customer_result.get(
                "data"
            ),

            "etl_status": etl_result.get(
                "data"
            )
        }

        # =================================================
        # STEP 6: Create Complete Report
        # =================================================

        report = create_report(
            combined_data
        )

        # =================================================
        # STEP 7: Return Result
        # =================================================

        return {
            "agent": "Report Agent",
            "type": "summary_report",
            "data": combined_data,
            "report": report,
            "message": (
                "Summary report generated successfully."
            )
        }

    except Exception as e:

        return {
            "agent": "Report Agent",
            "type": "error",
            "data": None,
            "report": None,
            "message": (
                f"Report Agent Error: {str(e)}"
            )
        }