# =====================================================
# Report Agent - Complete Data & Business Report
# =====================================================

from agent.agents.data_agent import data_agent
from agent.agents.insight_agent import generate_insights
from agent.agents.action_agent import generate_actions


def create_report(intent, data):
    """
    Creates a structured report using:

    1. Actual data from Data Agent
    2. Insights from Insight Agent
    3. Actions from Action Agent
    """

    insights = generate_insights(intent, data)

    actions = generate_actions(intent, data)

    report = {
        "title": f"{intent.replace('_', ' ').title()} Report",
        "data": data,
        "insights": insights,
        "recommended_actions": actions
    }

    return report


def report_agent(query):
    """
    Report Agent:

    1. Receives report request
    2. Calls Data Agent
    3. Gets actual project/database data
    4. Generates insights
    5. Generates recommended actions
    6. Creates a complete report
    """

    # Step 1: Get actual data
    data_result = data_agent(query)

    intent = data_result.get("type")
    data = data_result.get("data")

    # Check if data request was successful
    if intent == "unknown":

        return {
            "agent": "Report Agent",
            "type": "unknown",
            "data": None,
            "report": None,
            "message": "Sorry, I could not identify the data required for the report."
        }

    # Step 2: Create complete report
    report = create_report(intent, data)

    return {
        "agent": "Report Agent",
        "type": intent,
        "data": data,
        "report": report,
        "message": "Report generated successfully."
    }